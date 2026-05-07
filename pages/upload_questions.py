# Author: rana-mostakin
"""
ThinkTrace v1 — User Question Upload
Students can upload their own questions (PDF, image, text).
The Socratic engine extracts, parses, and runs diagnosis on them.
Zero extra API calls for extraction — uses Claude vision only when image uploaded.
"""

import streamlit as st
import json
import re
import io
import os
import anthropic
from datetime import datetime

# ── EXTRACTION HELPERS ────────────────────────────────────────────────────────

def extract_from_text(raw: str) -> list[dict]:
    """
    Parse plain text into question dicts.
    Accepts numbered lists, bullet points, Q: format, or raw paragraphs.
    Returns a list of {text, subject_hint, topic_hint} dicts.
    """
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    questions = []
    buffer = []

    def flush():
        if buffer:
            q = " ".join(buffer).strip()
            # Strip leading markers: 1. Q: - * etc.
            q = re.sub(r'^[\d]+[\.\)]\s*', '', q)
            q = re.sub(r'^[Qq][\d]*[\.\):]\s*', '', q)
            q = re.sub(r'^[-*•]\s*', '', q)
            if len(q) > 15:
                questions.append({"text": q, "subject_hint": "", "topic_hint": ""})
            buffer.clear()

    for line in lines:
        # New question starts with numbering or Q: marker
        if re.match(r'^[\d]+[\.\)]', line) or re.match(r'^[Qq][\d]*[\.\):]', line) or re.match(r'^[-*•]', line):
            flush()
            buffer.append(line)
        else:
            if buffer:
                buffer.append(line)
            else:
                # No marker — treat each non-empty line as a question if long enough
                if len(line) > 20:
                    questions.append({"text": line, "subject_hint": "", "topic_hint": ""})

    flush()
    return questions


def extract_from_image_via_claude(image_bytes: bytes, mime: str) -> list[dict]:
    """
    Use Claude vision to extract questions from an image (photo of paper, screenshot, PDF page).
    Only called when user uploads an image — one API call total.
    """
    import base64
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
    b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    system = (
        "You are a question extractor. Extract all questions from the image. "
        "Return ONLY valid JSON: {\"questions\": [\"question text\", ...]}. "
        "No preamble. No explanation. If no questions found, return {\"questions\": []}."
    )
    msg = {
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64}},
            {"type": "text", "text": "Extract all questions from this image."},
        ],
    }
    try:
        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=800,
            system=system,
            messages=[msg],
        )
        raw = resp.content[0].text
        raw = re.sub(r"```json|```", "", raw).strip()
        data = json.loads(raw)
        return [{"text": q, "subject_hint": "", "topic_hint": ""} for q in data.get("questions", [])]
    except Exception:
        return []


def classify_question(q_text: str, available_subjects: list[str]) -> dict:
    """
    Lightweight local classifier — no API call.
    Detects subject and topic hint from keywords in the question text.
    """
    text_lower = q_text.lower()

    keyword_map = {
        "Physics": ["force", "mass", "velocity", "acceleration", "newton", "energy", "work",
                    "momentum", "wave", "frequency", "electric", "magnetic", "optics", "quantum",
                    "gravity", "friction", "pressure", "thermodynamics", "heat", "torque"],
        "Chemistry": ["atom", "molecule", "bond", "reaction", "acid", "base", "ph", "oxidation",
                      "reduction", "equilibrium", "stoichiometry", "mole", "electron", "orbital",
                      "periodic", "entropy", "enthalpy", "electrolysis", "organic", "carbon"],
        "Higher Math": ["derivative", "integral", "limit", "matrix", "vector", "probability",
                        "series", "differential", "function", "equation", "complex number",
                        "geometry", "conic", "determinant", "eigenvalue", "fourier"],
        "DSAT": ["passage", "author", "evidence", "inference", "sentence", "grammar",
                 "vocabulary", "reading", "writing", "algebra", "geometry", "statistics"],
        "IELTS": ["essay", "task 1", "task 2", "speaking", "listening", "reading passage",
                  "ielts", "band", "coherence", "cohesion", "paraphrase"],
        "Biology": ["cell", "dna", "gene", "protein", "enzyme", "photosynthesis", "respiration",
                    "evolution", "ecosystem", "nervous", "immune", "reproduction", "biotechnology"],
    }

    scores = {subj: 0 for subj in available_subjects}
    for subj, keywords in keyword_map.items():
        if subj in available_subjects:
            for kw in keywords:
                if kw in text_lower:
                    scores[subj] += 1

    best = max(scores, key=lambda s: scores[s]) if scores else "Physics"
    if scores.get(best, 0) == 0:
        best = ""

    return {"subject_hint": best, "topic_hint": ""}


