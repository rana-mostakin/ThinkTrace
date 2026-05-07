# Author: rana-mostakin
"""
ThinkTrace v1 — Adaptive Engine
4-layer adaptation: reasoning style, depth calibration, cross-subject linking, spaced repetition.
"""

from typing import Optional
from collections import Counter
from auth.db import (
    get_user_sessions, get_knowledge_graph, upsert_graph_node,
    upsert_graph_edge, upsert_schedule, get_due_reviews
)


# ── L1: REASONING STYLE CLASSIFIER ───────────────────────────────────────────

STYLE_LABELS = {
    "analytical":  "Analytical",
    "visual":      "Visual",
    "procedural":  "Procedural",
    "analogical":  "Analogical",
    "unclear":     "Developing",
}

STYLE_DESCRIPTIONS = {
    "analytical":  "Prefers logical, systematic step-by-step reasoning",
    "visual":      "Builds understanding through spatial and diagrammatic thinking",
    "procedural":  "Follows established procedures and algorithms",
    "analogical":  "Connects new concepts to familiar real-world analogies",
    "unclear":     "Reasoning pattern still emerging",
}

STYLE_QUESTION_FRAMINGS = {
    "analytical":  "Consider the logical chain: if A causes B, and B causes C, then what must be true about...",
    "visual":      "Imagine you could draw a diagram of this process. What would the arrows between...",
    "procedural":  "Walk me through the exact sequence of steps. At which specific step does...",
    "analogical":  "Think of a real-world system that behaves similarly. Why does this analogy break down at...",
    "unclear":     "In your own words, explain the causal relationship between...",
}


def detect_reasoning_style(sessions: list[dict]) -> str:
    """
    After 3+ sessions, classify dominant reasoning style from signals.
    Returns style key.
    """
    if len(sessions) < 3:
        return "unclear"

    style_votes = []
    for session in sessions:
        for msg in session.get("messages", []):
            if msg.get("role") == "assistant":
                signal = msg.get("meta", {}).get("reasoning_style_signal", "unclear")
                if signal != "unclear":
                    style_votes.append(signal)

    if not style_votes:
        return "unclear"

    counter = Counter(style_votes)
    dominant, count = counter.most_common(1)[0]
    # Need at least 30% dominance
    if count / len(style_votes) >= 0.3:
        return dominant
    return "unclear"


def get_user_reasoning_style(user_id: int) -> str:
    sessions = get_user_sessions(user_id, limit=10)
    return detect_reasoning_style(sessions)


def get_style_framing(style: str) -> str:
    return STYLE_QUESTION_FRAMINGS.get(style, STYLE_QUESTION_FRAMINGS["unclear"])


# ── L2: DEPTH CALIBRATOR ──────────────────────────────────────────────────────

def should_continue_depth(current_depth: int, gap_detected: bool, max_depth: int = 5) -> bool:
    """Returns True if we should go deeper."""
    if gap_detected:
        return False
    return current_depth < max_depth


def get_depth_label(depth: int) -> str:
    labels = {
        1: "Surface Understanding",
        2: "Conceptual Recall",
        3: "Causal Mechanism",
        4: "Underlying Principles",
        5: "Foundational Structure",
    }
    return labels.get(depth, f"Depth {depth}")


# ── L3: KNOWLEDGE GRAPH UPDATER ──────────────────────────────────────────────

def process_session_for_graph(user_id: int, session: dict, q_result: dict):
    """
    After each question exchange, update knowledge graph and schedule.
    """
    subject = session.get("subject", "")
    topics = session.get("topics", [])
    gap_detected = q_result.get("gap_detected", False)
    gap_location = q_result.get("gap_location", "")
    depth = q_result.get("depth_level", 1)

    # Update topic nodes
    for topic in topics:
        strength_delta = 0.05 if not gap_detected else -0.05
        upsert_graph_node(
            user_id, topic, subject,
            strength_delta=strength_delta,
            is_gap=False,
        )

    # Update gap node if detected
    if gap_detected and gap_location:
        parts = gap_location.split("->")
        if len(parts) == 2:
            source = parts[0].strip()
            target = parts[1].strip()
            upsert_graph_node(user_id, source, subject, is_gap=False)
            upsert_graph_node(user_id, target, subject, is_gap=True)
            upsert_graph_edge(user_id, source, target, broken=True)

            # Schedule for spaced repetition
            gap_desc = q_result.get("gap_description", "")
            upsert_schedule(
                user_id, concept=target, subject=subject,
                strength=0.2, is_gap=True,
            )


