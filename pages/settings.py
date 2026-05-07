# Author: rana-mostakin
"""
ThinkTrace v1 — Settings Page
User preferences: language, grade, study goal, theme toggle.
"""

import streamlit as st
from auth.db import update_user, get_user
from data.languages import LANGUAGES, DEFAULT_LANGUAGE
from data.subjects import SUBJECTS


GRADE_OPTIONS = [
    "Grade 9", "Grade 10", "Grade 11", "Grade 12",
    "First Year (University)", "Second Year (University)",
    "Third Year (University)", "Other",
]

GOAL_OPTIONS = [
    "HSC / A-Level Preparation",
    "SAT / DSAT Preparation",
    "IELTS / TOEFL Preparation",
    "University Entrance Exam",
    "Deep Subject Mastery",
    "Competitive Math / Science",
    "General Self-Study",
]


def show_settings():
    user = st.session_state.get("user", {})
    user_id = user.get("id")

    st.markdown("""
    <div style="margin-bottom:1.5rem">
      <div class="tt-h2">Settings</div>
      <div style="font-size:13px;color:var(--text2);font-family:'DM Sans',sans-serif;margin-top:4px">
        Manage your profile, language, and study preferences.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Profile ────────────────────────────────────────────────────────────────
    st.markdown(
        '<div style="font-family:\'Syne\',sans-serif;font-size:13px;font-weight:700;'
        'color:var(--text2);text-transform:uppercase;letter-spacing:.04em;'
        'margin-bottom:0.75rem">Profile</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="glass-card" style="margin-bottom:1.25rem">', unsafe_allow_html=True)

    new_name = st.text_input("Name", value=user.get("name", ""), key="settings_name")

    grade_idx = GRADE_OPTIONS.index(user.get("grade", GRADE_OPTIONS[3])) \
        if user.get("grade") in GRADE_OPTIONS else 3
    new_grade = st.selectbox("Grade / Year", GRADE_OPTIONS,
                              index=grade_idx, key="settings_grade")

    goal_idx = GOAL_OPTIONS.index(user.get("study_goal", GOAL_OPTIONS[0])) \
        if user.get("study_goal") in GOAL_OPTIONS else 0
    new_goal = st.selectbox("Study Goal", GOAL_OPTIONS,
                             index=goal_idx, key="settings_goal")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Language ───────────────────────────────────────────────────────────────
    st.markdown(
        '<div style="font-family:\'Syne\',sans-serif;font-size:13px;font-weight:700;'
        'color:var(--text2);text-transform:uppercase;letter-spacing:.04em;'
        'margin-bottom:0.75rem">Language</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="glass-card" style="margin-bottom:1.25rem">', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:12px;color:var(--text3);font-family:\'DM Sans\',sans-serif;'
        'margin-bottom:0.75rem">ThinkTrace uses this language for all AI responses.</div>',
        unsafe_allow_html=True,
    )

    lang_names = [l["english"] for l in LANGUAGES]
    current_lang = user.get("language", DEFAULT_LANGUAGE)
    lang_idx = lang_names.index(current_lang) if current_lang in lang_names else 0
    new_lang = st.selectbox("Language", lang_names,
                             index=lang_idx, key="settings_lang")

    # Find native name
    native = next((l["native"] for l in LANGUAGES if l["english"] == new_lang), new_lang)
    st.markdown(
        f'<div style="font-size:12px;color:var(--accent2);margin-top:6px">'
        f'Native: {native}</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Save ───────────────────────────────────────────────────────────────────
    if st.button("Save Changes", key="settings_save", use_container_width=True):
        update_user(
            user_id,
            name=new_name.strip() or user.get("name", ""),
            grade=new_grade,
            study_goal=new_goal,
            language=new_lang,
        )
        # Refresh user in session state
        updated = get_user(user_id)
        if updated:
            st.session_state["user"] = dict(updated)
        st.success("Settings saved.")
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Account info ───────────────────────────────────────────────────────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-family:\'DM Sans\',sans-serif;font-size:13px;color:var(--text2)">'
        f'Email: <span style="color:var(--text)">{user.get("email","")}</span>'
        f'</div>'
        f'<div style="font-size:11px;color:var(--text3);margin-top:4px">'
        f'Member since: {user.get("created_at","")[:10]}'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Sign out ───────────────────────────────────────────────────────────────
    if st.button("Sign Out", key="settings_signout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
