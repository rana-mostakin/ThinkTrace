# Author: rana-mostakin
"""
ThinkTrace v1 — CSS Design System
All styling injected via st.markdown. Never use Streamlit default widgets unstyled.
"""

GOOGLE_FONTS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
"""

MASTER_CSS = """
<style>
/* ── DESIGN TOKENS ─────────────────────────────────────── */
:root {
  --bg:#07070f; --bg2:#0d0d1a; --bg3:#12121f;
  --glass:rgba(255,255,255,0.04); --glass2:rgba(255,255,255,0.07); --glass3:rgba(255,255,255,0.10);
  --border:rgba(255,255,255,0.06); --border2:rgba(255,255,255,0.10);
  --text:#eeeef5; --text2:#9090a8; --text3:#4a4a62;
  --accent:#7c6fff; --accent2:#a78bfa; --accentd:#5b4de8;
  --green:#22d47a; --red:#ff5555; --amber:#ffb347;
  --teal:#22d4c0; --pink:#f472b6; --blue:#60a5fa;
  --shadow-sm:0 2px 8px rgba(0,0,0,0.4);
  --shadow-md:0 8px 24px rgba(0,0,0,0.5);
  --glow-accent:0 0 0 1px rgba(124,111,255,.2),0 4px 24px rgba(124,111,255,.08);
  --glow-red:0 0 0 1px rgba(255,85,85,.2),0 4px 24px rgba(255,85,85,.12);
  --glow-green:0 0 0 1px rgba(34,212,122,.2),0 4px 24px rgba(34,212,122,.08);
  --tf:150ms cubic-bezier(0.4,0,0.2,1);
  --ts:300ms cubic-bezier(0.25,0.8,0.25,1);
}

/* ── STREAMLIT OVERRIDES ───────────────────────────────── */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.stDeployButton {display:none;}
.stDecoration {display:none;}

html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] > .main {
  background-color: transparent !important;
}

.main .block-container {
  padding-top: 1.5rem !important;
  padding-bottom: 2rem !important;
  max-width: 1200px !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
  background-color: rgba(13,13,26,0.92) !important;
  backdrop-filter: blur(24px) !important;
  border-right: 1px solid var(--border) !important;
  width: 220px !important;
}
[data-testid="stSidebarNav"] {display:none !important;}
[data-testid="stSidebar"] .block-container {padding: 0 !important;}

/* ── AMBIENT BACKGROUND BLOBS ──────────────────────────── */
@keyframes drift-a {
  0% {transform:translate(0,0) scale(1);} 100% {transform:translate(40px,30px) scale(1.05);}
}
@keyframes drift-b {
  0% {transform:translate(0,0) scale(1);} 100% {transform:translate(-30px,-20px) scale(0.97);}
}
@keyframes drift-c {
  0% {transform:translate(0,0) scale(1);} 100% {transform:translate(20px,-35px) scale(1.03);}
}

.ambient-blob {
  position:fixed; pointer-events:none; z-index:0;
  filter:blur(80px); border-radius:50%;
}
.blob-a {
  width:500px; height:500px;
  background:rgba(124,111,255,0.38);
  top:-100px; left:-100px;
  animation: drift-a 20s infinite alternate ease-in-out;
  opacity:0.45;
}
.blob-b {
  width:400px; height:400px;
  background:rgba(34,212,192,0.22);
  bottom:-80px; right:-80px;
  animation: drift-b 22s infinite alternate ease-in-out;
  opacity:0.5;
}
.blob-c {
  width:350px; height:350px;
  background:rgba(244,114,182,0.14);
  top:40%; right:15%;
  animation: drift-c 18s infinite alternate ease-in-out;
  opacity:0.45;
}

/* ── GLASS CARD SYSTEM ────────────────────────────────── */
.glass-card {
  background: var(--glass);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border2);
  border-radius: 16px;
  padding: 1.25rem;
  position: relative;
  overflow: hidden;
  transition: var(--ts);
}
.glass-card::before {
  content:'';
  position:absolute; inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,.03) 0%,transparent 60%);
  pointer-events:none;
}
.glass-card:hover {
  transform: translateY(-2px);
  border-color: rgba(124,111,255,.3);
}
.gc-accent { box-shadow: var(--glow-accent); }
.gc-red    { box-shadow: var(--glow-red); border-color: rgba(255,85,85,.22) !important; }
.gc-green  { box-shadow: var(--glow-green); border-color: rgba(34,212,122,.22) !important; }
.gc-teal   { box-shadow: 0 0 0 1px rgba(34,212,192,.2),0 4px 24px rgba(34,212,192,.08); }

