# Author: rana-mostakin
"""
ThinkTrace v1 — Registration & Login
3-step registration wizard + login page.
"""

import streamlit as st
from auth.db import create_user, authenticate, init_db
from data.languages import LANGUAGES, DEFAULT_LANGUAGE
from data.subjects import SUBJECTS


# ── LOGIN PAGE ────────────────────────────────────────────────────────────────

def show_login():
    st.markdown("""
    <div style="max-width:400px;margin:0 auto;padding-top:2rem">
      <div style="text-align:center;margin-bottom:2.5rem">
        <div style="font-family:'Syne',sans-serif;font-size:32px;font-weight:800;
                    color:var(--text);letter-spacing:-0.02em">ThinkTrace</div>
        <div style="font-family:'DM Sans',sans-serif;font-size:13px;font-weight:300;
                    color:var(--text2);margin-top:4px">Cognitive Reasoning Laboratory</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-family:\'Syne\',sans-serif;font-size:16px;font-weight:700;'
            'color:var(--text);margin-bottom:1.25rem">Sign In</div>',
            unsafe_allow_html=True,
        )

        email = st.text_input("Email", placeholder="you@example.com",
                              key="login_email")
        password = st.text_input("Password", type="password",
                                 placeholder="Your password",
                                 key="login_password")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Sign In", key="login_btn", use_container_width=True):
                if email and password:
                    user = authenticate(email, password)
                    if user:
                        st.session_state["user"] = user
                        st.session_state["page"] = "dashboard"
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
                else:
                    st.warning("Please enter your credentials.")

        st.markdown(
            '<div style="text-align:center;margin-top:1rem;font-size:13px;color:var(--text3)">'
            'New to ThinkTrace? </div>',
            unsafe_allow_html=True,
        )
        if st.button("Create Account", key="goto_register", use_container_width=True):
            st.session_state["page"] = "register"
            st.session_state["reg_step"] = 1
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# ── REGISTRATION WIZARD ───────────────────────────────────────────────────────

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


def show_register():
    step = st.session_state.get("reg_step", 1)
    reg_data = st.session_state.get("reg_data", {})

    st.markdown("""
    <div style="max-width:540px;margin:0 auto;padding-top:1.5rem">
      <div style="margin-bottom:1.5rem">
        <div style="font-family:'Syne',sans-serif;font-size:24px;font-weight:800;
                    color:var(--text)">Create your account</div>
        <div style="font-size:13px;color:var(--text2);font-family:'DM Sans',sans-serif;
                    margin-top:3px">Step {step} of 3</div>
      </div>
    </div>
    """.format(step=step), unsafe_allow_html=True)

    # Step progress indicator
    _render_steps(step)

    st.markdown('<div class="form-section">', unsafe_allow_html=True)

    if step == 1:
        _reg_step1(reg_data)
    elif step == 2:
        _reg_step2(reg_data)
    elif step == 3:
        _reg_step3(reg_data)

    st.markdown('</div>', unsafe_allow_html=True)

    if step > 1:
        if st.button("← Back", key="reg_back"):
            st.session_state["reg_step"] = step - 1
            st.rerun()


def _render_steps(current: int):
    labels = ["Identity", "Goals", "Language"]
    dots = ""
    for i, label in enumerate(labels, 1):
        if i < current:
            cls = "done"
            dot_content = "✓"
        elif i == current:
            cls = "active"
            dot_content = str(i)
        else:
            cls = ""
            dot_content = str(i)

        dots += f"""
        <div class="reg-step {cls}">
          <div class="reg-step-dot">{dot_content}</div>
          <span>{label}</span>
        </div>"""
        if i < len(labels):
            dots += '<div class="reg-step-line"></div>'

    st.markdown(f'<div class="reg-steps">{dots}</div>', unsafe_allow_html=True)


def _reg_step1(reg_data: dict):
    st.markdown(
        '<div style="font-family:\'Syne\',sans-serif;font-size:15px;font-weight:700;'
        'color:var(--text);margin-bottom:1rem">Your identity</div>',
        unsafe_allow_html=True,
    )

    name = st.text_input("Full Name", value=reg_data.get("name", ""),
                         placeholder="Your name", key="reg_name")
    email = st.text_input("Email", value=reg_data.get("email", ""),
                          placeholder="you@example.com", key="reg_email")
    password = st.text_input("Password", type="password",
                              placeholder="Minimum 8 characters", key="reg_pw")
    confirm = st.text_input("Confirm Password", type="password",
                             placeholder="Repeat password", key="reg_pw2")

    if st.button("Continue →", key="reg_step1_next", use_container_width=True):
        errors = []
        if not name.strip():
            errors.append("Name is required.")
        if not email.strip() or "@" not in email:
            errors.append("Valid email is required.")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")
        if password != confirm:
            errors.append("Passwords do not match.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            st.session_state["reg_data"] = {
                **reg_data, "name": name.strip(),
                "email": email.strip(), "password": password,
            }
            st.session_state["reg_step"] = 2
            st.rerun()


def _reg_step2(reg_data: dict):
    st.markdown(
        '<div style="font-family:\'Syne\',sans-serif;font-size:15px;font-weight:700;'
        'color:var(--text);margin-bottom:1rem">Your study profile</div>',
        unsafe_allow_html=True,
    )

    grade = st.selectbox("Grade / Year", GRADE_OPTIONS,
                         index=GRADE_OPTIONS.index(reg_data.get("grade", GRADE_OPTIONS[3])),
                         key="reg_grade")
    goal = st.selectbox("Primary Study Goal", GOAL_OPTIONS,
                        index=GOAL_OPTIONS.index(reg_data.get("goal", GOAL_OPTIONS[0]))
                        if reg_data.get("goal") in GOAL_OPTIONS else 0,
                        key="reg_goal")

    if st.button("Continue →", key="reg_step2_next", use_container_width=True):
        st.session_state["reg_data"] = {
            **reg_data, "grade": grade, "goal": goal,
        }
        st.session_state["reg_step"] = 3
        st.rerun()


def _reg_step3(reg_data: dict):
    st.markdown(
        '<div style="font-family:\'Syne\',sans-serif;font-size:15px;font-weight:700;'
        'color:var(--text);margin-bottom:0.5rem">Choose your language</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:12px;color:var(--text2);font-family:\'DM Sans\',sans-serif;'
        'margin-bottom:1rem">ThinkTrace will reason with you in your chosen language.</div>',
        unsafe_allow_html=True,
    )

    # Search filter
    search = st.text_input("Search languages", placeholder="Type to filter...",
                           key="reg_lang_search")

    selected_lang = st.session_state.get("reg_selected_lang",
                                          reg_data.get("language", DEFAULT_LANGUAGE))

    # Filter languages
    filtered = LANGUAGES
    if search.strip():
        sq = search.lower()
        filtered = [l for l in LANGUAGES
                    if sq in l["native"].lower() or sq in l["english"].lower()]

    # Render language grid
    grid_html = '<div class="lang-grid">'
    for lang in filtered:
        is_selected = lang["english"] == selected_lang
        sel_cls = "selected" if is_selected else ""
        grid_html += f"""
        <div class="lang-option {sel_cls}"
             onclick="this.closest('.lang-grid').querySelectorAll('.lang-option').forEach(el=>el.classList.remove('selected'));this.classList.add('selected')">
          <div class="lang-native">{lang['native']}</div>
          <div class="lang-en">{lang['english']}</div>
        </div>"""
    grid_html += "</div>"

    # Use a selectbox as the actual selector (grid is visual reference)
    lang_names = [l["english"] for l in filtered] if filtered else [DEFAULT_LANGUAGE]
    default_idx = lang_names.index(selected_lang) if selected_lang in lang_names else 0

    chosen = st.selectbox(
        "Selected Language",
        lang_names,
        index=default_idx,
        key="reg_lang_select",
    )
    st.session_state["reg_selected_lang"] = chosen

    st.markdown(grid_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Create Account", key="reg_final", use_container_width=True):
        language = chosen
        user_id = create_user(
            name=reg_data.get("name", ""),
            email=reg_data.get("email", ""),
            password=reg_data.get("password", ""),
            grade=reg_data.get("grade", ""),
            study_goal=reg_data.get("goal", ""),
            language=language,
        )

        if user_id:
            # Auto login
            user = authenticate(reg_data["email"], reg_data["password"])
            if user:
                st.session_state["user"] = user
                st.session_state["page"] = "dashboard"
                # Clear reg state
                st.session_state.pop("reg_data", None)
                st.session_state.pop("reg_step", None)
                st.session_state.pop("reg_selected_lang", None)
                st.rerun()
        else:
            st.error("Email already registered. Please sign in.")
