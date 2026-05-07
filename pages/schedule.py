# Author: rana-mostakin
"""
ThinkTrace v1 — Review Schedule Page
Spaced repetition queue with SM-2 interval tracking.
"""

import streamlit as st
from datetime import datetime
from auth.db import get_all_schedule, upsert_schedule
from engine.adaptive import repair_gap_in_graph
from data.subjects import SUBJECT_COLORS


def show_schedule():
    user = st.session_state.get("user", {})
    user_id = user.get("id")

    st.markdown("""
    <div style="margin-bottom:1.5rem">
      <div class="tt-h2">Review Schedule</div>
      <div style="font-size:13px;color:var(--text2);font-family:'DM Sans',sans-serif;margin-top:4px">
        Spaced repetition queue. Concepts strengthen each time you review them.
      </div>
    </div>
    """, unsafe_allow_html=True)

    all_items = get_all_schedule(user_id)
    today = datetime.now().strftime("%Y-%m-%d")

    if not all_items:
        st.markdown("""
        <div style="text-align:center;padding:3rem 0">
          <div style="font-size:15px;color:var(--text3);font-family:'DM Sans',sans-serif">
            No items scheduled yet.
          </div>
          <div style="font-size:13px;color:var(--text3);margin-top:6px">
            Complete a session to add concepts to your review queue.
          </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Segment: overdue, today, upcoming
    overdue  = [i for i in all_items if i["next_review"] <  today]
    due_today= [i for i in all_items if i["next_review"] == today]
    upcoming = [i for i in all_items if i["next_review"] >  today]

    if overdue:
        st.markdown(f"""
        <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
                    color:var(--red);text-transform:uppercase;letter-spacing:.04em;
                    margin-bottom:0.5rem">Overdue — {len(overdue)}</div>
        """, unsafe_allow_html=True)
        _render_schedule_items(overdue, user_id, today, "overdue")
        st.markdown("<br>", unsafe_allow_html=True)

    if due_today:
        st.markdown(f"""
        <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
                    color:var(--amber);text-transform:uppercase;letter-spacing:.04em;
                    margin-bottom:0.5rem">Due Today — {len(due_today)}</div>
        """, unsafe_allow_html=True)
        _render_schedule_items(due_today, user_id, today, "today")
        st.markdown("<br>", unsafe_allow_html=True)

    if upcoming:
        st.markdown(f"""
        <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
                    color:var(--text2);text-transform:uppercase;letter-spacing:.04em;
                    margin-bottom:0.5rem">Upcoming — {len(upcoming)}</div>
        """, unsafe_allow_html=True)
        _render_schedule_items(upcoming[:10], user_id, today, "upcoming")


def _render_schedule_items(items: list, user_id: int, today: str, section: str):
    for item in items:
        subj = item.get("subject", "")
        concept = item.get("concept", "")
        strength = item.get("strength", 0.5)
        interval = item.get("interval_days", 1)
        next_r = item.get("next_review", today)
        session_count = item.get("session_count", 0)

        str_pct = int(strength * 100)
        subj_color = SUBJECT_COLORS.get(subj, "var(--text2)")

        if next_r < today:
            days_str = f"{(datetime.strptime(today, '%Y-%m-%d') - datetime.strptime(next_r, '%Y-%m-%d')).days}d overdue"
            date_color = "var(--red)"
        elif next_r == today:
            days_str = "Today"
            date_color = "var(--amber)"
        else:
            days_diff = (datetime.strptime(next_r, "%Y-%m-%d") - datetime.now()).days
            days_str = f"In {days_diff}d"
            date_color = "var(--text3)"

        # Strength bar
        bar_color = "var(--red)" if strength < 0.3 else ("var(--amber)" if strength < 0.7 else "var(--green)")

        col_main, col_action = st.columns([4, 1])
        with col_main:
            st.markdown(f"""
            <div style="padding:12px 16px;background:var(--glass);
                        border:1px solid var(--border2);border-radius:10px;margin-bottom:6px">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
                <div>
                  <div style="font-family:'DM Sans',sans-serif;font-size:13px;
                              font-weight:500;color:var(--text)">{concept}</div>
                  <div style="font-size:11px;color:{subj_color};margin-top:1px">{subj}</div>
                </div>
                <div style="text-align:right">
                  <div style="font-family:'JetBrains Mono',monospace;font-size:11px;
                              color:{date_color}">{days_str}</div>
                  <div style="font-size:10px;color:var(--text3);margin-top:1px">
                    interval {interval}d · {session_count} reviews
                  </div>
                </div>
              </div>
              <div style="display:flex;align-items:center;gap:8px">
                <div style="flex:1;height:3px;background:var(--glass2);border-radius:2px">
                  <div style="width:{str_pct}%;height:100%;background:{bar_color};border-radius:2px"></div>
                </div>
                <div style="font-size:10px;color:var(--text3);font-family:'JetBrains Mono',monospace">
                  {str_pct}%
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        with col_action:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Review", key=f"review_{item.get('id', concept)}_{section}"):
                # Mark as reviewed: boost strength, extend interval
                new_strength = min(1.0, strength + 0.2)
                upsert_schedule(user_id, concept, subj,
                                strength=new_strength, is_gap=False)
                repair_gap_in_graph(user_id, concept, subj)
                st.success(f"Reviewed: {concept}")
                st.rerun()
