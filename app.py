import streamlit as st
import json
import os
import time
import random
import pandas as pd
import plotly.express as px
from datetime import datetime
from typing import Dict, List

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="Mock Test Platform",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CUSTOM CSS - REAL CBT STYLE ====================


def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main background - Dark like real CBT */
    .stApp {
        background: #f0f2f5;
    }
    
    /* ============ LOGIN PAGE ============ */
    .login-header {
        background: linear-gradient(135deg, #1a237e, #283593, #3949ab);
        padding: 40px 20px;
        text-align: center;
        color: white;
        border-radius: 0 0 30px 30px;
        margin-bottom: 30px;
    }
    
    .login-card {
        background: white;
        border-radius: 16px;
        padding: 40px 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        max-width: 420px;
        margin: 0 auto;
    }
    
    /* ============ EXAM HEADER BAR ============ */
    .cbt-header {
        background: linear-gradient(135deg, #1a237e, #283593);
        color: white;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .cbt-header .exam-title {
        font-weight: 600;
        font-size: 14px;
        max-width: 300px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    .cbt-header .section-badge {
        background: rgba(255,255,255,0.2);
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }
    
    /* Timer - Exactly like real CBT */
    .cbt-timer {
        background: #000;
        color: #fff;
        padding: 8px 18px;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        font-size: 20px;
        font-weight: bold;
        letter-spacing: 2px;
        min-width: 80px;
        text-align: center;
        border: 2px solid #444;
    }
    
    .cbt-timer.warning {
        color: #ffcc00;
        border-color: #ffcc00;
        animation: timerBlink 1s infinite;
    }
    
    .cbt-timer.danger {
        color: #ff4444;
        border-color: #ff4444;
        animation: timerBlink 0.5s infinite;
    }
    
    @keyframes timerBlink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* ============ QUESTION AREA ============ */
    .question-container {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #1a237e;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .question-text {
        font-size: 16px;
        font-weight: 500;
        line-height: 1.7;
        color: #1a1a1a;
        margin-bottom: 20px;
    }
    
    .question-number {
        font-weight: 700;
        color: #1a237e;
        font-size: 14px;
        margin-bottom: 8px;
    }
    
    /* ============ OPTION BUTTONS ============ */
    .option-btn {
        display: block;
        width: 100%;
        text-align: left;
        padding: 12px 16px;
        margin: 6px 0;
        border: 2px solid #d0d0d0;
        border-radius: 8px;
        background: white;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 15px;
        color: #333;
    }
    
    .option-btn:hover {
        border-color: #1a237e;
        background: #f5f7ff;
    }
    
    .option-btn.selected {
        border-color: #1a237e;
        background: #e8eaf6;
        font-weight: 600;
        box-shadow: 0 0 0 2px rgba(26, 35, 126, 0.2);
    }
    
    .option-letter {
        display: inline-block;
        width: 28px;
        height: 28px;
        line-height: 28px;
        text-align: center;
        background: #e0e0e0;
        border-radius: 50%;
        margin-right: 10px;
        font-weight: 700;
        font-size: 13px;
    }
    
    .option-btn.selected .option-letter {
        background: #1a237e;
        color: white;
    }
    
    /* ============ QUESTION PALETTE (Right Sidebar) ============ */
    .palette-container {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        height: fit-content;
    }
    
    .palette-title {
        font-weight: 700;
        color: #1a237e;
        font-size: 13px;
        text-align: center;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 8px;
    }
    
    .palette-grid {
        display: grid;
        grid-template-columns: repeat(10, 1fr);
        gap: 6px;
    }
    
    .q-btn {
        aspect-ratio: 1;
        border-radius: 5px;
        border: 2px solid #c0c0c0;
        background: white;
        font-size: 11px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #555;
    }
    
    .q-btn:hover {
        transform: scale(1.15);
        z-index: 10;
    }
    
    .q-btn.answered {
        background: #4caf50;
        color: white;
        border-color: #388e3c;
    }
    
    .q-btn.marked {
        background: #ff9800;
        color: white;
        border-color: #f57c00;
    }
    
    .q-btn.review-answered {
        background: #9c27b0;
        color: white;
        border-color: #7b1fa2;
    }
    
    .q-btn.not-visited {
        background: #f5f5f5;
        color: #999;
        border-color: #ddd;
    }
    
    .q-btn.current {
        box-shadow: 0 0 0 3px #1a237e, 0 0 15px rgba(26, 35, 126, 0.4);
        transform: scale(1.1);
        border-color: #1a237e;
        z-index: 5;
    }
    
    /* ============ LEGEND ============ */
    .legend {
        font-size: 10px;
        margin-top: 12px;
        padding-top: 10px;
        border-top: 1px solid #e0e0e0;
    }
    
    .legend-item {
        display: flex;
        align-items: center;
        gap: 6px;
        margin: 3px 0;
        color: #666;
    }
    
    .legend-dot {
        width: 14px;
        height: 14px;
        border-radius: 3px;
        display: inline-block;
        border: 1px solid rgba(0,0,0,0.2);
    }
    
    /* ============ ACTION BUTTONS ============ */
    .action-btn {
        padding: 10px 18px;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        font-size: 13px;
        transition: all 0.2s;
    }
    
    .btn-save-next {
        background: #2e7d32;
        color: white;
    }
    
    .btn-save-next:hover {
        background: #1b5e20;
    }
    
    .btn-clear {
        background: #c62828;
        color: white;
    }
    
    .btn-clear:hover {
        background: #b71c1c;
    }
    
    .btn-mark {
        background: #e65100;
        color: white;
    }
    
    .btn-mark:hover {
        background: #bf360c;
    }
    
    .btn-submit {
        background: #1a237e;
        color: white;
        padding: 12px 30px;
        font-size: 15px;
    }
    
    .btn-submit:hover {
        background: #0d1b3e;
    }
    
    /* ============ DASHBOARD CARDS ============ */
    .dashboard-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-top: 4px solid #1a237e;
        margin-bottom: 15px;
        transition: all 0.2s;
    }
    
    .dashboard-card:hover {
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    .stat-box {
        background: white;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    .stat-number {
        font-size: 2em;
        font-weight: 800;
        color: #1a237e;
    }
    
    .stat-desc {
        font-size: 12px;
        color: #777;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }
    
    /* ============ RESULT PAGE ============ */
    .result-card {
        background: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .result-score {
        font-size: 3.5em;
        font-weight: 900;
        color: #1a237e;
    }
    
    .result-label {
        font-size: 14px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .correct-dot {
        width: 24px;
        height: 24px;
        border-radius: 4px;
        background: #4caf50;
        display: inline-block;
    }
    
    .incorrect-dot {
        width: 24px;
        height: 24px;
        border-radius: 4px;
        background: #f44336;
        display: inline-block;
    }
    
    .unattempted-dot {
        width: 24px;
        height: 24px;
        border-radius: 4px;
        background: #bdbdbd;
        display: inline-block;
    }
    
    /* ============ RESPONSIVE ============ */
    @media (max-width: 768px) {
        .cbt-timer {
            font-size: 16px;
            padding: 6px 12px;
        }
        .palette-grid {
            grid-template-columns: repeat(8, 1fr);
        }
        .question-text {
            font-size: 14px;
        }
    }
    
    /* Hide Streamlit expander arrow in exam */
    .palette-expander > div:first-child {
        border: none !important;
        background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== SESSION STATE ====================


def init_session():
    defaults = {
        'authenticated': False,
        'username': None,
        'role': None,
        'page': 'dashboard',
        'current_section': None,
        'exam_state': None,
        'last_result': None,
        'show_admin': False,
        'editing_section': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ==================== DATA MANAGEMENT ====================
DATA_DIR = "data"
USERS_FILE = "users.json"


def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "tests"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "attempts"), exist_ok=True)


def load_json(path, default=None):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return default if default is not None else {}


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, default=str)


def load_users():
    return load_json(USERS_FILE, {})


def save_users(users):
    save_json(USERS_FILE, users)


def get_user_tests_path(username):
    return os.path.join(DATA_DIR, "tests", f"{username}.json")


def get_user_attempts_path(username):
    return os.path.join(DATA_DIR, "attempts", f"{username}.json")


def load_user_tests(username):
    return load_json(get_user_tests_path(username), {'sections': {}})


def save_user_tests(username, data):
    data['last_updated'] = datetime.now().isoformat()
    save_json(get_user_tests_path(username), data)


def load_user_attempts(username):
    return load_json(get_user_attempts_path(username), {'history': []})


def save_user_attempt(username, attempt_data):
    attempts = load_user_attempts(username)
    attempts['history'].append(attempt_data)
    save_json(get_user_attempts_path(username), attempts)

# ==================== AUTH ====================


def check_login(username, password):
    users = load_users()
    if username in users:
        user = users[username]
        if user.get('active', True) and user['password'] == password:
            return True
    return False


def login_page():
    st.markdown("""
    <div class="login-header">
        <h1 style="font-size: 2.5em; font-weight: 800; margin: 0;">📚 MockTest Pro</h1>
        <p style="opacity: 0.9; margin-top: 8px;">Computer Based Test Platform</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Sign In to Continue")

        username = st.text_input(
            "Username", placeholder="Enter username", key="login_user")
        password = st.text_input(
            "Password", type="password", placeholder="Enter password", key="login_pass")

        if st.button("🚀 Login to Dashboard", use_container_width=True, type="primary"):
            if not username or not password:
                st.error("Please fill all fields")
            elif check_login(username, password):
                users = load_users()
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = users[username].get('role', 'user')
                st.rerun()
            else:
                st.error("Invalid credentials or account deactivated")

        st.markdown("""
        <p style="text-align: center; color: #999; font-size: 12px; margin-top: 16px;">
            Contact administrator for login credentials
        </p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== ADMIN PANEL ====================


def admin_user_management():
    st.markdown("## 👥 User Management")

    users = load_users()

    active_users = sum(1 for u in users.values() if u.get('active', True))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Users", len(users))
    with col2:
        st.metric("Active Users", active_users)
    with col3:
        st.metric("Admins", sum(1 for u in users.values()
                  if u.get('role') == 'admin'))

    st.markdown("---")

    # Users table
    user_data = []
    for uname, udata in users.items():
        user_data.append({
            'Username': uname,
            'Role': udata.get('role', 'user'),
            'Status': '🟢 Active' if udata.get('active', True) else '🔴 Inactive',
            'Created': udata.get('created', 'N/A')
        })

    if user_data:
        st.dataframe(pd.DataFrame(user_data),
                     use_container_width=True, hide_index=True)

    # Add user
    with st.expander("➕ Add New User", expanded=False):
        with st.form("add_user_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                new_user = st.text_input(
                    "Username", placeholder="e.g., john_doe")
            with col2:
                new_pass = st.text_input(
                    "Password", type="password", placeholder="Set password")

            new_role = st.selectbox("Role", ["user", "admin"])

            if st.form_submit_button("✅ Create User", use_container_width=True):
                if not new_user or not new_pass:
                    st.error("Username and password required")
                elif new_user in users:
                    st.error("User already exists")
                else:
                    users[new_user] = {
                        'password': new_pass,
                        'role': new_role,
                        'created': datetime.now().strftime('%Y-%m-%d'),
                        'active': True
                    }
                    save_users(users)
                    st.success(f"✅ User '{new_user}' created!")
                    st.info(
                        f"🔑 Credentials:\n- Username: `{new_user}`\n- Password: `{new_pass}`")
                    time.sleep(2)
                    st.rerun()

    # Manage existing users
    with st.expander("⚙️ Manage Users", expanded=False):
        user_to_manage = st.selectbox("Select user", list(users.keys()))

        if user_to_manage:
            user_info = users[user_to_manage]

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Role", user_info.get('role', 'user'))
            with col2:
                st.metric("Status", "Active" if user_info.get(
                    'active', True) else "Inactive")

            col_a, col_b, col_c = st.columns(3)

            with col_a:
                new_status = not user_info.get('active', True)
                action = "Activate" if new_status else "Deactivate"
                if st.button(f"🔄 {action}", use_container_width=True):
                    if user_to_manage == st.session_state.username:
                        st.error("Cannot modify yourself!")
                    else:
                        users[user_to_manage]['active'] = new_status
                        save_users(users)
                        st.success(f"User {action.lower()}d!")
                        time.sleep(1)
                        st.rerun()

            with col_b:
                new_password = st.text_input(
                    "New password", type="password", key="reset_pass")
                if st.button("🔑 Reset Password", use_container_width=True):
                    if new_password:
                        users[user_to_manage]['password'] = new_password
                        save_users(users)
                        st.success(f"Password reset!")
                        st.info(f"New password: `{new_password}`")
                        time.sleep(2)
                        st.rerun()

            with col_c:
                if st.button("🗑 Delete", use_container_width=True, type="primary"):
                    if user_to_manage == st.session_state.username:
                        st.error("Cannot delete yourself!")
                    else:
                        del users[user_to_manage]
                        save_users(users)
                        for f in [get_user_tests_path(user_to_manage), get_user_attempts_path(user_to_manage)]:
                            if os.path.exists(f):
                                os.remove(f)
                        st.success(f"Deleted '{user_to_manage}'!")
                        time.sleep(1)
                        st.rerun()

# ==================== DASHBOARD ====================


def dashboard():
    username = st.session_state.username
    user_tests = load_user_tests(username)
    attempts = load_user_attempts(username)
    history = attempts.get('history', [])
    sections = user_tests.get('sections', {})

    # Header
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0 20px;">
        <div>
            <h1 style="font-size: 1.8em; font-weight: 700; color: #1a237e; margin: 0;">
                👋 Welcome, {username}!
            </h1>
            <p style="color: #666; margin: 4px 0 0;">Your CBT Practice Dashboard</p>
        </div>
        {f'<span style="background:#1a237e;color:white;padding:4px 14px;border-radius:20px;font-size:12px;font-weight:600;">ADMIN</span>' if st.session_state.role == 'admin' else ''}
    </div>
    """, unsafe_allow_html=True)

    # Stats
    total_q = sum(len(s.get('questions', [])) for s in sections.values())

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f'<div class="stat-box"><div class="stat-number">{len(history)}</div><div class="stat-desc">Total Tests</div></div>', unsafe_allow_html=True)
    with col2:
        avg = sum(h.get('percentage', 0)
                  for h in history) / len(history) if history else 0
        st.markdown(
            f'<div class="stat-box"><div class="stat-number">{avg:.1f}%</div><div class="stat-desc">Avg Score</div></div>', unsafe_allow_html=True)
    with col3:
        best = max((h.get('percentage', 0) for h in history), default=0)
        st.markdown(
            f'<div class="stat-box"><div class="stat-number">{best:.1f}%</div><div class="stat-desc">Best Score</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(
            f'<div class="stat-box"><div class="stat-number">{total_q}</div><div class="stat-desc">Questions</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3 = st.tabs(
        ["📝 My Test Sections", "➕ Add Questions", "📊 History"])

    with tab1:
        if not sections:
            st.info(
                "🎯 No test sections yet. Go to 'Add Questions' tab to create your first mock test section.")
        else:
            for section_name, section_data in sections.items():
                questions = section_data.get('questions', [])
                q_count = len(questions)
                section_attempts = [h for h in history if h.get(
                    'section') == section_name]
                last = section_attempts[-1] if section_attempts else None

                with st.container():
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                            <div>
                                <h3 style="margin:0; color:#1a237e;">📚 {section_name.replace('_', ' ').title()}</h3>
                                <p style="margin:4px 0 0; color:#888; font-size:13px;">
                                    {q_count} questions • {len(section_attempts)} attempts
                                    {f' • Last Score: {last.get("percentage", 0):.1f}%' if last else ''}
                                </p>
                            </div>
                            <div style="display: flex; gap: 8px;">
                    """, unsafe_allow_html=True)

                    c1, c2, c3 = st.columns([2, 1, 1])
                    with c1:
                        if st.button("▶ Start CBT", key=f"start_{section_name}", use_container_width=True):
                            st.session_state.current_section = section_name
                            st.session_state.page = 'exam_setup'
                            st.rerun()
                    with c2:
                        if st.button("✏️", key=f"edit_{section_name}", use_container_width=True, help="Edit questions"):
                            st.session_state.editing_section = section_name
                            st.rerun()
                    with c3:
                        if st.button("🗑", key=f"del_{section_name}", use_container_width=True, help="Delete section"):
                            del sections[section_name]
                            user_tests['sections'] = sections
                            save_user_tests(username, user_tests)
                            st.success("Deleted!")
                            time.sleep(0.5)
                            st.rerun()

                    st.markdown("</div></div></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("### ➕ Create / Edit Test Section")

        editing = st.session_state.get('editing_section', None)
        existing_q = []
        existing_name = ""

        if editing and editing in sections:
            existing_q = sections[editing].get('questions', [])
            existing_name = editing

        with st.form("section_form"):
            section_name = st.text_input(
                "Section Name",
                value=existing_name.replace(
                    '_', ' ').title() if existing_name else "",
                placeholder="e.g., General Awareness, English, Reasoning, IT Technical"
            )

            st.markdown("**Paste Questions in JSON format:**")

            default_json = json.dumps(
                existing_q, indent=2) if existing_q else ""
            questions_json = st.text_area(
                "JSON Array",
                value=default_json,
                height=250,
                placeholder='[{"id":1,"text":"Question?","options":["A","B","C","D"],"correct":0,"category":"Optional"}]'
            )

            st.markdown("""
            <details>
            <summary style="color:#1a237e; cursor:pointer; font-weight:600;">📋 JSON Format Help</summary>
            <pre style="background:#f5f5f5; padding:12px; border-radius:8px; font-size:13px;">
[
  {
    "id": 1,
    "text": "Your question text here",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": 0,
    "category": "Optional topic",
    "explanation": "Optional explanation"
  }
]
            </pre>
            </details>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button(
                    "💾 Save Section", use_container_width=True, type="primary")
            with col2:
                cancel = st.form_submit_button(
                    "🔄 Cancel", use_container_width=True)

            if cancel:
                st.session_state.editing_section = None
                st.rerun()

            if submit:
                if not section_name or not questions_json:
                    st.error("Fill all fields")
                else:
                    try:
                        questions = json.loads(questions_json)
                        if not isinstance(questions, list) or len(questions) == 0:
                            st.error("Must be a non-empty array")
                        else:
                            valid = all(
                                all(k in q for k in ['text', 'options', 'correct']) and len(
                                    q['options']) == 4
                                for q in questions
                            )
                            if not valid:
                                st.error(
                                    "Each question needs: text, options[4], correct")
                            else:
                                section_key = section_name.lower().replace(' ', '_')
                                if editing and editing != section_key:
                                    del sections[editing]

                                sections[section_key] = {
                                    'questions': questions,
                                    'added': datetime.now().isoformat()
                                }
                                user_tests['sections'] = sections
                                save_user_tests(username, user_tests)
                                st.session_state.editing_section = None
                                st.success(
                                    f"✅ Saved '{section_key}' with {len(questions)} questions!")
                                st.balloons()
                                time.sleep(1.5)
                                st.rerun()
                    except json.JSONDecodeError as e:
                        st.error(f"Invalid JSON: {e}")

    with tab3:
        if not history:
            st.info("📊 No test history yet. Take a test to see results here!")
        else:
            if len(history) > 1:
                chart_data = [
                    {'Attempt': i+1, 'Score (%)': h.get('percentage', 0)} for i, h in enumerate(history)]
                fig = px.line(pd.DataFrame(chart_data), x='Attempt', y='Score (%)', markers=True,
                              color_discrete_sequence=['#1a237e'])
                fig.update_layout(plot_bgcolor='white',
                                  paper_bgcolor='white', height=300)
                st.plotly_chart(fig, use_container_width=True)

            recent = sorted(history, key=lambda x: x.get(
                'timestamp', ''), reverse=True)
            df = pd.DataFrame([{
                'Date': h.get('timestamp', '')[:16],
                'Section': h.get('section', '').replace('_', ' ').title(),
                'Score': f"{h.get('score', 0)}/{h.get('total', 0)}",
                '%': f"{h.get('percentage', 0):.1f}%",
                '✓': h.get('correct', 0),
                '✗': h.get('incorrect', 0),
                'Time': h.get('time_taken', '')
            } for h in recent])
            st.dataframe(df, use_container_width=True, hide_index=True)

# ==================== EXAM SETUP ====================


def exam_setup():
    section = st.session_state.current_section
    username = st.session_state.username
    user_tests = load_user_tests(username)
    section_data = user_tests.get('sections', {}).get(section, {})
    questions = section_data.get('questions', [])

    if not questions:
        st.error("No questions found!")
        st.session_state.page = 'dashboard'
        st.rerun()

    st.markdown(f"## ⚙️ CBT Setup: {section.replace('_', ' ').title()}")
    st.markdown("Configure your Computer Based Test settings below.")

    col1, col2, col3 = st.columns(3)
    with col1:
        num_q = st.number_input("Questions", 5, len(
            questions), min(20, len(questions)), 5)
    with col2:
        timer_min = st.number_input(
            "Time (Minutes)", 1, 180, min(num_q, 30), 5)
    with col3:
        neg = st.selectbox("Negative Marking", [0, 0.25, 0.33, 0.50], 1,
                           format_func=lambda x: f"{x:.2f}" if x > 0 else "None")

    cats = list(set(q.get('category', 'General') for q in questions))
    cat_filter = st.selectbox("Category Filter", ["All"] + sorted(cats))

    if st.button("🚀 START CBT NOW", use_container_width=True, type="primary"):
        pool = questions if cat_filter == "All" else [
            q for q in questions if q.get('category') == cat_filter]
        if len(pool) < num_q:
            st.warning(f"Only {len(pool)} available. Using all.")
            num_q = len(pool)

        selected = random.sample(pool, num_q)
        random.shuffle(selected)

        st.session_state.exam_state = {
            'section': section,
            'questions': selected,
            'current_q': 0,
            'answers': [None] * num_q,
            'status': ['not_visited'] * num_q,
            'total_time': timer_min * 60,
            'negative': neg,
            'total_marks': num_q,
            'start_time': time.time(),
            'submitted': False
        }
        st.session_state.page = 'exam'
        st.rerun()

# ==================== EXAM INTERFACE (CBT STYLE) ====================


def exam_interface():
    state = st.session_state.exam_state

    if not state or state.get('submitted'):
        st.session_state.page = 'result'
        st.rerun()

    elapsed = time.time() - state['start_time']
    remaining = max(0, state['total_time'] - elapsed)

    if remaining <= 0:
        submit_exam()
        return

    # ============ CBT HEADER BAR ============
    mins, secs = divmod(int(remaining), 60)
    timer_class = 'danger' if remaining < 60 else 'warning' if remaining < 180 else ''
    answered = sum(1 for a in state['answers'] if a is not None)

    st.markdown(f"""
    <div class="cbt-header">
        <span class="exam-title">📚 {state['section'].replace('_', ' ').title()}</span>
        <span class="section-badge">Q {state['current_q']+1}/{len(state['questions'])} | Answered: {answered}</span>
        <div class="cbt-timer {timer_class}">{mins:02d}:{secs:02d}</div>
    </div>
    """, unsafe_allow_html=True)

    # ============ MAIN LAYOUT: Question + Palette ============
    col_question, col_palette = st.columns([3, 1])

    with col_palette:
        # Question Palette (Right Side)
        st.markdown('<div class="palette-container">', unsafe_allow_html=True)
        st.markdown(
            '<div class="palette-title">Question Palette</div>', unsafe_allow_html=True)

        # Grid
        grid_html = '<div class="palette-grid">'
        for i in range(len(state['questions'])):
            cls = 'not-visited'
            if state['answers'][i] is not None and state['status'][i] != 'marked':
                cls = 'answered'
            if state['status'][i] == 'marked' and state['answers'][i] is not None:
                cls = 'review-answered'
            elif state['status'][i] == 'marked':
                cls = 'marked'
            if i == state['current_q']:
                cls += ' current'
            grid_html += f'<div class="q-btn {cls}" title="Q{i+1}">{i+1}</div>'
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)

        # Legend
        st.markdown("""
        <div class="legend">
            <div class="legend-item"><span class="legend-dot" style="background:#4caf50;"></span> Answered</div>
            <div class="legend-item"><span class="legend-dot" style="background:#ff9800;"></span> Marked for Review</div>
            <div class="legend-item"><span class="legend-dot" style="background:#9c27b0;"></span> Answered & Marked</div>
            <div class="legend-item"><span class="legend-dot" style="background:#f5f5f5;"></span> Not Visited</div>
            <div class="legend-item"><span class="legend-dot" style="border:3px solid #1a237e;"></span> Current Question</div>
        </div>
        """, unsafe_allow_html=True)

        # Quick jump
        st.markdown("<br>", unsafe_allow_html=True)
        jump = st.number_input("Jump to Q", 1, len(
            state['questions']), state['current_q']+1, key="jump")
        if st.button("Go", key="jump_btn", use_container_width=True):
            state['current_q'] = jump - 1
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with col_question:
        q = state['questions'][state['current_q']]
        current_ans = state['answers'][state['current_q']]

        # Mark as visited
        if state['status'][state['current_q']] == 'not_visited':
            state['status'][state['current_q']] = 'visited'

        # Question display
        st.markdown(f"""
        <div class="question-container">
            <div class="question-number">Question {state['current_q']+1} of {len(state['questions'])}</div>
            <div class="question-text">{q['text']}</div>
            {f'<span style="background:#e8eaf6; padding:2px 10px; border-radius:12px; font-size:12px; color:#1a237e;">📂 {q.get("category", "")}</span>' if q.get('category') else ''}
        </div>
        """, unsafe_allow_html=True)

        # Options
        st.markdown("**Select your answer:**")

        for i, opt in enumerate(q['options']):
            is_sel = current_ans == i
            btn_label = f"{'✅ ' if is_sel else ''}{chr(65+i)}. {opt}"
            btn_type = "primary" if is_sel else "secondary"

            if st.button(btn_label, key=f"opt_{state['current_q']}_{i}", use_container_width=True, type=btn_type):
                state['answers'][state['current_q']] = i
                if state['status'][state['current_q']] in ['not_visited', 'visited']:
                    state['status'][state['current_q']] = 'answered'
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # ============ ACTION BUTTONS (CBT STYLE) ============
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("📌 Mark & Next", use_container_width=True, key="mark_btn",
                         help="Mark for review and go to next question"):
                state['status'][state['current_q']] = 'marked'
                if state['current_q'] < len(state['questions']) - 1:
                    state['current_q'] += 1
                st.rerun()

        with col2:
            if st.button("🗑 Clear", use_container_width=True, key="clear_btn",
                         help="Clear your answer for this question"):
                state['answers'][state['current_q']] = None
                state['status'][state['current_q']] = 'visited'
                st.rerun()

        with col3:
            if st.button("💾 Save & Next", use_container_width=True, key="save_btn",
                         help="Save answer and go to next question"):
                if state['answers'][state['current_q']] is not None:
                    state['status'][state['current_q']] = 'answered'
                if state['current_q'] < len(state['questions']) - 1:
                    state['current_q'] += 1
                st.rerun()

        with col4:
            if st.button("⬅ Previous", use_container_width=True, key="prev_btn",
                         help="Go to previous question", disabled=state['current_q'] == 0):
                if state['current_q'] > 0:
                    state['current_q'] -= 1
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Submit button
        unanswered = sum(1 for a in state['answers'] if a is None)
        if st.button(f"🏁 SUBMIT EXAM ({unanswered} unanswered)", use_container_width=True, type="primary"):
            submit_exam()


def submit_exam():
    state = st.session_state.exam_state
    state['submitted'] = True

    correct = incorrect = unattempted = score = 0
    category_stats = {}

    for i, q in enumerate(state['questions']):
        ans = state['answers'][i]
        cat = q.get('category', 'General')

        if cat not in category_stats:
            category_stats[cat] = {'correct': 0, 'total': 0}
        category_stats[cat]['total'] += 1

        if ans is None:
            unattempted += 1
        elif ans == q['correct']:
            correct += 1
            score += 1
            category_stats[cat]['correct'] += 1
        else:
            incorrect += 1
            score -= state['negative']

    total = len(state['questions'])
    percentage = (score / total) * 100 if total > 0 else 0
    time_taken = int(time.time() - state['start_time'])

    attempt = {
        'timestamp': datetime.now().isoformat(),
        'section': state['section'],
        'score': round(score, 2),
        'total': total,
        'percentage': round(percentage, 2),
        'correct': correct,
        'incorrect': incorrect,
        'unattempted': unattempted,
        'time_taken': f"{time_taken//60}m {time_taken%60}s",
        'negative_marking': state['negative'],
        'category_stats': category_stats
    }

    save_user_attempt(st.session_state.username, attempt)

    st.session_state.last_result = {
        'score': round(score, 2),
        'total': total,
        'percentage': round(percentage, 2),
        'correct': correct,
        'incorrect': incorrect,
        'unattempted': unattempted,
        'time_taken': f"{time_taken//60}m {time_taken%60}s",
        'category_stats': category_stats,
        'questions': state['questions'],
        'answers': state['answers'],
        'negative': state['negative']
    }

    st.session_state.page = 'result'
    st.rerun()

# ==================== RESULT PAGE ====================


def result_page():
    result = st.session_state.get('last_result')
    if not result:
        st.session_state.page = 'dashboard'
        st.rerun()

    st.markdown("## 📊 CBT Exam Results")

    # Score overview
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-score">{result['score']:.1f}</div>
            <div class="result-label">out of {result['total']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        color = "#4caf50" if result['percentage'] >= 60 else "#ff9800" if result['percentage'] >= 35 else "#f44336"
        st.markdown(f"""
        <div class="result-card">
            <div class="result-score" style="color:{color};">{result['percentage']:.1f}%</div>
            <div class="result-label">Percentage</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-score" style="color:#4caf50;">{result['correct']}</div>
            <div class="result-label">Correct</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-score" style="color:#f44336;">{result['incorrect']}</div>
            <div class="result-label">Incorrect</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-score" style="color:#9e9e9e;">{result['unattempted']}</div>
            <div class="result-label">Skipped</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"**⏱ Time Taken:** {result['time_taken']}")

    st.markdown("---")

    # Question-wise review grid
    st.markdown("### 🔍 Question Performance")

    questions = result.get('questions', [])
    answers = result.get('answers', [])

    # Dot grid
    dot_html = '<div style="display: flex; flex-wrap: wrap; gap: 6px; margin: 15px 0;">'
    for i, (q, ans) in enumerate(zip(questions, answers)):
        if ans is None:
            dot_html += f'<span class="unattempted-dot" title="Q{i+1}: Skipped"></span>'
        elif ans == q['correct']:
            dot_html += f'<span class="correct-dot" title="Q{i+1}: Correct"></span>'
        else:
            dot_html += f'<span class="incorrect-dot" title="Q{i+1}: Wrong"></span>'
    dot_html += '</div>'
    st.markdown(dot_html, unsafe_allow_html=True)

    # Detailed review
    st.markdown("### 📝 Detailed Review")

    for i, (q, ans) in enumerate(zip(questions, answers)):
        icon = "⚠️" if ans is None else "✅" if ans == q['correct'] else "❌"
        status = "Skipped" if ans is None else "Correct (+1)" if ans == q[
            'correct'] else f"Wrong (-{result.get('negative', 0.25)})"

        with st.expander(f"{icon} Q{i+1}: {q['text'][:100]}... — {status}"):
            st.markdown(f"**{q['text']}**")
            if q.get('category'):
                st.caption(f"Category: {q['category']}")

            for j, opt in enumerate(q['options']):
                mark = ""
                if j == q['correct']:
                    mark = " ✅"
                if j == ans and ans != q['correct']:
                    mark = " ❌ (Your answer)"
                st.text(f"{chr(65+j)}. {opt}{mark}")

            if q.get('explanation'):
                st.info(f"💡 {q['explanation']}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Retake Test", use_container_width=True):
            st.session_state.page = 'exam_setup'
            st.rerun()
    with col2:
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.session_state.exam_state = None
            st.session_state.last_result = None
            st.rerun()

# ==================== MAIN ====================


def main():
    load_css()
    ensure_dirs()
    init_session()

    # Sidebar
    with st.sidebar:
        if st.session_state.authenticated:
            st.markdown(f"### 👤 {st.session_state.username}")
            st.caption(f"Role: {st.session_state.role}")
            st.markdown("---")

            if st.button("🏠 Dashboard", use_container_width=True):
                for k in ['page', 'exam_state', 'last_result', 'editing_section']:
                    if k in st.session_state:
                        st.session_state[k] = 'dashboard' if k == 'page' else None
                st.rerun()

            if st.session_state.role == 'admin':
                if st.button("👥 User Management", use_container_width=True):
                    st.session_state.show_admin = not st.session_state.get(
                        'show_admin', False)
                    st.rerun()

            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

    # Routing
    if not st.session_state.authenticated:
        login_page()
    elif st.session_state.get('show_admin') and st.session_state.role == 'admin':
        admin_user_management()
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.show_admin = False
            st.rerun()
    elif st.session_state.page == 'exam_setup':
        exam_setup()
    elif st.session_state.page == 'exam':
        exam_interface()
    elif st.session_state.page == 'result':
        result_page()
    else:
        dashboard()


if __name__ == "__main__":
    main()
