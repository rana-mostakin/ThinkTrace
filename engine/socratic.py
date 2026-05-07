# Author: rana-mostakin
"""
ThinkTrace v1 — Socratic Reasoning Engine
Core AI: Claude API for Socratic diagnosis + response rendering.
"""

import json
import os
import re
import anthropic
from typing import Optional, Generator
from engine.figure_gen import figure_html

# ── CLIENT ────────────────────────────────────────────────────────────────────

def _get_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    return anthropic.Anthropic(api_key=api_key)


# ── SYSTEM PROMPT ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a Socratic reasoning diagnostician embedded in ThinkTrace, a cognitive laboratory.
Your sole purpose: find the EXACT broken causal link in the student's reasoning chain.

RULES:
- Do NOT teach. Do NOT correct. Do NOT lecture. Ask ONE question one causal level deeper.
- Never reveal the answer. Never confirm if the student is right — only probe deeper.
- Find gaps in CAUSAL understanding, not calculation errors.
- Wrong calculation → neutral question. Missing causal link → mark as gap.
- Each question must go exactly one level deeper than the previous.
- Maximum depth: 5. At depth 5, you may surface the gap if found.
- Adapt framing to detected reasoning style: {style}
- All text fields must be in: {language}. Keep math notation and technical terms international.

RESPONSE: Respond ONLY in valid JSON. No preamble, no markdown, no explanation.

Return exactly this structure:
{{
  "q_intro": "warm 1-sentence validation or setup (italic floating text — NOT the question itself)",
  "q_number": "Q 01",
  "q_topic": "short 2-4 word descriptor",
  "q_text": "the Socratic question using **bold** for key causal terms",
  "q_needs_figure": false,
  "q_figure_type": "none",
  "q_figure_params": {{}},
  "q_hint": null,
  "gap_detected": false,
  "gap_description": "",
  "gap_location": "",
  "depth_level": 1,
  "reasoning_style_signal": "unclear",
  "confidence": 0.85
}}

q_figure_type options: force_diagram, velocity_diagram, molecular, graph_curve, process_flow, rocket_diagram, circuit_diagram, none
reasoning_style_signal options: analytical, visual, procedural, analogical, unclear
gap_detected: true ONLY when you identify a structural causal misunderstanding (not wrong math)
gap_location: "ConceptA -> ConceptB" format (which causal link is broken)
"""


# ── INITIAL QUESTION GENERATOR ────────────────────────────────────────────────

INITIAL_SYSTEM = """You are starting a Socratic diagnostic session.
Generate the FIRST question — broad enough to surface the student's current understanding.
Start at depth 1. Do NOT assume any gaps yet.
All text in: {language}. Respond ONLY in valid JSON.

Return exactly this structure:
{{
  "q_intro": "brief warm session-opening line",
  "q_number": "Q 01",
  "q_topic": "short descriptor",
  "q_text": "an open diagnostic question to map current understanding",
  "q_needs_figure": false,
  "q_figure_type": "none",
  "q_figure_params": {{}},
  "q_hint": null,
  "gap_detected": false,
  "gap_description": "",
  "gap_location": "",
  "depth_level": 1,
  "reasoning_style_signal": "unclear",
  "confidence": 0.7
}}"""


def generate_initial_question(subject: str, topics: list[str], language: str) -> dict:
    """Generate the opening question for a session."""
    client = _get_client()
    topics_str = ", ".join(topics)

    system = INITIAL_SYSTEM.format(language=language)
    user_msg = (
        f"Subject: {subject}\n"
        f"Topics selected: {topics_str}\n"
        f"Generate the first diagnostic question to map the student's understanding."
    )

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=system,
            messages=[{"role": "user", "content": user_msg}],
        )
        raw = response.content[0].text
        data = _safe_json(raw)
        return data
    except Exception as e:
        return _fallback_question(subject, topics, 1)


def generate_next_question(
    subject: str,
    topics: list[str],
    language: str,
    conversation: list[dict],
    current_depth: int,
    reasoning_style: str = "unclear",
) -> dict:
    """Generate the next Socratic question based on conversation history."""
    client = _get_client()

    system = SYSTEM_PROMPT.format(language=language, style=reasoning_style)

    # Build message list for Claude
    messages = []
    for msg in conversation:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})

    # Add context injection
    ctx = (
        f"\n\n[CONTEXT: Subject={subject}, Topics={', '.join(topics)}, "
        f"Current depth={current_depth}, Max depth=5, Language={language}]"
    )
    if messages and messages[-1]["role"] == "user":
        messages[-1]["content"] += ctx
    else:
        messages.append({"role": "user", "content": ctx})

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=system,
            messages=messages,
        )
        raw = response.content[0].text
        data = _safe_json(raw)
        data["depth_level"] = current_depth + 1
        return data
    except Exception as e:
        return _fallback_question(subject, topics, current_depth + 1)


# ── BRIDGE GENERATOR ──────────────────────────────────────────────────────────

BRIDGE_SYSTEM = """You are a targeted concept repair teacher.
A reasoning gap was found. Create a 4-minute bridge lesson that DIRECTLY repairs the broken causal link.
Do NOT be general. Target EXACTLY the gap described.
Language: {language}. Respond ONLY in valid JSON.

