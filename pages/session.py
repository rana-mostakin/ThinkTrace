# Author: rana-mostakin
"""
ThinkTrace v1 — Session Page
Premium two-part Socratic chat UI with live context panel.
Layout: 70% chat / 30% context panel
"""

import streamlit as st
import json
from datetime import datetime

from data.subjects import SUBJECTS, validate_topics, SUBJECT_COLORS
from engine.socratic import (
    generate_initial_question, generate_next_question,
    render_question_html, render_gap_html, render_bridge_html,
    generate_bridge,
)
from engine.adaptive import (
    process_session_for_graph, get_user_reasoning_style,
    should_continue_depth, get_depth_label, update_session_style,
    STYLE_LABELS, STYLE_DESCRIPTIONS,
)
from auth.db import (
    create_session, update_session, get_session, get_user
)
from utils.styles import depth_pips, skeleton_loading


# ── SESSION SETUP PAGE ────────────────────────────────────────────────────────

def show_session_setup():
    """Subject & topic selection before starting a session."""
    user = st.session_state.get("user", {})

    st.markdown("""
    <div style="margin-bottom:1.5rem">
      <div class="tt-h2">New Session</div>
      <div style="font-size:13px;color:var(--text2);font-family:'DM Sans',sans-serif;
                  margin-top:4px">Choose a subject and at least 3 topics to begin Socratic diagnosis.</div>
    </div>
    """, unsafe_allow_html=True)

    # Subject picker
    subjects = list(SUBJECTS.keys())
    selected_subject = st.session_state.get("setup_subject", subjects[0])

    st.markdown('<div class="glass-card gc-accent" style="margin-bottom:1rem">', unsafe_allow_html=True)
    st.markdown('<div class="tt-label" style="margin-bottom:0.75rem">Subject</div>', unsafe_allow_html=True)

    # Subject pills
    pill_html = '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:0">'
    for subj in subjects:
        color = SUBJECT_COLORS.get(subj, "var(--accent)")
        active = "active" if subj == selected_subject else ""
        pill_html += f"""
        <span class="btn-pill {active}" style="cursor:pointer;
          {'background:rgba(124,111,255,.12);border-color:rgba(124,111,255,.4);color:var(--accent2)' if active else ''}">
          {subj}
        </span>"""
    pill_html += "</div>"
    st.markdown(pill_html, unsafe_allow_html=True)

    new_subject = st.selectbox(
        "Select Subject",
        subjects,
        index=subjects.index(selected_subject),
        key="setup_subject_select",
        label_visibility="collapsed",
    )
    if new_subject != st.session_state.get("setup_subject"):
        st.session_state["setup_subject"] = new_subject
        st.session_state.pop("setup_topics", None)
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Topic picker
    topics_for_subject = SUBJECTS.get(new_subject, [])
    selected_topics = st.session_state.get("setup_topics", [])

    st.markdown('<div class="glass-card" style="margin-bottom:1rem">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tt-label" style="margin-bottom:0.75rem">Topics — {new_subject}</div>',
        unsafe_allow_html=True,
    )

    chosen_topics = st.multiselect(
        "Select topics (minimum 3)",
        topics_for_subject,
        default=[t for t in selected_topics if t in topics_for_subject],
        key="setup_topics_select",
        label_visibility="collapsed",
    )
    st.session_state["setup_topics"] = chosen_topics

    is_valid, feedback = validate_topics(chosen_topics)

    fb_color = "var(--green)" if is_valid else "var(--amber)"
    st.markdown(
        f'<div style="font-size:12px;color:{fb_color};font-family:\'DM Sans\',sans-serif;'
        f'margin-top:6px">{feedback}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Language display
    language = user.get("language", "English")
    st.markdown(
        f'<div style="margin-bottom:1rem">'
        f'<span class="lang-badge">Session language: {language}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Start button
    if is_valid:
        if st.button("Begin Diagnostic Session →", key="start_session",
                     use_container_width=True):
            _start_session(user, new_subject, chosen_topics, language)
    else:
        st.markdown(
            '<div style="opacity:0.5;pointer-events:none">', unsafe_allow_html=True
        )
        st.button("Begin Diagnostic Session →", disabled=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


def _start_session(user: dict, subject: str, topics: list, language: str):
    """Initialize a new session in DB and load the chat view."""
    session_id = create_session(user["id"], subject, topics)
    st.session_state["active_session_id"] = session_id
    st.session_state["session_messages"] = []
    st.session_state["session_depth"] = 1
    st.session_state["session_gaps"] = []
    st.session_state["session_style"] = "unclear"
    st.session_state["session_bridge"] = None
    st.session_state["page"] = "session_chat"
    st.rerun()


# ── CHAT PAGE ─────────────────────────────────────────────────────────────────

def show_session_chat():
    """The active Socratic chat session."""
    session_id = st.session_state.get("active_session_id")
    if not session_id:
        st.session_state["page"] = "new_session"
        st.rerun()
        return

    session = get_session(session_id)
    if not session:
        st.error("Session not found.")
        return

    user = st.session_state.get("user", {})
    subject = session["subject"]
    topics = session["topics"]
    language = user.get("language", "English")
    messages = st.session_state.get("session_messages", session["messages"])
    depth = st.session_state.get("session_depth", session["depth_reached"])
    gaps = st.session_state.get("session_gaps", session["gaps"])
    reasoning_style = st.session_state.get("session_style", session["style"])
    bridge_data = st.session_state.get("session_bridge")

    # Layout: 70% chat | 30% context
    chat_col, ctx_col = st.columns([0.70, 0.30], gap="medium")

    with chat_col:
        _render_chat_header(subject, topics, depth)

        # Chat container
        st.markdown('<div class="chat-container" id="chat-scroll">', unsafe_allow_html=True)

        # If no messages yet, generate first question
        if not messages:
            _generate_and_show_first_question(
                subject, topics, language, messages, session_id, depth
            )
        else:
            _render_all_messages(messages)

        st.markdown('</div>', unsafe_allow_html=True)

        # Bridge card if gap found
        if bridge_data:
            st.markdown(render_bridge_html(bridge_data), unsafe_allow_html=True)

        # Answer input
        _render_answer_input(
            messages, session_id, subject, topics, language,
            depth, gaps, reasoning_style, user
        )

    with ctx_col:
        _render_context_panel(subject, topics, depth, gaps, reasoning_style, bridge_data)


def _render_chat_header(subject: str, topics: list, depth: int):
    topics_preview = ", ".join(topics[:3]) + ("..." if len(topics) > 3 else "")
    st.markdown(f"""
    <div class="session-header">
      <div>
        <div class="session-subject">{subject}</div>
        <div class="session-topic-line">{topics_preview}</div>
      </div>
    </div>
    <hr class="tt-divider">
    """, unsafe_allow_html=True)


def _generate_and_show_first_question(
    subject, topics, language, messages, session_id, depth
):
    """Generate and display the first Socratic question."""
    placeholder = st.empty()

    with placeholder.container():
        st.markdown(
            '<div style="padding:8px 0">'
            '<div class="skeleton skeleton-line long"></div>'
            '<div class="skeleton skeleton-line medium"></div>'
            '<div class="skeleton skeleton-block" style="margin-top:8px"></div>'
            '</div>',
            unsafe_allow_html=True,
        )

    q = generate_initial_question(subject, topics, language)
    placeholder.empty()

    # Render and store
    q_html = render_question_html(q)
    st.markdown(q_html, unsafe_allow_html=True)

    # Store in messages
    msg = {
        "role": "assistant",
        "content": q.get("q_text", ""),
        "html": q_html,
        "meta": q,
        "timestamp": datetime.now().isoformat(),
    }
    messages.append(msg)
    st.session_state["session_messages"] = messages

    update_session(session_id,
                   messages=[{k: v for k, v in m.items() if k != "html"}
                              for m in messages])


def _render_all_messages(messages: list):
    """Render all messages in the chat."""
    for msg in messages:
        if msg["role"] == "assistant":
            html = msg.get("html", "")
            if html:
                st.markdown(html, unsafe_allow_html=True)
            else:
                # Reconstruct from meta
                meta = msg.get("meta", {})
                if meta:
                    st.markdown(render_question_html(meta), unsafe_allow_html=True)
                    if meta.get("gap_detected"):
                        st.markdown(render_gap_html(meta), unsafe_allow_html=True)
        elif msg["role"] == "user":
            content = msg.get("content", "")
            st.markdown(
                f'<div class="msg-user">{content}</div>',
                unsafe_allow_html=True,
            )


def _render_answer_input(
    messages, session_id, subject, topics, language,
    depth, gaps, reasoning_style, user
):
    """Sticky answer input at bottom of chat."""
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<div class="lang-badge" style="margin-bottom:6px">Responding in {language}</div>',
        unsafe_allow_html=True,
    )

    answer = st.text_area(
        "Your answer",
        placeholder=f"Type your reasoning… (Bengali বা English, যেকোনো ভাষায়)",
        height=100,
        key=f"answer_input_{len(messages)}",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        submit = st.button("Submit Response →", key=f"submit_{len(messages)}",
                           use_container_width=True)
    with col2:
        if st.button("End Session", key="end_session"):
            _end_session(session_id, messages, gaps, depth, reasoning_style)
            return

    if submit and answer.strip():
        _process_answer(
            answer.strip(), messages, session_id,
            subject, topics, language, depth, gaps,
            reasoning_style, user,
        )


def _process_answer(
    answer: str, messages: list, session_id: int,
    subject: str, topics: list, language: str,
    depth: int, gaps: list, reasoning_style: str, user: dict,
):
    """Process student's answer and generate next question."""
    # Add user message
    user_msg = {
        "role": "user",
        "content": answer,
        "timestamp": datetime.now().isoformat(),
    }
    messages.append(user_msg)

    # Build Claude conversation history
    claude_messages = []
    for m in messages:
        role = m["role"]
        content = m.get("content", "")
        if role == "assistant" and not content:
            # Use q_text as assistant content
            content = m.get("meta", {}).get("q_text", "")
        if content:
            claude_messages.append({"role": role, "content": content})

    # Generate next question
    new_depth = depth + 1 if depth < 5 else 5
    q = generate_next_question(
        subject=subject,
        topics=topics,
        language=language,
        conversation=claude_messages,
        current_depth=depth,
        reasoning_style=reasoning_style,
    )

    # Render question
    q_html = render_question_html(q)
    gap_html = render_gap_html(q) if q.get("gap_detected") else ""

    # Store assistant message
    ai_msg = {
        "role": "assistant",
        "content": q.get("q_text", ""),
        "html": q_html + gap_html,
        "meta": q,
        "timestamp": datetime.now().isoformat(),
    }
    messages.append(ai_msg)

    # Update depth and style
    new_style = q.get("reasoning_style_signal", reasoning_style)
    if new_style != "unclear":
        reasoning_style = new_style

    # Process gap
    if q.get("gap_detected"):
        gap_info = {
            "location": q.get("gap_location", ""),
            "description": q.get("gap_description", ""),
            "depth": q.get("depth_level", depth),
            "subject": subject,
        }
        gaps.append(gap_info)

        # Generate bridge lesson
        bridge = generate_bridge(
            gap_location=gap_info["location"],
            gap_description=gap_info["description"],
            subject=subject,
            language=language,
        )
        st.session_state["session_bridge"] = bridge

        # Update knowledge graph
        # FIX: Retrieve the session object before using it
        session = get_session(session_id)
        if session:
            process_session_for_graph(user["id"], session, q)

    # Update session state
    st.session_state["session_messages"] = messages
    st.session_state["session_depth"] = new_depth
    st.session_state["session_gaps"] = gaps
    st.session_state["session_style"] = reasoning_style

    # Persist to DB
    update_session(
        session_id,
        messages=[{k: v for k, v in m.items() if k != "html"} for m in messages],
        gaps=gaps,
        depth_reached=new_depth,
        style=reasoning_style,
    )

    st.rerun()


def _render_context_panel(subject, topics, depth, gaps, reasoning_style, bridge_data):
    """Right panel: live session context."""
    st.markdown(
        '<div style="font-family:\'Syne\',sans-serif;font-size:12px;font-weight:700;'
        'color:var(--text2);text-transform:uppercase;letter-spacing:.05em;'
        'margin-bottom:1rem">Live Context</div>',
        unsafe_allow_html=True,
    )

    # Depth indicator
    st.markdown('<div class="glass-card" style="margin-bottom:0.75rem">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tt-label" style="margin-bottom:8px">Diagnostic Depth</div>',
        unsafe_allow_html=True,
    )
    has_gap = len(gaps) > 0
    st.markdown(depth_pips(depth, has_gap=has_gap), unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-size:11px;color:var(--text3);margin-top:6px;'
        f'font-family:\'DM Sans\',sans-serif">{_get_depth_label(depth)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Topics status
    st.markdown('<div class="glass-card" style="margin-bottom:0.75rem">', unsafe_allow_html=True)
    st.markdown(
        '<div class="tt-label" style="margin-bottom:8px">Topics</div>',
        unsafe_allow_html=True,
    )
    tags_html = ""
    for topic in topics:
        tags_html += f'<span class="topic-tag probing">{topic}</span>'
    st.markdown(f'<div style="display:flex;flex-wrap:wrap">{tags_html}</div>',
                unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Reasoning style
    from engine.adaptive import STYLE_LABELS, STYLE_DESCRIPTIONS
    style_label = STYLE_LABELS.get(reasoning_style, "Developing")
    style_desc = STYLE_DESCRIPTIONS.get(reasoning_style, "")
    st.markdown('<div class="glass-card" style="margin-bottom:0.75rem">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="tt-label" style="margin-bottom:6px">Reasoning Style</div>'
        f'<div style="font-family:\'Syne\',sans-serif;font-size:13px;font-weight:700;'
        f'color:var(--accent2)">{style_label}</div>'
        f'<div style="font-size:11px;color:var(--text3);margin-top:3px;'
        f'font-family:\'DM Sans\',sans-serif;line-height:1.5">{style_desc}</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Gaps detected
    if gaps:
        st.markdown('<div class="gap-card" style="margin-bottom:0.75rem">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="gap-title">{len(gaps)} Gap{"s" if len(gaps) > 1 else ""} Found</div>',
            unsafe_allow_html=True,
        )
        for g in gaps:
            loc = g.get("location", "")
            if loc:
                st.markdown(
                    f'<div style="font-size:11px;color:#ffaaaa;font-family:\'JetBrains Mono\',monospace;'
                    f'margin:3px 0">{loc}</div>',
                    unsafe_allow_html=True,
                )
        st.markdown('</div>', unsafe_allow_html=True)


def _get_depth_label(depth: int) -> str:
    labels = {
        1: "Surface Understanding",
        2: "Conceptual Recall",
        3: "Causal Mechanism",
        4: "Underlying Principles",
        5: "Foundational Structure",
    }
    return labels.get(depth, f"Depth {depth}")


def _end_session(session_id, messages, gaps, depth, style):
    """Finalize and save the session."""
    update_session(
        session_id,
        messages=[{k: v for k, v in m.items() if k != "html"} for m in messages],
        gaps=gaps,
        depth_reached=depth,
        style=style,
    )
    # Clear session state
    for key in ["active_session_id", "session_messages", "session_depth",
                "session_gaps", "session_style", "session_bridge"]:
        st.session_state.pop(key, None)

    st.session_state["page"] = "dashboard"
    st.rerun()


# ── IMPORT FIX ────────────────────────────────────────────────────────────────
# Need get_session locally for process_session_for_graph
_session_cache = {}

def session(session_id: int) -> dict:
    if session_id not in _session_cache:
        from auth.db import get_session as _get
        _session_cache[session_id] = _get(session_id) or {}
    return _session_cache[session_id]