# ── SOCRATIC ANALYSIS OF UPLOADED QUESTION ────────────────────────────────────

def analyze_uploaded_question(
    q_text: str,
    subject: str,
    language: str,
) -> dict:
    """
    Run one Socratic diagnostic call on an uploaded question.
    Returns the standard socratic JSON response.
    This is the ONLY API call per question analysis.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

    system = f"""You are a Socratic reasoning diagnostician analyzing a student's uploaded question.
The student submitted this question from their own study material (exam paper, textbook, worksheet).
Your task:
1. Understand what concept this question is testing.
2. Generate ONE Socratic question that probes whether the student genuinely understands the CAUSAL reasoning behind this concept — not just the calculation.
3. Identify which reasoning gap this question is most likely to reveal.

Subject: {subject}
Language for all text: {language}
Respond ONLY in valid JSON matching this structure exactly:

{{
  "concept_identified": "what core concept this question tests",
  "q_intro": "1 sentence warm intro relating to their uploaded question",
  "q_number": "Q 01",
  "q_topic": "short descriptor",
  "q_text": "your Socratic probe using **bold** for key causal terms",
  "q_needs_figure": false,
  "q_figure_type": "none",
  "q_figure_params": {{}},
  "q_hint": null,
  "gap_detected": false,
  "gap_description": "",
  "gap_location": "",
  "depth_level": 1,
  "reasoning_style_signal": "unclear",
  "confidence": 0.8,
  "likely_gaps": ["gap A that this question often surfaces", "gap B"]
}}"""

    try:
        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=900,
            system=system,
            messages=[{"role": "user", "content": f"Student's uploaded question:\n\n{q_text}"}],
        )
        raw = resp.content[0].text
        raw = re.sub(r"```json|```", "", raw).strip()
        s = raw.find("{"); e = raw.rfind("}")
        if s != -1 and e != -1:
            raw = raw[s:e+1]
        return json.loads(raw)
    except Exception:
        return {
            "concept_identified": "Unknown concept",
            "q_intro": "Let's explore what this question is really testing.",
            "q_number": "Q 01",
            "q_topic": subject,
            "q_text": f"Before solving, can you explain **why** this type of question matters — what concept does it fundamentally test?",
            "q_needs_figure": False,
            "q_figure_type": "none",
            "q_figure_params": {},
            "q_hint": None,
            "gap_detected": False,
            "gap_description": "",
            "gap_location": "",
            "depth_level": 1,
            "reasoning_style_signal": "unclear",
            "confidence": 0.5,
            "likely_gaps": [],
        }


# ── UI ────────────────────────────────────────────────────────────────────────

def show_upload_questions():
    """Main upload questions page."""
    from data.subjects import SUBJECTS

    st.markdown("""
    <div style="margin-bottom:1.5rem">
      <div class="tt-h2">Upload Your Questions</div>
      <div style="font-size:13px;color:var(--text2);font-family:'DM Sans',sans-serif;
                  margin-top:4px;line-height:1.6">
        Upload questions from your exam papers, textbooks, or worksheets.
        ThinkTrace will run Socratic analysis on each one — identifying the reasoning
        gaps they are most likely to reveal.
      </div>
    </div>
    """, unsafe_allow_html=True)

    available_subjects = list(SUBJECTS.keys())

    # ── UPLOAD SECTION ────────────────────────────────────────────────────────
    st.markdown('<div class="glass-card gc-accent" style="margin-bottom:1rem">', unsafe_allow_html=True)
    st.markdown('<div class="tt-label" style="margin-bottom:0.75rem">Upload Source</div>', unsafe_allow_html=True)

    tab_txt, tab_img = st.tabs(["Text / Paste", "Image / Photo"])

    extracted_questions = st.session_state.get("uploaded_qs", [])

    with tab_txt:
        st.markdown("""
        <div style="font-size:12px;color:var(--text2);margin-bottom:.5rem">
        Paste questions directly — numbered list, bullet points, or one per line.
        </div>""", unsafe_allow_html=True)

        raw_text = st.text_area(
            "Paste questions here",
            height=180,
            placeholder="1. A ball is thrown upward. What determines how high it goes?\n2. Explain why salt dissolves in water but oil does not.\n3. ...",
            key="upload_text_input",
            label_visibility="collapsed",
        )
        if st.button("Extract Questions", key="extract_text_btn", type="primary"):
            if raw_text.strip():
                qs = extract_from_text(raw_text)
                # Auto-classify subject
                for q in qs:
                    cls = classify_question(q["text"], available_subjects)
                    q["subject_hint"] = cls["subject_hint"]
                st.session_state["uploaded_qs"] = qs
                st.rerun()
            else:
                st.warning("Paste some questions first.")

    with tab_img:
        st.markdown("""
        <div style="font-size:12px;color:var(--text2);margin-bottom:.5rem">
        Upload a photo of your exam paper, a screenshot, or a worksheet image.
        Claude Vision will extract the questions automatically.
        <strong style="color:var(--amber)">Note:</strong> uses 1 API call per upload.
        </div>""", unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload image",
            type=["png", "jpg", "jpeg", "webp"],
            key="upload_img_input",
            label_visibility="collapsed",
        )
        if uploaded_file and st.button("Extract from Image", key="extract_img_btn", type="primary"):
            mime_map = {"png": "image/png", "jpg": "image/jpeg",
                        "jpeg": "image/jpeg", "webp": "image/webp"}
            ext = uploaded_file.name.split(".")[-1].lower()
            mime = mime_map.get(ext, "image/jpeg")
            with st.spinner("Reading image…"):
                img_bytes = uploaded_file.read()
                qs = extract_from_image_via_claude(img_bytes, mime)
                for q in qs:
                    cls = classify_question(q["text"], available_subjects)
                    q["subject_hint"] = cls["subject_hint"]
                st.session_state["uploaded_qs"] = qs
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ── REVIEW & CONFIGURE ────────────────────────────────────────────────────
    if not extracted_questions:
        st.markdown("""
        <div style="text-align:center;padding:2rem;color:var(--text3);font-family:'DM Sans',sans-serif;
                    font-size:13px">
          Upload questions above to begin. They will appear here for review.
        </div>""", unsafe_allow_html=True)
        return

    user_lang = st.session_state.get("user", {}).get("language", "English")

    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem">
      <div class="tt-label">{len(extracted_questions)} Questions Extracted</div>
      <div style="font-size:11px;color:var(--text3)">Review and assign subjects before analysis</div>
    </div>""", unsafe_allow_html=True)

    updated_qs = []
    for i, q in enumerate(extracted_questions):
        st.markdown(f'<div class="glass-card" style="margin-bottom:8px">', unsafe_allow_html=True)

        col_q, col_s = st.columns([3, 1])
        with col_q:
            # Editable question text
            edited_text = st.text_area(
                f"Q{i+1}",
                value=q["text"],
                height=80,
                key=f"q_text_{i}",
                label_visibility="collapsed",
            )
        with col_s:
            subject_options = ["Auto-detect"] + available_subjects
            default_idx = 0
            if q.get("subject_hint") and q["subject_hint"] in available_subjects:
                default_idx = available_subjects.index(q["subject_hint"]) + 1
            chosen_subj = st.selectbox(
                "Subject",
                subject_options,
                index=default_idx,
                key=f"q_subj_{i}",
                label_visibility="visible",
            )
            if chosen_subj == "Auto-detect":
                chosen_subj = q.get("subject_hint", "Physics") or "Physics"

        updated_qs.append({
            "text": edited_text,
            "subject_hint": chosen_subj,
            "topic_hint": q.get("topic_hint", ""),
        })
        st.markdown('</div>', unsafe_allow_html=True)

    st.session_state["uploaded_qs"] = updated_qs

    st.markdown('<div style="display:flex;gap:10px;margin-top:.5rem">', unsafe_allow_html=True)
    col_run, col_clear = st.columns([2, 1])

    with col_run:
        run_analysis = st.button(
            f"Run Socratic Analysis on {len(updated_qs)} Questions",
            type="primary",
            key="run_upload_analysis",
        )
    with col_clear:
        if st.button("Clear All", key="clear_upload"):
            st.session_state.pop("uploaded_qs", None)
            st.session_state.pop("upload_results", None)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ── ANALYSIS RESULTS ──────────────────────────────────────────────────────
    if run_analysis:
        results = []
        prog = st.progress(0, text="Analyzing questions…")
        for i, q in enumerate(updated_qs):
            prog.progress((i) / len(updated_qs), text=f"Analyzing Q{i+1} of {len(updated_qs)}…")
            result = analyze_uploaded_question(
                q_text=q["text"],
                subject=q["subject_hint"] or "Physics",
                language=user_lang,
            )
            result["original_question"] = q["text"]
            result["assigned_subject"] = q["subject_hint"]
            results.append(result)
        prog.progress(1.0, text="Done.")
        st.session_state["upload_results"] = results
        st.rerun()

    results = st.session_state.get("upload_results", [])
    if not results:
        return

    st.markdown('<div class="tt-label" style="margin-top:1.5rem;margin-bottom:.75rem">Analysis Results</div>', unsafe_allow_html=True)

    for i, r in enumerate(results):
        concept = r.get("concept_identified", "")
        likely_gaps = r.get("likely_gaps", [])
        q_intro = r.get("q_intro", "")
        q_text = r.get("q_text", "")
        orig = r.get("original_question", "")
        subj = r.get("assigned_subject", "")

        # Format bold in q_text
        q_text_html = re.sub(r'\*\*(.+?)\*\*', r'<span class="q-key">\1</span>', q_text)

        st.markdown(f"""
        <div class="glass-card" style="margin-bottom:12px">
          <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:.75rem">
            <div>
              <div style="font-family:'Syne',sans-serif;font-size:10px;font-weight:700;
                          letter-spacing:.08em;text-transform:uppercase;color:var(--accent2);
                          margin-bottom:4px">Q{i+1} — {subj}</div>
              <div style="font-size:13px;color:var(--text2);font-style:italic;
                          border-left:2px solid var(--border2);padding-left:10px;
                          line-height:1.6">{orig}</div>
            </div>
          </div>

          <div style="background:rgba(124,111,255,.05);border:1px solid rgba(124,111,255,.15);
                      border-radius:10px;padding:.75rem 1rem;margin-bottom:.75rem">
            <div style="font-family:'Syne',sans-serif;font-size:10px;font-weight:700;
                        letter-spacing:.06em;text-transform:uppercase;color:var(--text3);
                        margin-bottom:4px">Concept Identified</div>
            <div style="font-size:13px;color:var(--accent2);font-weight:500">{concept}</div>
          </div>

          <div class="q-intro">{q_intro}</div>
          <div class="q-card" style="margin-top:.5rem">
            <div class="q-header">Socratic Probe</div>
            <div class="q-body">{q_text_html}</div>
          </div>

          {'<div style="margin-top:.75rem"><div style="font-family:Syne,sans-serif;font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--amber);margin-bottom:6px">Likely Gaps This Question Surfaces</div>' + "".join(f'<div style="font-size:12px;color:var(--text2);padding:3px 0;display:flex;align-items:flex-start;gap:6px"><span style="color:var(--red);margin-top:2px">⚡</span>{g}</div>' for g in likely_gaps) + '</div>' if likely_gaps else ''}
        </div>
        """, unsafe_allow_html=True)

        # Start session with this question
        if st.button(f"Start Session with Q{i+1}", key=f"start_upload_session_{i}"):
            st.session_state["setup_subject"] = subj or "Physics"
            st.session_state["upload_session_q"] = r
            st.session_state["page"] = "session"
            st.rerun()

    # Export results as JSON
    if results:
        export_data = json.dumps(results, indent=2, ensure_ascii=False)
        st.download_button(
            "Download Analysis (JSON)",
            data=export_data.encode("utf-8"),
            file_name=f"thinktrace_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            key="download_analysis",
        )