/* ── BUTTON SYSTEM ────────────────────────────────────── */
.btn-primary {
  display:inline-flex; align-items:center; gap:6px;
  background: linear-gradient(135deg, var(--accent), var(--accentd));
  color: #fff !important;
  border: none; border-radius: 10px;
  padding: 10px 22px;
  font-family: 'Syne', sans-serif; font-weight: 600;
  font-size: 14px; letter-spacing: 0.02em;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(124,111,255,.3);
  transition: var(--ts);
  text-decoration: none !important;
}
.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 24px rgba(124,111,255,.45);
}

.btn-ghost {
  display:inline-flex; align-items:center; gap:6px;
  background: var(--glass); border: 1px solid var(--border2);
  color: var(--text2) !important;
  border-radius: 10px; padding: 9px 18px;
  font-family: 'Syne', sans-serif; font-weight: 600;
  font-size: 13px; letter-spacing: 0.02em;
  cursor: pointer; transition: var(--ts);
  text-decoration: none !important;
}
.btn-ghost:hover {
  background: var(--glass2);
  border-color: var(--border2);
  color: var(--text) !important;
}

.btn-pill {
  display:inline-flex; align-items:center;
  background: var(--glass); border: 1px solid var(--border2);
  color: var(--text2) !important;
  border-radius: 999px; padding: 5px 14px;
  font-family: 'DM Sans', sans-serif; font-weight: 500;
  font-size: 12px; cursor: pointer; transition: var(--tf);
  text-decoration: none !important;
}
.btn-pill:hover, .btn-pill.active {
  background: rgba(124,111,255,.12);
  border-color: rgba(124,111,255,.3);
  color: var(--accent2) !important;
}

.btn-bridge {
  display:inline-flex; align-items:center; gap:6px;
  background: var(--glass); border: 1px solid rgba(255,179,71,.3);
  color: var(--amber) !important;
  border-radius: 10px; padding: 9px 18px;
  font-family: 'Syne', sans-serif; font-weight: 600;
  font-size: 13px; letter-spacing: 0.02em;
  cursor: pointer; transition: var(--ts);
  text-decoration: none !important;
}
.btn-bridge:hover {
  box-shadow: 0 0 0 1px rgba(255,179,71,.3),0 4px 16px rgba(255,179,71,.15);
}

/* ── STREAMLIT BUTTON OVERRIDES ───────────────────────── */
.stButton > button {
  background: linear-gradient(135deg, var(--accent), var(--accentd)) !important;
  color: #fff !important; border: none !important;
  border-radius: 10px !important;
  padding: 10px 22px !important;
  font-family: 'Syne', sans-serif !important; font-weight: 600 !important;
  font-size: 14px !important; letter-spacing: 0.02em !important;
  box-shadow: 0 4px 16px rgba(124,111,255,.3) !important;
  transition: var(--ts) !important;
}
.stButton > button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 24px rgba(124,111,255,.45) !important;
}

/* Ghost buttons via data attribute */
[data-btn-ghost] .stButton > button {
  background: var(--glass) !important;
  border: 1px solid var(--border2) !important;
  color: var(--text2) !important;
  box-shadow: none !important;
}

/* ── INPUT FIELDS ─────────────────────────────────────── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stMultiSelect > div > div {
  background: rgba(255,255,255,.035) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus {
  border-color: rgba(124,111,255,.5) !important;
  box-shadow: 0 0 0 3px rgba(124,111,255,.1) !important;
}

.stTextArea > div > div > textarea {
  background: rgba(255,255,255,.035) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 12px !important;
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 14px !important;
  line-height: 1.7 !important;
  resize: vertical !important;
}
.stTextArea > div > div > textarea:focus {
  border-color: rgba(124,111,255,.5) !important;
  box-shadow: 0 0 0 3px rgba(124,111,255,.1) !important;
}
.stTextArea > div > div > textarea::placeholder {
  color: var(--text3) !important;
}

/* Selectbox */
.stSelectbox [data-baseweb="select"] > div {
  background: rgba(255,255,255,.035) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 10px !important;
}
.stSelectbox label, .stMultiSelect label, .stTextInput label, .stTextArea label {
  color: var(--text2) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 13px !important;
  font-weight: 500 !important;
}