def repair_gap_in_graph(user_id: int, concept: str, subject: str):
    """Call this when a student completes a bridge lesson."""
    upsert_graph_node(user_id, concept, subject, strength_delta=0.25, is_gap=False)
    upsert_schedule(user_id, concept=concept, subject=subject,
                    strength=0.6, is_gap=False)

    # Try to repair any broken edges pointing to this concept
    graph = get_knowledge_graph(user_id)
    for edge in graph.get("edges", []):
        if edge["target"] == concept:
            edge["broken"] = False
    from auth.db import update_knowledge_graph
    update_knowledge_graph(user_id, graph)


# ── L4: CROSS-SUBJECT LINKER ──────────────────────────────────────────────────

def find_cross_subject_links(user_id: int) -> list[dict]:
    """
    Detect when the same gap_location appears across multiple subjects.
    Returns list of cross-subject link dicts.
    """
    sessions = get_user_sessions(user_id, limit=50)

    # Collect gap locations per subject
    gap_by_location: dict[str, set] = {}
    gap_descriptions: dict[str, list] = {}

    for session in sessions:
        subject = session.get("subject", "")
        for gap in session.get("gaps", []):
            loc = gap.get("location", "")
            desc = gap.get("description", "")
            if loc:
                gap_by_location.setdefault(loc, set()).add(subject)
                gap_descriptions.setdefault(loc, []).append((subject, desc))

    # Find locations that appear in 2+ subjects
    cross_links = []
    for location, subjects in gap_by_location.items():
        if len(subjects) >= 2:
            examples = gap_descriptions.get(location, [])
            cross_links.append({
                "location": location,
                "subjects": list(subjects),
                "insight": f"This causal link ({location}) is broken across {', '.join(subjects)}. "
                           f"This suggests a foundational concept gap that spans subjects.",
                "examples": examples[:2],
            })

    return cross_links


# ── REASONING PROFILE ────────────────────────────────────────────────────────

def compute_reasoning_profile(user_id: int) -> dict[str, float]:
    """
    Returns proficiency 0.0-1.0 for each reasoning dimension.
    Based on session history.
    """
    sessions = get_user_sessions(user_id, limit=20)

    dimensions = {
        "Analytical":  [],
        "Visual":      [],
        "Procedural":  [],
        "Analogical":  [],
    }

    style_to_dim = {
        "analytical": "Analytical",
        "visual":     "Visual",
        "procedural": "Procedural",
        "analogical": "Analogical",
    }

    for session in sessions:
        style = session.get("style", "unclear")
        gaps = session.get("gaps", [])
        depth = session.get("depth_reached", 1)

        dim = style_to_dim.get(style)
        if dim:
            # Higher depth with fewer gaps = higher proficiency
            score = (depth / 5.0) * (1.0 - min(len(gaps) * 0.1, 0.5))
            dimensions[dim].append(score)

    profile = {}
    for dim, scores in dimensions.items():
        if scores:
            profile[dim] = min(1.0, sum(scores) / len(scores) + 0.1)
        else:
            profile[dim] = 0.2  # baseline

    return profile


# ── SESSION-LEVEL TRACKING ────────────────────────────────────────────────────

def update_session_style(session_messages: list[dict]) -> str:
    """Detect dominant style from a single session's messages."""
    styles = []
    for msg in session_messages:
        if msg.get("role") == "assistant":
            signal = msg.get("meta", {}).get("reasoning_style_signal", "unclear")
            if signal != "unclear":
                styles.append(signal)

    if not styles:
        return "unclear"

    counter = Counter(styles)
    return counter.most_common(1)[0][0]
