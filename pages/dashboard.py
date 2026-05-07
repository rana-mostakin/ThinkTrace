# Author: rana-mostakin
"""
ThinkTrace v1 — Dashboard Page
Stats, activity chart, reasoning profile bars, spaced repetition schedule, recent sessions.
"""

import streamlit as st
from datetime import datetime, timedelta

from auth.db import get_user_stats, get_user_sessions, get_due_reviews
from utils.graph_builder import build_activity_chart
from utils.styles import profile_bar
from engine.adaptive import compute_reasoning_profile, find_cross_subject_links
from data.subjects import SUBJECT_COLORS


def show_dashboard():
    user = st.session_state.get("user", {})
    name = user.get("name", "Student")
    user_id = user.get("id")

    # Welcome header
    st.markdown(f"""
    <div style="margin-bottom:1.75rem">
      <div class="tt-h1">Welcome back, {name}.</div>
      <div style="font-size:13px;color:var(--text2);font-family:'DM Sans',sans-serif;
                  margin-top:5px;font-weight:300">
        {datetime.now().strftime("%A, %B %d")} — Your cognitive laboratory is ready.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── STAT CARDS ────────────────────────────────────────────────────────────
    stats = get_user_stats(user_id)
    sessions_list = get_user_sessions(user_id, limit=50)

    stat_items = [
        {
            "value": stats["sessions"],
            "label": "Sessions",
            "delta": "+1 today" if stats["sessions"] > 0 else "Start your first",
            "delta_type": "pos" if stats["sessions"] > 0 else "neu",
            "variant": "gc-accent",
            "color": "var(--accent)",
        },
        {
            "value": stats["gaps_found"],
            "label": "Gaps Found",
            "delta": "Reasoning gaps identified",
            "delta_type": "neu",
            "variant": "gc-red",
            "color": "var(--red)",
        },
        {
            "value": stats["gaps_repaired"],
            "label": "Gaps Repaired",
            "delta": f"{int(stats['gaps_repaired'] / max(stats['gaps_found'], 1) * 100)}% repair rate" if stats["gaps_found"] > 0 else "Complete bridge lessons",
            "delta_type": "pos" if stats["gaps_repaired"] > 0 else "neu",
            "variant": "gc-green",
            "color": "var(--green)",
        },
        {
            "value": stats["cross_links"],
            "label": "Cross-Subject Links",
            "delta": "Patterns across subjects",
            "delta_type": "neu",
            "variant": "gc-teal",
            "color": "var(--teal)",
        },
    ]

    cols = st.columns(4, gap="small")
    for col, item in zip(cols, stat_items):
        with col:
            st.markdown(f"""
            <div class="stat-card {item['variant']}">
              <div style="width:3px;height:24px;background:{item['color']};
                          border-radius:2px;margin-bottom:10px"></div>
              <div class="stat-value">{item['value']}</div>
              <div class="stat-label">{item['label']}</div>
              <div class="stat-delta delta-{item['delta_type']}">{item['delta']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── MIDDLE ROW: Chart + Reasoning Profile ─────────────────────────────────
    chart_col, profile_col = st.columns([1.5, 1], gap="medium")

    with chart_col:
        st.markdown('<div class="glass-card gc-accent">', unsafe_allow_html=True)
        st.markdown(
            '<div class="tt-h3" style="margin-bottom:1rem">Session Activity</div>',
            unsafe_allow_html=True,
        )
        fig = build_activity_chart(sessions_list)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with profile_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="tt-h3" style="margin-bottom:4px">Reasoning Profile</div>'
            '<div style="font-size:11px;color:var(--text3);font-family:\'DM Sans\',sans-serif;'
            'margin-bottom:1rem">Adaptive analysis across sessions</div>',
            unsafe_allow_html=True,
        )

        profile = compute_reasoning_profile(user_id)
        bar_colors = {
            "Analytical":  "linear-gradient(90deg,#7c6fff,#a78bfa)",
            "Visual":      "linear-gradient(90deg,#22d4c0,#60a5fa)",
            "Procedural":  "linear-gradient(90deg,#ffb347,#f472b6)",
            "Analogical":  "linear-gradient(90deg,#22d47a,#22d4c0)",
        }

        profile_html = ""
        for dim, score in profile.items():
            pct = int(score * 100)
            color_grad = bar_colors.get(dim, "linear-gradient(90deg,var(--accent),var(--teal))")
            profile_html += f"""
            <div class="profile-bar-wrap">
              <div class="profile-bar-label">
                <span>{dim}</span>
                <span style="color:var(--text2)">{pct}%</span>
              </div>
              <div class="profile-bar-track">
                <div class="profile-bar-fill" style="width:{pct}%;background:{color_grad}"></div>
              </div>
            </div>"""

        st.markdown(profile_html, unsafe_allow_html=True)

        # Dominant style badge
        dominant = max(profile, key=profile.get)
        st.markdown(
            f'<div style="margin-top:1rem;padding:8px 12px;'
            f'background:rgba(124,111,255,.08);border:1px solid rgba(124,111,255,.18);'
            f'border-radius:8px">'
            f'<div style="font-size:10px;color:var(--text3);font-family:\'DM Sans\',sans-serif;'
            f'margin-bottom:3px">Dominant Style</div>'
            f'<div style="font-family:\'Syne\',sans-serif;font-size:14px;font-weight:700;'
            f'color:var(--accent2)">{dominant}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── BOTTOM ROW: Due Reviews + Recent Sessions ──────────────────────────────
    reviews_col, recent_col = st.columns([1, 1], gap="medium")

    with reviews_col:
        _render_due_reviews(user_id)

    with recent_col:
        _render_recent_sessions(sessions_list)

    # ── CROSS-SUBJECT LINKS ───────────────────────────────────────────────────
    cross_links = find_cross_subject_links(user_id)
    if cross_links:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="tt-h3" style="margin-bottom:0.75rem">Cross-Subject Patterns</div>',
                    unsafe_allow_html=True)
        for link in cross_links[:3]:
            subjects_str = " & ".join(link["subjects"])
            st.markdown(f"""
            <div class="cross-link">
              <div class="cross-link-title">Cross-Subject Gap</div>
              <div style="font-family:'DM Sans',sans-serif;font-size:13px;color:var(--text);
                          margin:4px 0">
                <span style="font-family:'JetBrains Mono',monospace;font-size:12px;
                             color:var(--pink)">{link['location']}</span>
                &nbsp;·&nbsp;
                <span style="color:var(--text2)">{subjects_str}</span>
              </div>
              <div style="font-size:12px;color:var(--text2);font-family:'DM Sans',sans-serif;
                          line-height:1.5;margin-top:3px">{link['insight'][:160]}...</div>
            </div>
            """, unsafe_allow_html=True)


def _render_due_reviews(user_id: int):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="tt-h3" style="margin-bottom:0.25rem">Today\'s Reviews</div>'
        '<div style="font-size:11px;color:var(--text3);font-family:\'DM Sans\',sans-serif;'
        'margin-bottom:0.75rem">Spaced repetition queue</div>',
        unsafe_allow_html=True,
    )

    due = get_due_reviews(user_id, limit=6)
    today = datetime.now().strftime("%Y-%m-%d")

    if not due:
        st.markdown(
            '<div style="font-size:13px;color:var(--text3);font-family:\'DM Sans\',sans-serif;'
            'padding:12px 0">No reviews due today. Complete a session to build your schedule.</div>',
            unsafe_allow_html=True,
        )
    else:
        for item in due:
            next_r = item.get("next_review", today)
            if next_r < today:
                due_cls = "overdue"
                due_label = "Overdue"
            elif next_r == today:
                due_cls = "today"
                due_label = "Today"
            else:
                days = (datetime.strptime(next_r, "%Y-%m-%d") -
                        datetime.now()).days
                due_cls = "future"
                due_label = f"In {days}d"

            subj_color = SUBJECT_COLORS.get(item.get("subject", ""), "var(--text2)")
            strength = item.get("strength", 0.5)
            str_pct = int(strength * 100)

            st.markdown(f"""
            <div class="review-row">
              <div>
                <div class="review-concept">{item['concept']}</div>
                <div class="review-subject" style="color:{subj_color}">{item['subject']}</div>
              </div>
              <div style="display:flex;align-items:center;gap:10px">
                <div style="text-align:right">
                  <div class="review-due {due_cls}">{due_label}</div>
                  <div style="font-size:10px;color:var(--text3)">str {str_pct}%</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def _render_recent_sessions(sessions_list: list):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="tt-h3" style="margin-bottom:0.75rem">Recent Sessions</div>',
        unsafe_allow_html=True,
    )

    if not sessions_list:
        st.markdown(
            '<div style="font-size:13px;color:var(--text3);font-family:\'DM Sans\',sans-serif;'
            'padding:12px 0">No sessions yet. Start your first diagnostic session.</div>',
            unsafe_allow_html=True,
        )
        if st.button("Start First Session →", key="dash_start_session"):
            st.session_state["page"] = "new_session"
            st.rerun()
    else:
        for s in sessions_list[:5]:
            topics = s.get("topics", [])
            gaps = s.get("gaps", [])
            depth = s.get("depth_reached", 1)
            subj_color = SUBJECT_COLORS.get(s.get("subject", ""), "var(--accent)")
            created = s.get("created_at", "")[:10]

            gap_badge = ""
            if gaps:
                gap_badge = (f'<span style="font-size:10px;color:var(--red);'
                             f'background:rgba(255,85,85,.1);border:1px solid rgba(255,85,85,.2);'
                             f'border-radius:4px;padding:1px 6px;margin-left:6px">'
                             f'{len(gaps)} gap{"s" if len(gaps) > 1 else ""}</span>')
            else:
                gap_badge = (f'<span style="font-size:10px;color:var(--green);'
                             f'background:rgba(34,212,122,.1);border:1px solid rgba(34,212,122,.2);'
                             f'border-radius:4px;padding:1px 6px;margin-left:6px">clean</span>')

            topics_preview = ", ".join(topics[:2]) + ("…" if len(topics) > 2 else "")

            st.markdown(f"""
            <div style="padding:10px 0;border-bottom:1px solid var(--border)">
              <div style="display:flex;align-items:center;justify-content:space-between">
                <div>
                  <div style="display:flex;align-items:center">
                    <span style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
                                 color:{subj_color}">{s.get('subject','')}</span>
                    {gap_badge}
                  </div>
                  <div style="font-size:11px;color:var(--text3);
                              font-family:'DM Sans',sans-serif;margin-top:2px">
                    {topics_preview} · Depth {depth}
                  </div>
                </div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
                            color:var(--text3)">{created}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