/* Multiselect tags */
[data-baseweb="tag"] {
  background: rgba(124,111,255,.15) !important;
  border: 1px solid rgba(124,111,255,.3) !important;
  color: var(--accent2) !important;
}

/* Dropdown menu */
[data-baseweb="menu"] {
  background: var(--bg2) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 10px !important;
}
[data-baseweb="menu"] li:hover {
  background: rgba(124,111,255,.1) !important;
}

/* ── SKELETON LOADING ─────────────────────────────────── */
@keyframes shimmer {
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
}

.skeleton {
  background: linear-gradient(90deg,
    rgba(255,255,255,.03) 25%,
    rgba(255,255,255,.08) 50%,
    rgba(255,255,255,.03) 75%);
  background-size: 2000px 100%;
  animation: shimmer 1.8s infinite linear;
  border-radius: 8px;
}
.skeleton-line { height: 14px; margin: 8px 0; }
.skeleton-line.short { width: 60%; }
.skeleton-line.medium { width: 80%; }
.skeleton-line.long { width: 95%; }
.skeleton-block { height: 80px; width: 100%; border-radius: 12px; }

/* ── QUESTION CARD ────────────────────────────────────── */
.q-intro {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px; font-weight: 300; font-style: italic;
  color: var(--text2); line-height: 1.6;
  margin-bottom: 10px;
  padding-left: 4px;
}

.q-card {
  background: rgba(124,111,255,.07);
  border: 1px solid rgba(124,111,255,.2);
  border-radius: 14px;
  padding: 1.25rem;
  position: relative; overflow: hidden;
  margin-bottom: 1.25rem;
}
.q-card::before {
  content:'';
  position:absolute; top:0; left:0; right:0; height:2px;
  background: linear-gradient(135deg, var(--accent), var(--teal));
}

.q-header {
  font-family: 'Syne', sans-serif;
  font-size: 10px; font-weight: 700;
  letter-spacing: .05em; text-transform: uppercase;
  color: var(--accent2);
  margin-bottom: 10px;
}

.q-body {
  font-family: 'DM Sans', sans-serif;
  font-size: 14px; line-height: 1.7;
  color: var(--text);
}
.q-body strong, .q-key {
  font-weight: 500;
  color: var(--accent2);
}

.q-hint {
  font-size: 12px; color: var(--text3);
  font-style: italic; margin-top: 10px;
}

/* ── GAP ALERT CARD ───────────────────────────────────── */
.gap-card {
  background: rgba(255,85,85,.07);
  border: 1px solid rgba(255,85,85,.22);
  border-radius: 14px;
  padding: 1.25rem;
  position: relative; overflow: hidden;
  margin-bottom: 1.25rem;
}
.gap-card::before {
  content:'';
  position:absolute; top:0; left:0; right:0; height:2px;
  background: linear-gradient(135deg, var(--red), var(--amber));
}
.gap-title {
  font-family: 'Syne', sans-serif;
  font-size: 12px; font-weight: 700;
  text-transform: uppercase;
  color: var(--red);
  margin-bottom: 8px;
}
.gap-body {
  font-size: 13px; color: #ffaaaa;
  line-height: 1.65;
}
.gap-bridge-link {
  font-size: 12px; color: var(--amber);
  font-weight: 500; margin-top: 8px;
}

/* ── BRIDGE CARD ──────────────────────────────────────── */
.bridge-card {
  background: rgba(34,212,122,.05);
  border: 1px solid rgba(34,212,122,.2);
  border-radius: 14px;
  padding: 1.25rem;
  position: relative; overflow: hidden;
  margin-bottom: 1.25rem;
}
.bridge-card::before {
  content:'';
  position:absolute; top:0; left:0; right:0; height:2px;
  background: linear-gradient(135deg, var(--green), var(--teal));
}

/* ── STAT CARDS ───────────────────────────────────────── */
.stat-card {
  background: var(--glass);
  border: 1px solid var(--border2);
  border-radius: 14px;
  padding: 1.1rem;
  position: relative; overflow: hidden;
  transition: var(--ts);
}
.stat-card:hover { transform: translateY(-2px); }
.stat-value {
  font-family: 'Syne', sans-serif;
  font-size: 28px; font-weight: 800;
  color: var(--text);
  line-height: 1;
}
.stat-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 12px; font-weight: 400;
  color: var(--text2);
  margin-top: 4px;
}
.stat-delta {
  font-size: 11px; font-weight: 500;
  padding: 2px 7px; border-radius: 999px;
  display: inline-block; margin-top: 6px;
}
.delta-pos { background: rgba(34,212,122,.12); color: var(--green); }
.delta-neg { background: rgba(255,85,85,.12); color: var(--red); }
.delta-neu { background: rgba(144,144,168,.12); color: var(--text2); }

