# Author: rana-mostakin
"""
ThinkTrace v1 — Hybrid Question Engine
Cost architecture: question_bank.py handles depth 1-2 (zero API cost).
Claude API is called ONLY from depth 3 onward, or when bank has no entry.

Cost breakdown per session:
  Depth 1-2  → 0 API calls (served from local bank)
  Depth 3    → 1 API call
  Depth 4    → 1 API call
  Depth 5    → 1 API call
  Bridge     → 1 API call (only if gap found)
  Maximum:   → 4 API calls per full session (vs 6+ before)

For uploads: 1 API call per question analyzed (Claude vision if image).
"""

import random
import os
import json
import re
import anthropic

# Import the pre-built bank
try:
    from data.question_bank import BANK
except ImportError:
    BANK = {}

# ── PUBLIC API ─────────────────────────────────────────────────────────────────

def get_question(
    subject: str,
    topics: list[str],
    depth: int,
    conversation: list[dict],
    language: str,
    reasoning_style: str = "unclear",
) -> dict:
    """
    Main entry point. Returns a question dict matching the socratic JSON schema.
    Depth 1-2: served from bank (zero API cost).
    Depth 3+:  Claude API call.
    Falls back to Claude if bank has no entry for the topic.
    """
    if depth <= 2:
        banked = _from_bank(subject, topics, depth)
        if banked:
            _localize(banked, language)
            return banked

    # Depth 3+ or bank miss → Claude
    return _from_claude(subject, topics, depth, conversation, language, reasoning_style)


def get_initial_question(subject: str, topics: list[str], language: str) -> dict:
    """
    Opening question (depth 1) — always served from bank.
    Zero API cost.
    """
    banked = _from_bank(subject, topics, 1)
    if banked:
        _localize(banked, language)
        banked["q_number"] = "Q 01"
        return banked
    # Very unlikely fallback
    return _from_claude(subject, topics, 1, [], language, "unclear")


# ── BANK LOOKUP ───────────────────────────────────────────────────────────────

def _from_bank(subject: str, topics: list[str], depth: int) -> dict | None:
    """
    Look up a question from the pre-built bank.
    Tries topics in order, picks a random question if multiple exist.
    Returns None if no match found.
    """
    subj_bank = BANK.get(subject, {})
    if not subj_bank:
        return None

    # Try each selected topic in random order (variety between sessions)
    shuffled = list(topics)
    random.shuffle(shuffled)

    for topic in shuffled:
        topic_bank = subj_bank.get(topic, {})
        depth_qs = topic_bank.get(depth, [])
        if depth_qs:
            q = dict(random.choice(depth_qs))  # copy so we don't mutate bank
            q["q_number"] = f"Q {depth:02d}"
            q["depth_level"] = depth
            q["gap_detected"] = False
            q["gap_description"] = ""
            q["gap_location"] = ""
            if "confidence" not in q:
                q["confidence"] = 0.75
            if "reasoning_style_signal" not in q:
                q["reasoning_style_signal"] = "unclear"
            return q

    return None


# ── CLAUDE FALLBACK (depth 3+) ────────────────────────────────────────────────

_SYSTEM = """You are a Socratic reasoning diagnostician embedded in ThinkTrace.
Your sole purpose: find the EXACT broken causal link in the student's reasoning chain.

RULES:
- Do NOT teach. Do NOT correct. Ask ONE question one causal level deeper than the previous.
- Never reveal the answer. Find causal gaps, not calculation errors.
- Wrong calculation → neutral. Missing causal link → mark gap_detected true.
- Adapt framing to detected reasoning style: {style}
- All text in: {language}. Keep math notation international.

Respond ONLY in valid JSON. No preamble, no markdown.

{{
  "q_intro": "warm 1-sentence setup (NOT the question — italic floating text)",
  "q_number": "Q {qnum:02d}",
  "q_topic": "2-4 word descriptor",
  "q_text": "the Socratic question with **bold** key causal terms",
  "q_needs_figure": false,
  "q_figure_type": "none",
  "q_figure_params": {{}},
  "q_hint": null,
  "gap_detected": false,
  "gap_description": "",
  "gap_location": "",
  "depth_level": {depth},
  "reasoning_style_signal": "unclear",
  "confidence": 0.85
}}

q_figure_type options: force_diagram, velocity_diagram, molecular, graph_curve,
                       process_flow, rocket_diagram, circuit_diagram, none
reasoning_style_signal: analytical, visual, procedural, analogical, unclear
gap_location format: "ConceptA -> ConceptB"
"""