Return:
{{
  "bridge_title": "short lesson title",
  "bridge_intro": "1 sentence: what was broken and what this lesson repairs",
  "core_explanation": "2-3 paragraph causal explanation (use **bold** for key terms)",
  "analogy": "one concrete everyday analogy",
  "practice": [
    {{"level": "Easy",   "question": "...", "answer_hint": "..."}},
    {{"level": "Medium", "question": "...", "answer_hint": "..."}},
    {{"level": "Hard",   "question": "...", "answer_hint": "..."}}
  ]
}}"""


def generate_bridge(gap_location: str, gap_description: str,
                    subject: str, language: str) -> dict:
    """Generate a targeted bridge lesson for a detected gap."""
    client = _get_client()

    system = BRIDGE_SYSTEM.format(language=language)
    user_msg = (
        f"Subject: {subject}\n"
        f"Gap location: {gap_location}\n"
        f"Gap description: {gap_description}\n"
        f"Generate a 4-minute bridge lesson."
    )

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=system,
            messages=[{"role": "user", "content": user_msg}],
        )
        raw = response.content[0].text
        return _safe_json(raw)
    except Exception:
        return {
            "bridge_title": f"Repairing: {gap_location}",
            "bridge_intro": gap_description,
            "core_explanation": "Please review your textbook for this concept.",
            "analogy": "",
            "practice": [],
        }


# ── RENDERING ─────────────────────────────────────────────────────────────────

def render_question_html(q: dict, show_figure: bool = True) -> str:
    """
    Renders the two-part question format as HTML.
    Part 1: Floating conversational intro (italic, no card)
    Part 2: Question card with accent bar, header, body, optional hint
    """
    intro = q.get("q_intro", "")
    q_number = q.get("q_number", "Q 01")
    q_topic = q.get("q_topic", "")
    q_text = q.get("q_text", "")
    q_hint = q.get("q_hint")

    # Render key terms: **bold** → accent colored span
    q_text_html = _render_bold(q_text)

    # Auto figure
    figure_svg = ""
    if show_figure and q.get("q_needs_figure"):
        fig_type = q.get("q_figure_type", "none")
        fig_params = q.get("q_figure_params", {})
        if fig_type and fig_type != "none":
            figure_svg = figure_html(fig_type, fig_params)

    hint_html = ""
    if q_hint:
        hint_html = f'<div class="q-hint">↳ {q_hint}</div>'

    html = f"""
<div class="q-intro">{intro}</div>
<div class="q-card">
  <div class="q-header">{q_number} — {q_topic}</div>
  <div class="q-body">{q_text_html}</div>
  {figure_svg}
  {hint_html}
</div>
"""
    return html


def render_gap_html(q: dict) -> str:
    """Renders a gap alert card."""
    if not q.get("gap_detected"):
        return ""

    depth = q.get("depth_level", 1)
    gap_desc = q.get("gap_description", "A reasoning gap was detected.")
    gap_loc = q.get("gap_location", "")

    bridge_link = ""
    if gap_loc:
        bridge_link = f'<div class="gap-bridge-link">→ Repair Link: {gap_loc}</div>'

    return f"""