/* ── DEPTH INDICATOR ──────────────────────────────────── */
.depth-pips {
  display: flex; gap: 5px; align-items: center;
}
.depth-pip {
  width: 28px; height: 6px;
  border-radius: 3px;
  background: var(--glass2);
  border: 1px solid var(--border);
  transition: var(--ts);
}
.depth-pip.active { background: var(--accent); border-color: var(--accent2); }
.depth-pip.gap    { background: var(--red); border-color: var(--red); }

/* ── REASONING PROFILE BARS ───────────────────────────── */
.profile-bar-wrap { margin-bottom: 10px; }
.profile-bar-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 12px; color: var(--text2);
  display: flex; justify-content: space-between;
  margin-bottom: 4px;
}
.profile-bar-track {
  height: 5px; background: var(--glass2);
  border-radius: 99px; overflow: hidden;
}
.profile-bar-fill {
  height: 100%; border-radius: 99px;
  background: linear-gradient(90deg, var(--accent), var(--teal));
  transition: width 0.6s cubic-bezier(0.25,0.8,0.25,1);
}

/* ── LANGUAGE BADGE ───────────────────────────────────── */
@keyframes badge-pulse {
  0%,100% { opacity:1; } 50% { opacity:0.65; }
}
.lang-badge {
  display: inline-flex; align-items: center; gap: 5px;
  background: rgba(124,111,255,.1);
  border: 1px solid rgba(124,111,255,.2);
  border-radius: 999px;
  padding: 3px 10px;
  font-size: 11px; color: var(--accent2);
  font-family: 'DM Sans', sans-serif;
  animation: badge-pulse 3s ease-in-out infinite;
}

/* ── TOPIC TAG ────────────────────────────────────────── */
.topic-tag {
  display: inline-flex; align-items: center; gap: 4px;
  background: var(--glass);
  border: 1px solid var(--border2);
  border-radius: 6px;
  padding: 3px 9px;
  font-size: 11px; color: var(--text2);
  font-family: 'DM Sans', sans-serif;
  margin: 2px;
}
.topic-tag.probing {
  background: rgba(124,111,255,.1);
  border-color: rgba(124,111,255,.25);
  color: var(--accent2);
}
.topic-tag.done {
  background: rgba(34,212,122,.08);
  border-color: rgba(34,212,122,.2);
  color: var(--green);
}
.topic-tag.gap {
  background: rgba(255,85,85,.08);
  border-color: rgba(255,85,85,.2);
  color: var(--red);
}

/* ── SIDEBAR NAV ──────────────────────────────────────── */
.nav-section {
  padding: 0 12px;
  margin-bottom: 4px;
}
.nav-section-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 10px; font-weight: 500;
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: .06em;
  padding: 8px 8px 4px;
}
.nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 10px;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px; font-weight: 400;
  color: var(--text2);
  cursor: pointer;
  transition: var(--tf);
  text-decoration: none !important;
  border: none; background: transparent;
  width: 100%;
}
.nav-item:hover {
  background: var(--glass2);
  color: var(--text);
}
.nav-item.active {
  background: rgba(124,111,255,.12);
  color: var(--accent2);
  border-left: 2.5px solid var(--accent);
  padding-left: 7.5px;
}
.nav-icon {
  width: 18px; height: 18px;
  flex-shrink: 0;
}
.nav-item.active .nav-icon {
  filter: drop-shadow(0 0 8px rgba(124,111,255,.4));
  color: var(--accent);
}

/* ── SCROLLBAR ────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--glass3); }

/* ── CHAT CONTAINER ───────────────────────────────────── */
.chat-container {
  height: calc(100vh - 280px);
  overflow-y: auto;
  padding-right: 4px;
}

