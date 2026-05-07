# Author: rana-mostakin
"""
ThinkTrace v1 — Insights Page
Deep analysis: reasoning patterns, cross-subject links, gap heatmap, session history.
"""

import streamlit as st
from collections import Counter
from datetime import datetime

from auth.db import get_user_sessions, get_knowledge_graph
from engine.adaptive import (
    compute_reasoning_profile, find_cross_subject_links,
    get_user_reasoning_style, STYLE_LABELS, STYLE_DESCRIPTIONS,
)
from data.subjects import SUBJECT_COLORS
from utils.styles import profile_bar


def show_insights():
    user = st.session_state.get("user", {})
    user_id = user.get("id")

    st.markdown("""
    <div style="margin-bottom:1.5rem">
      <div class="tt-h2">Insights</div>
      <div style="font-size:13px;color:var(--text2);font-family:'DM Sans',sans-serif;margin-top:4px">
        Adaptive analysis of your reasoning patterns across all sessions.
      </div>
    </div>
    """, unsafe_allow_html=True)

    sessions = get_user_sessions(user_id, limit=50)

    if not sessions:
        st.markdown("""
        <div style="text-align:center;padding:3rem 0">
          <div style="font-size:15px;color:var(--text3);font-family:'DM Sans',sans-serif">
            No data yet. Complete at least one session to see insights.
          </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── ROW 1: Style + Subject breakdown ─────────────────────────────────────
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="tt-h3" style="margin-bottom:1rem">Reasoning Profile</div>',
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
            grad = bar_colors.get(dim, "")
            profile_html += f"""
            <div class="profile-bar-wrap">
              <div class="profile-bar-label">
                <span>{dim}</span><span style="color:var(--text2)">{pct}%</span>
              </div>
              <div class="profile-bar-track">
                <div class="profile-bar-fill" style="width:{pct}%;background:{grad}"></div>
              </div>
            </div>"""
        st.markdown(profile_html, unsafe_allow_html=True)

        dominant_style = get_user_reasoning_style(user_id)
        desc = STYLE_DESCRIPTIONS.get(dominant_style, "")
        st.markdown(
            f'<div style="margin-top:1rem;padding:10px 12px;background:rgba(124,111,255,.08);'
            f'border:1px solid rgba(124,111,255,.15);border-radius:8px">'
            f'<div style="font-size:10px;color:var(--text3);margin-bottom:3px">Detected Style</div>'
            f'<div style="font-family:\'Syne\',sans-serif;font-size:14px;font-weight:700;'
            f'color:var(--accent2)">{STYLE_LABELS.get(dominant_style, "Developing")}</div>'
            f'<div style="font-size:12px;color:var(--text2);margin-top:3px">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="tt-h3" style="margin-bottom:1rem">Subject Breakdown</div>',
            unsafe_allow_html=True,
        )

        subject_stats: dict[str, dict] = {}
        for s in sessions:
            subj = s.get("subject", "Unknown")
            if subj not in subject_stats:
                subject_stats[subj] = {"sessions": 0, "gaps": 0, "max_depth": 0}
            subject_stats[subj]["sessions"] += 1
            subject_stats[subj]["gaps"] += len(s.get("gaps", []))
            subject_stats[subj]["max_depth"] = max(
                subject_stats[subj]["max_depth"], s.get("depth_reached", 1)
            )

        total_sessions = len(sessions)
        for subj, data in sorted(subject_stats.items(),
                                  key=lambda x: x[1]["sessions"], reverse=True):
            pct = int(data["sessions"] / total_sessions * 100) if total_sessions else 0
            color = SUBJECT_COLORS.get(subj, "var(--accent)")
            st.markdown(f"""
            <div style="margin-bottom:12px">
              <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                <span style="font-family:'DM Sans',sans-serif;font-size:13px;
                             color:{color};font-weight:500">{subj}</span>
                <span style="font-size:11px;color:var(--text3)">
                  {data['sessions']} sessions · {data['gaps']} gaps · depth {data['max_depth']}
                </span>
              </div>
              <div style="height:4px;background:var(--glass2);border-radius:2px">
                <div style="width:{pct}%;height:100%;background:{color};border-radius:2px;opacity:0.7"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROW 2: Gap Analysis ────────────────────────────────────────────────────
    all_gaps = []
    for s in sessions:
        for g in s.get("gaps", []):
            all_gaps.append({**g, "subject": s.get("subject", "")})

    if all_gaps:
        st.markdown(
            '<div class="tt-h3" style="margin-bottom:0.75rem">Gap Analysis</div>',
            unsafe_allow_html=True,
        )

        # Most frequent gaps
        gap_locations = Counter(g.get("location", "") for g in all_gaps if g.get("location"))
        top_gaps = gap_locations.most_common(5)

        gap_col, _ = st.columns([2, 1])
        with gap_col:
            st.markdown('<div class="glass-card gc-red">', unsafe_allow_html=True)
            st.markdown(
                '<div style="font-family:\'Syne\',sans-serif;font-size:12px;font-weight:700;'
                'color:var(--red);text-transform:uppercase;letter-spacing:.04em;'
                'margin-bottom:0.75rem">Most Frequent Gaps</div>',
                unsafe_allow_html=True,
            )
            max_count = top_gaps[0][1] if top_gaps else 1
            for loc, count in top_gaps:
                pct = int(count / max_count * 100)
                st.markdown(f"""
                <div style="margin-bottom:10px">
                  <div style="display:flex;justify-content:space-between;margin-bottom:3px">
                    <span style="font-family:'JetBrains Mono',monospace;font-size:12px;
                                 color:var(--text2)">{loc}</span>
                    <span style="font-size:11px;color:var(--red)">{count}×</span>
                  </div>
                  <div style="height:3px;background:var(--glass2);border-radius:2px">
                    <div style="width:{pct}%;height:100%;background:rgba(255,85,85,0.5);border-radius:2px"></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    # ── ROW 3: Cross-Subject Links ─────────────────────────────────────────────
    cross_links = find_cross_subject_links(user_id)
    if cross_links:
        st.markdown(
            '<div class="tt-h3" style="margin-bottom:0.75rem">Cross-Subject Patterns</div>',
            unsafe_allow_html=True,
        )
        for link in cross_links:
            subjects_str = " · ".join(link["subjects"])
            st.markdown(f"""
            <div class="cross-link" style="margin-bottom:8px">
              <div style="display:flex;align-items:center;justify-content:space-between;
                          margin-bottom:6px">
                <div class="cross-link-title">Cross-Subject Gap</div>
                <div style="font-size:11px;color:var(--pink)">{subjects_str}</div>
              </div>
              <div style="font-family:'JetBrains Mono',monospace;font-size:12px;
                          color:var(--text2);margin-bottom:4px">{link['location']}</div>
              <div style="font-size:12px;color:var(--text3);font-family:'DM Sans',sans-serif;
                          line-height:1.5">{link['insight']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── SESSION HISTORY TABLE ──────────────────────────────────────────────────
    st.markdown(
        '<div class="tt-h3" style="margin-bottom:0.75rem">Session History</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    for s in sessions[:15]:
        subj = s.get("subject", "")
        topics = s.get("topics", [])
        gaps = s.get("gaps", [])
        depth = s.get("depth_reached", 1)
        style = s.get("style", "unclear")
        created = s.get("created_at", "")[:16].replace("T", " ")
        color = SUBJECT_COLORS.get(subj, "var(--accent)")

        style_label = STYLE_LABELS.get(style, "—")
        topics_str = ", ".join(topics[:3]) + ("…" if len(topics) > 3 else "")

        gap_badge = (
            f'<span style="color:var(--red);font-size:10px">{len(gaps)} gap{"s" if len(gaps) != 1 else ""}</span>'
            if gaps else
            f'<span style="color:var(--green);font-size:10px">clean</span>'
        )

        st.markdown(f"""
        <div style="display:flex;align-items:center;padding:10px 0;
                    border-bottom:1px solid var(--border);gap:12px">
          <div style="width:3px;height:36px;background:{color};border-radius:2px;flex-shrink:0"></div>
          <div style="flex:1">
            <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:{color}">
              {subj}
            </div>
            <div style="font-size:11px;color:var(--text3);margin-top:1px">{topics_str}</div>
          </div>
          <div style="text-align:center;min-width:60px">
            <div style="font-family:'JetBrains Mono',monospace;font-size:13px;
                        color:var(--text2)">D{depth}</div>
            <div style="font-size:10px;color:var(--text3)">depth</div>
          </div>
          <div style="text-align:center;min-width:70px">
            <div>{gap_badge}</div>
          </div>
          <div style="text-align:right;min-width:80px">
            <div style="font-size:11px;color:var(--accent2)">{style_label}</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
                        color:var(--text3)">{created}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