<div class="gap-card">
  <div class="gap-title">Reasoning Gap Detected — Depth {depth}</div>
  <div class="gap-body">{gap_desc}</div>
  {bridge_link}
</div>
"""


def render_bridge_html(bridge: dict) -> str:
    """Renders a bridge lesson card."""
    title = bridge.get("bridge_title", "Bridge Lesson")
    intro = bridge.get("bridge_intro", "")
    explanation = bridge.get("core_explanation", "")
    analogy = bridge.get("analogy", "")
    practice = bridge.get("practice", [])

    explanation_html = _render_bold(explanation)

    practice_html = ""
    level_colors = {"Easy": "var(--green)", "Medium": "var(--amber)", "Hard": "var(--red)"}
    for p in practice:
        level = p.get("level", "")
        question = p.get("question", "")
        hint = p.get("answer_hint", "")
        color = level_colors.get(level, "var(--text2)")
        practice_html += f"""
<div style="margin-bottom:10px;padding:10px;background:var(--glass2);border-radius:8px;border:1px solid var(--border)">
  <div style="font-size:10px;font-weight:700;color:{color};font-family:'Syne',sans-serif;
              text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px">{level}</div>
  <div style="font-size:13px;color:var(--text);font-family:'DM Sans',sans-serif;line-height:1.6">{question}</div>
  <div style="font-size:11px;color:var(--text3);font-style:italic;margin-top:4px">{hint}</div>
</div>"""

    analogy_html = ""
    if analogy:
        analogy_html = f"""
<div style="background:rgba(255,179,71,.06);border:1px solid rgba(255,179,71,.2);
            border-radius:10px;padding:10px 12px;margin:10px 0">
  <div style="font-size:10px;font-weight:700;color:var(--amber);font-family:'Syne',sans-serif;
              text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px">Analogy</div>
  <div style="font-size:13px;color:var(--text2);font-family:'DM Sans',sans-serif;
              line-height:1.6;font-style:italic">{analogy}</div>
</div>"""

    return f"""
<div class="bridge-card">
  <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
              text-transform:uppercase;color:var(--green);letter-spacing:.04em;margin-bottom:8px">
    Bridge Lesson
  </div>
  <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:700;
              color:var(--text);margin-bottom:6px">{title}</div>
  <div style="font-size:13px;color:var(--text2);font-style:italic;
              margin-bottom:12px;line-height:1.6">{intro}</div>
  <div style="font-size:14px;color:var(--text);line-height:1.75;
              font-family:'DM Sans',sans-serif;margin-bottom:12px">{explanation_html}</div>
  {analogy_html}
  {'<div style="margin-top:12px"><div style="font-size:12px;font-weight:500;color:var(--text2);margin-bottom:8px;font-family:\'DM Sans\',sans-serif">Practice Questions</div>' + practice_html + '</div>' if practice else ''}
</div>
"""


# ── HELPERS ───────────────────────────────────────────────────────────────────

def _render_bold(text: str) -> str:
    """Convert **bold** markdown to accent-colored spans."""
    return re.sub(
        r'\*\*(.+?)\*\*',
        r'<span class="q-key">\1</span>',
        text
    )


def _safe_json(raw: str) -> dict:
    """Extract JSON from Claude's response safely."""
    # Strip markdown code blocks if present
    raw = raw.strip()
    raw = re.sub(r'^```json\s*', '', raw)
    raw = re.sub(r'^```\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    raw = raw.strip()

    # Find JSON object
    start = raw.find('{')
    end = raw.rfind('}')
    if start != -1 and end != -1:
        raw = raw[start:end + 1]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def _fallback_question(subject: str, topics: list[str], depth: int) -> dict:
    topic = topics[0] if topics else subject
    return {
        "q_intro": "Let's explore your understanding of this concept.",
        "q_number": f"Q {depth:02d}",
        "q_topic": topic,
        "q_text": f"Can you explain in your own words what you understand about **{topic}** and why it works the way it does?",
        "q_needs_figure": False,
        "q_figure_type": "none",
        "q_figure_params": {},
        "q_hint": None,
        "gap_detected": False,
        "gap_description": "",
        "gap_location": "",
        "depth_level": depth,
        "reasoning_style_signal": "unclear",
        "confidence": 0.5,
    }