/* ── TYPOGRAPHY HELPERS ───────────────────────────────── */
.tt-h1 {
  font-family: 'Syne', sans-serif;
  font-size: 28px; font-weight: 800;
  color: var(--text);
  letter-spacing: -0.01em;
}
.tt-h2 {
  font-family: 'Syne', sans-serif;
  font-size: 20px; font-weight: 700;
  color: var(--text);
}
.tt-h3 {
  font-family: 'Syne', sans-serif;
  font-size: 15px; font-weight: 700;
  color: var(--text);
  letter-spacing: .01em;
}
.tt-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px; font-weight: 500;
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: .05em;
}
.tt-mono {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px; font-weight: 400;
  color: var(--text2);
}

/* ── DIVIDER ──────────────────────────────────────────── */
.tt-divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 1.25rem 0;
}

/* ── PROGRESS STEPS (registration) ───────────────────── */
.reg-steps {
  display: flex; align-items: center; gap: 8px;
  margin-bottom: 2rem;
}
.reg-step {
  display: flex; align-items: center; gap: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 12px; color: var(--text3);
}
.reg-step.active { color: var(--accent2); }
.reg-step.done { color: var(--green); }
.reg-step-dot {
  width: 24px; height: 24px;
  border-radius: 50%;
  background: var(--glass2);
  border: 1px solid var(--border2);
  display: flex; align-items: center; justify-content: center;
  font-family: 'Syne', sans-serif;
  font-size: 11px; font-weight: 700;
  flex-shrink: 0;
}
.reg-step.active .reg-step-dot {
  background: rgba(124,111,255,.2);
  border-color: rgba(124,111,255,.4);
  color: var(--accent2);
}
.reg-step.done .reg-step-dot {
  background: rgba(34,212,122,.15);
  border-color: rgba(34,212,122,.3);
  color: var(--green);
}
.reg-step-line {
  flex:1; height:1px; background: var(--border);
}

/* ── LANGUAGE GRID ────────────────────────────────────── */
.lang-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 6px;
  max-height: 280px;
  overflow-y: auto;
  padding: 2px;
}
.lang-option {
  background: var(--glass);
  border: 1px solid var(--border2);
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
  transition: var(--tf);
}
.lang-option:hover {
  border-color: rgba(124,111,255,.3);
  background: rgba(124,111,255,.06);
}
.lang-option.selected {
  background: rgba(124,111,255,.12);
  border-color: rgba(124,111,255,.4);
}
.lang-native {
  font-size: 13px; color: var(--text); font-weight: 500;
  font-family: 'DM Sans', sans-serif;
}
.lang-en {
  font-size: 11px; color: var(--text3);
  font-family: 'DM Sans', sans-serif;
}

/* ── REVIEW SCHEDULE ROW ──────────────────────────────── */
.review-row {
  display: flex; align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
}
.review-concept {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px; color: var(--text);
}
.review-subject {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px; color: var(--text2);
  margin-top: 2px;
}
.review-due {
  font-size: 11px; font-family: 'JetBrains Mono', monospace;
}
.review-due.overdue { color: var(--red); }
.review-due.today { color: var(--amber); }
.review-due.future { color: var(--text3); }

/* ── CROSS-SUBJECT LINK ───────────────────────────────── */
.cross-link {
  background: rgba(244,114,182,.06);
  border: 1px solid rgba(244,114,182,.2);
  border-radius: 10px;
  padding: 10px 14px;
  margin-bottom: 8px;
}
.cross-link-title {
  font-family: 'Syne', sans-serif;
  font-size: 11px; font-weight: 700;
  color: var(--pink);
  text-transform: uppercase;
  letter-spacing: .04em;
}

/* ── FORM LAYOUT HELPERS ──────────────────────────────── */
.form-section {
  background: var(--glass);
  border: 1px solid var(--border2);
  border-radius: 14px;
  padding: 1.5rem;
  margin-bottom: 1rem;
}

/* ── SPINNER OVERRIDE ─────────────────────────────────── */
.stSpinner { display: none !important; }

/* ── SELECT SLIDERS ───────────────────────────────────── */
.stSlider > div > div {
  color: var(--accent) !important;
}

/* ── RADIO & CHECKBOX ─────────────────────────────────── */
.stRadio label, .stCheckbox label {
  color: var(--text2) !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* ── METRIC OVERRIDES ─────────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--glass) !important;
  border-radius: 12px !important;
  padding: 12px 16px !important;
  border: 1px solid var(--border2) !important;
}

