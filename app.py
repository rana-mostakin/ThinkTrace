# Author: rana-mostakin
"""
ThinkTrace v1 — Main Application Router
Sidebar navigation, CSS injection, page routing, auth gate.
"""

import streamlit as st
import sys
import os

# Ensure package root is on path
sys.path.insert(0, os.path.dirname(__file__))

from auth.db import init_db
from utils.styles import inject_styles

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ThinkTrace",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── INIT DB ───────────────────────────────────────────────────────────────────
init_db()

# ── INJECT STYLES ─────────────────────────────────────────────────────────────
inject_styles()

# ── AUTH GATE ─────────────────────────────────────────────────────────────────
user = st.session_state.get("user")
page = st.session_state.get("page", "login")

if not user:
    # Unauthenticated routes
    if page == "register":
        from auth.auth_ui import show_register
        show_register()
    else:
        from auth.auth_ui import show_login
        show_login()
    st.stop()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────

def _nav_item(label: str, icon_svg: str, target_page: str, current_page: str) -> bool:
    is_active = current_page == target_page
    active_cls = "active" if is_active else ""
    clicked = st.sidebar.button(
        f"{label}",
        key=f"nav_{target_page}",
        use_container_width=True,
    )
    return clicked


def render_sidebar():
    current_page = st.session_state.get("page", "dashboard")
    user = st.session_state.get("user", {})
    name = user.get("name", "Student")
    grade = user.get("grade", "")
    language = user.get("language", "English")

    # Logo
    st.sidebar.markdown("""
    <div style="padding:20px 16px 12px">
      <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;
                  color:var(--text);letter-spacing:-0.01em">ThinkTrace</div>
      <div style="font-size:10px;color:var(--text3);font-family:'DM Sans',sans-serif;
                  margin-top:1px">Cognitive Laboratory</div>
    </div>
    <hr style="border:none;border-top:1px solid var(--border);margin:0 0 8px">
    """, unsafe_allow_html=True)

    # Navigation sections
    nav_items = [
        ("Main", [
            ("Dashboard",      "dashboard",     "□"),
            ("New Session",    "new_session",   "◈"),
            ("Knowledge Graph","graph",         "◇"),
            ("Review Schedule","schedule",      "◻"),
        ]),
        ("Analysis", [
            ("Insights",       "insights",      "◉"),
            ("Upload Questions","upload",        "↑"),
        ]),
        ("Account", [
            ("Settings",       "settings",      "◌"),
        ]),
    ]

    for section_label, items in nav_items:
        st.sidebar.markdown(
            f'<div style="padding:10px 16px 4px;font-size:10px;font-weight:500;'
            f'color:var(--text3);text-transform:uppercase;letter-spacing:.06em;'
            f'font-family:\'DM Sans\',sans-serif">{section_label}</div>',
            unsafe_allow_html=True,
        )
        for label, target, icon in items:
            is_active = current_page == target
            # Style active buttons differently via CSS trick
            if is_active:
                st.sidebar.markdown(
                    f'<div style="margin:1px 8px;padding:8px 10px;border-radius:8px;'
                    f'background:rgba(124,111,255,.12);border-left:2.5px solid var(--accent);'
                    f'font-family:\'DM Sans\',sans-serif;font-size:13px;font-weight:400;'
                    f'color:var(--accent2)">{icon} &nbsp; {label}</div>',
                    unsafe_allow_html=True,
                )
            else:
                if st.sidebar.button(
                    f"{icon}  {label}",
                    key=f"nav_{target}",
                    use_container_width=True,
                ):
                    st.session_state["page"] = target
                    st.rerun()

    # User profile card at bottom
    st.sidebar.markdown("<br>" * 3, unsafe_allow_html=True)
    st.sidebar.markdown('<hr style="border:none;border-top:1px solid var(--border)">', unsafe_allow_html=True)

    initial = name[0].upper() if name else "U"
    st.sidebar.markdown(f"""
    <div style="padding:12px 14px;display:flex;align-items:center;gap:10px">
      <div style="width:32px;height:32px;border-radius:50%;
                  background:linear-gradient(135deg,var(--accent),var(--teal));
                  display:flex;align-items:center;justify-content:center;
                  font-family:'Syne',sans-serif;font-weight:700;font-size:13px;
                  color:#fff;flex-shrink:0">{initial}</div>
      <div>
        <div style="font-family:'DM Sans',sans-serif;font-size:13px;font-weight:500;
                    color:var(--text)">{name}</div>
        <div style="font-size:10px;color:var(--text3)">{grade} · {language}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


render_sidebar()

# ── OVERRIDE SIDEBAR BUTTON STYLES ────────────────────────────────────────────
# Make sidebar buttons look like nav items
st.markdown("""
<style>
[data-testid="stSidebar"] .stButton > button {
  background: transparent !important;
  color: var(--text2) !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 8px 10px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 13px !important;
  font-weight: 400 !important;
  letter-spacing: 0 !important;
  box-shadow: none !important;
  text-align: left !important;
  justify-content: flex-start !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: var(--glass2) !important;
  color: var(--text) !important;
  transform: none !important;
}
</style>
""", unsafe_allow_html=True)

# ── PAGE ROUTER ───────────────────────────────────────────────────────────────
page = st.session_state.get("page", "dashboard")

# Main content wrapper
st.markdown('<div style="position:relative;z-index:1">', unsafe_allow_html=True)

if page == "dashboard":
    from pages.dashboard import show_dashboard
    show_dashboard()

elif page == "new_session":
    from pages.session import show_session_setup
    show_session_setup()

elif page == "session_chat":
    from pages.session import show_session_chat
    show_session_chat()

elif page == "graph":
    from pages.graph import show_graph
    show_graph()

elif page == "schedule":
    from pages.schedule import show_schedule
    show_schedule()

elif page == "insights":
    from pages.insights import show_insights
    show_insights()

elif page == "settings":
    from pages.settings import show_settings
    show_settings()

elif page == "upload":
    from pages.upload_questions import show_upload_questions
    show_upload_questions()

else:
    from pages.dashboard import show_dashboard
    show_dashboard()

st.markdown('</div>', unsafe_allow_html=True)