def _from_claude(
    subject: str,
    topics: list[str],
    depth: int,
    conversation: list[dict],
    language: str,
    style: str,
) -> dict:
    """Call Claude API for depth 3+ questions."""
    try:
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
        system = _SYSTEM.format(
            style=style, language=language, depth=depth, qnum=depth
        )

        messages = []
        for msg in conversation:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})

        ctx = (
            f"\n\n[CONTEXT: Subject={subject}, Topics={', '.join(topics)}, "
            f"Current depth={depth}, Max depth=5, Language={language}]"
        )
        if messages and messages[-1]["role"] == "user":
            messages[-1]["content"] += ctx
        else:
            messages.append({"role": "user", "content": ctx})

        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=900,
            system=system,
            messages=messages,
        )
        raw = resp.content[0].text
        raw = re.sub(r"```json|```", "", raw).strip()
        s = raw.find("{"); e = raw.rfind("}")
        if s != -1 and e != -1:
            raw = raw[s:e+1]
        data = json.loads(raw)
        data["depth_level"] = depth
        data["q_number"] = f"Q {depth:02d}"
        return data
    except Exception:
        return _fallback(subject, topics, depth)


# ── LANGUAGE NOTE ─────────────────────────────────────────────────────────────

def _localize(q: dict, language: str) -> None:
    """
    For non-English sessions, add a language note to the question.
    The bank questions are written in English.
    A real implementation would use a translation cache.
    Here we append a note so the student knows they can answer in their language.
    """
    if language and language.lower() not in ("english", "en"):
        note = f" (You may answer in {language}.)"
        if not q.get("q_text", "").endswith(note):
            q["q_text"] = q.get("q_text", "") + note


# ── FALLBACK ──────────────────────────────────────────────────────────────────

def _fallback(subject: str, topics: list[str], depth: int) -> dict:
    topic = topics[0] if topics else subject
    return {
        "q_intro": "Let's continue probing your understanding.",
        "q_number": f"Q {depth:02d}",
        "q_topic": topic,
        "q_text": (
            f"In your own words, explain **why** the concept of **{topic}** "
            f"works the way it does — not just what the formula says, but what causes it."
        ),
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


# ── COST TRACKER ──────────────────────────────────────────────────────────────

def estimate_session_cost(depth_reached: int, gap_found: bool, upload_qs: int = 0) -> dict:
    """
    Rough cost estimate for a session.
    Claude Sonnet 4: ~$3 / 1M input tokens, ~$15 / 1M output tokens.
    Avg tokens per question call: ~600 input + ~200 output.
    """
    claude_calls = max(0, depth_reached - 2)  # bank handles depth 1-2
    if gap_found:
        claude_calls += 1  # bridge lesson
    claude_calls += upload_qs  # one call per uploaded question analyzed

    input_tokens = claude_calls * 600
    output_tokens = claude_calls * 200
    cost_usd = (input_tokens / 1_000_000 * 3.0) + (output_tokens / 1_000_000 * 15.0)

    return {
        "claude_calls": claude_calls,
        "bank_calls": min(depth_reached, 2),
        "estimated_cost_usd": round(cost_usd, 4),
        "estimated_cost_cents": round(cost_usd * 100, 2),
    }


# ── QUESTION BANK GROWTH GUIDE ────────────────────────────────────────────────
# To extend the bank without API cost:
#
# 1. Open data/question_bank.py
# 2. Find BANK["Subject"]["Topic"]
# 3. Add new question dicts to depth 1 or 2 lists
# 4. Each dict must match this schema:
#    {
#      "q_intro":       str,   # warm 1-sentence setup
#      "q_topic":       str,   # 2-4 word descriptor
#      "q_text":        str,   # the question (use **bold** for key terms)
#      "q_needs_figure": bool,
#      "q_figure_type": str,   # "none" or figure type
#      "q_figure_params": dict,
#      "q_hint":        str | None,
#      "gap_detected":  False, # always False in bank
#      "gap_description": "",
#      "gap_location":  "",
#      "reasoning_style_signal": str,
#      "confidence":    float,
#    }
#
# 5. No API calls needed. Bank questions are served instantly.
# 6. To add a new subject or topic: add a new key to BANK dict.