/* ── INFO / WARNING / ERROR BOXES ────────────────────── */
.stAlert {
  border-radius: 10px !important;
  border: 1px solid var(--border2) !important;
}

/* ── USER PROFILE CARD (bottom of sidebar) ───────────── */
.user-profile-card {
  padding: 12px 16px;
  border-top: 1px solid var(--border);
  margin-top: auto;
}
.user-name {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px; font-weight: 500;
  color: var(--text);
}
.user-meta {
  font-size: 11px; color: var(--text3);
  font-family: 'DM Sans', sans-serif;
}
.user-avatar {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--teal));
  display: flex; align-items: center; justify-content: center;
  font-family: 'Syne', sans-serif; font-weight: 700;
  font-size: 12px; color: #fff;
  flex-shrink: 0;
}

/* ── SESSION HEADER ───────────────────────────────────── */
.session-header {
  display: flex; align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}
.session-subject {
  font-family: 'Syne', sans-serif;
  font-size: 18px; font-weight: 800;
  color: var(--text);
}
.session-topic-line {
  font-family: 'DM Sans', sans-serif;
  font-size: 12px; color: var(--text2);
  margin-top: 2px;
}

/* ── CHAT MESSAGES ────────────────────────────────────── */
.msg-user {
  background: rgba(124,111,255,.08);
  border: 1px solid rgba(124,111,255,.15);
  border-radius: 12px 12px 4px 12px;
  padding: 10px 14px;
  margin-bottom: 12px;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px; line-height: 1.6;
  color: var(--text);
  max-width: 85%; margin-left: auto;
}
.msg-ai {
  margin-bottom: 16px;
}

/* ── Z-INDEX LAYERING ─────────────────────────────────── */
.ambient-blob { z-index: 0; }
[data-testid="stAppViewContainer"] { z-index: 1; }
[data-testid="stSidebar"] { z-index: 10; }

/* ── PLOTLY OVERRIDES ─────────────────────────────────── */
.js-plotly-plot .plotly .bg { fill: transparent !important; }
.plotly-graph-div { background: transparent !important; }

/* ── RESPONSIVE ───────────────────────────────────────── */
@media (max-width: 768px) {
  html { font-size: 13px; }
  .tt-h1 { font-size: 24px; }
  .tt-h2 { font-size: 18px; }
  .main .block-container { padding: 0.75rem !important; }
}
</style>
"""

AMBIENT_HTML = """
<div class="ambient-blob blob-a"></div>
<div class="ambient-blob blob-b"></div>
<div class="ambient-blob blob-c"></div>
"""


def inject_styles():
    """Call at top of every page to inject all CSS."""
    import streamlit as st
    st.markdown(GOOGLE_FONTS + MASTER_CSS + AMBIENT_HTML, unsafe_allow_html=True)


def glass_card_open(variant=""):
    """Returns opening HTML for a glass card."""
    cls = f"glass-card {variant}" if variant else "glass-card"
    return f'<div class="{cls}">'


def glass_card_close():
    return "</div>"


def skeleton_loading(n_lines=3):
    """Render skeleton loading placeholders."""
    import streamlit as st
    sizes = ["medium", "long", "short", "long", "medium"]
    lines = "".join(f'<div class="skeleton skeleton-line {sizes[i % len(sizes)]}"></div>'
                    for i in range(n_lines))
    st.markdown(f'<div style="padding:8px 0">{lines}</div>', unsafe_allow_html=True)


def depth_pips(current: int, total: int = 5, has_gap: bool = False):
    """Render depth indicator pips."""
    pips = ""
    for i in range(1, total + 1):
        if i < current:
            cls = "depth-pip active"
        elif i == current and has_gap:
            cls = "depth-pip gap"
        elif i <= current:
            cls = "depth-pip active"
        else:
            cls = "depth-pip"
        pips += f'<div class="{cls}"></div>'
    return f'<div class="depth-pips">{pips}</div>'


def profile_bar(label: str, value: float, color: str = ""):
    """Render a reasoning profile progress bar."""
    pct = int(value * 100)
    fill_style = f"width:{pct}%"
    if color:
        fill_style += f";background:{color}"
    return f"""
    <div class="profile-bar-wrap">
      <div class="profile-bar-label">
        <span>{label}</span><span style="color:var(--text2)">{pct}%</span>
      </div>
      <div class="profile-bar-track">
        <div class="profile-bar-fill" style="{fill_style}"></div>
      </div>
    </div>"""
