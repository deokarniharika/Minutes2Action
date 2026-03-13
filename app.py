import streamlit as st
import json
import pandas as pd

from ai_parser import extract_tasks
from reminder import generate_reminder

st.set_page_config(
    page_title="minutes2action",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: #F0F5FF !important;
    font-family: 'DM Sans', sans-serif;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1100px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0F2255 !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #C8D8FF !important; }
[data-testid="stSidebar"] .sidebar-brand {
    font-size: 1.15rem;
    font-weight: 600;
    color: #fff !important;
    letter-spacing: -0.02em;
    padding: 0.25rem 0 1.5rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
[data-testid="stSidebar"] .sidebar-brand span {
    color: #60A5FA !important;
}
[data-testid="stSidebar"] .sidebar-nav-label {
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #5B7EC4 !important;
    font-weight: 500;
    margin-bottom: 0.5rem;
}
[data-testid="stSidebar"] .sidebar-footer {
    font-size: 0.78rem;
    color: #4A6090 !important;
    margin-top: 2rem;
    border-top: 1px solid #1B3470;
    padding-top: 1rem;
}
[data-testid="stSidebar"] .sidebar-footer strong {
    color: #7AABF7 !important;
}

/* radio buttons in sidebar */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #A8C0F0 !important;
    font-size: 0.9rem !important;
    padding: 0.35rem 0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"] + div label {
    color: #fff !important;
}

/* ── Page header ── */
.page-header {
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #D0DFFF;
}
.page-header .eyebrow {
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #3B82F6;
    font-weight: 600;
    margin-bottom: 0.4rem;
}
.page-header h1 {
    font-family: 'DM Sans', sans-serif;
    font-size: 2.1rem;
    font-weight: 600;
    color: #0D1F4E;
    letter-spacing: -0.03em;
    line-height: 1.2;
    margin: 0 0 0.5rem;
}
.page-header p {
    font-size: 1rem;
    color: #5470A0;
    margin: 0;
    font-weight: 300;
    max-width: 560px;
    line-height: 1.6;
}

/* ── Hero cards (how it works) ── */
.how-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem;
    margin: 2rem 0;
}
.how-card {
    background: #fff;
    border: 1px solid #D9E6FF;
    border-radius: 16px;
    padding: 1.5rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.how-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #2563EB, #60A5FA);
    border-radius: 16px 16px 0 0;
}
.how-card .step-num {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #3B82F6;
    margin-bottom: 0.6rem;
}
.how-card h3 {
    font-size: 1rem;
    font-weight: 600;
    color: #0D1F4E;
    margin: 0 0 0.4rem;
}
.how-card p {
    font-size: 0.85rem;
    color: #6080B0;
    line-height: 1.55;
    margin: 0;
}

/* ── Feature pills ── */
.feature-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 1.5rem 0 2rem;
}
.pill {
    background: #EEF4FF;
    color: #2563EB;
    border: 1px solid #BFDBFE;
    border-radius: 100px;
    padding: 5px 14px;
    font-size: 0.82rem;
    font-weight: 500;
}

/* ── Input area ── */
[data-testid="stTextArea"] textarea {
    background: #fff !important;
    border: 1.5px solid #CBD8F5 !important;
    border-radius: 12px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    color: #1E3A8A !important;
    line-height: 1.7 !important;
    padding: 1rem 1.1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
}

/* ── Primary button ── */
.stButton > button {
    background: #2563EB !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.6rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    transition: background 0.18s, transform 0.12s !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.25) !important;
}
.stButton > button:hover {
    background: #1D4ED8 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.3) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Section heading ── */
.section-heading {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #3B82F6;
    margin: 2.5rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #D0DFFF;
}

/* ── Task cards ── */
.task-card-wrap {
    background: #fff;
    border: 1px solid #D9E6FF;
    border-radius: 14px 14px 0 0;
    padding: 1.1rem 1.3rem 0.85rem;
    margin-bottom: 0;
    transition: border-color 0.15s, box-shadow 0.15s;
}
.task-card-wrap + div [data-testid="stLinkButton"] {
    margin-top: 0 !important;
}
/* Group card + button visually */
.task-card-wrap {
    border-bottom: none;
}
.task-name {
    font-size: 0.95rem;
    font-weight: 600;
    color: #0D1F4E;
    margin-bottom: 0.35rem;
}
.task-meta {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}
.task-meta-item {
    font-size: 0.78rem;
    color: #6080B0;
    display: flex;
    align-items: center;
    gap: 4px;
}
.task-meta-item strong {
    color: #3B5CA8;
}
.task-badge {
    font-size: 0.72rem;
    font-weight: 600;
    background: #EEF4FF;
    color: #2563EB;
    border: 1px solid #BFDBFE;
    border-radius: 6px;
    padding: 2px 8px;
    white-space: nowrap;
}
/* Style the native link button to look like part of the card */
[data-testid="stLinkButton"] a {
    background: #EEF4FF !important;
    color: #2563EB !important;
    border: 1px solid #D9E6FF !important;
    border-top: none !important;
    border-radius: 0 0 14px 14px !important;
    padding: 0.55rem 1.3rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    display: block !important;
    width: 100% !important;
    text-align: left !important;
    text-decoration: none !important;
    margin-bottom: 0.85rem !important;
    transition: background 0.15s !important;
}
[data-testid="stLinkButton"] a:hover {
    background: #DBEAFE !important;
}

/* ── Stats bar ── */
.stats-bar {
    display: flex;
    gap: 1.5rem;
    background: #0F2255;
    border-radius: 14px;
    padding: 1.1rem 1.5rem;
    margin-bottom: 1.75rem;
    flex-wrap: wrap;
}
.stat-item { text-align: left; }
.stat-num {
    font-size: 1.5rem;
    font-weight: 600;
    color: #60A5FA;
    line-height: 1;
}
.stat-label {
    font-size: 0.72rem;
    color: #5B7EC4;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 2px;
}
.stat-divider {
    width: 1px;
    background: #1B3470;
    align-self: stretch;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #D0DFFF !important;
    border-radius: 12px !important;
    overflow: hidden;
}

/* ── About page ── */
.about-card {
    background: #fff;
    border: 1px solid #D9E6FF;
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1rem;
}
.about-card h3 {
    font-size: 0.9rem;
    font-weight: 600;
    color: #0D1F4E;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-size: 0.75rem;
    color: #3B82F6;
}
.about-card p, .about-card li {
    font-size: 0.9rem;
    color: #4A6090;
    line-height: 1.65;
}
.about-card ul { padding-left: 1.2rem; margin: 0; }
.about-card li { margin-bottom: 0.3rem; }

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #2563EB !important; }

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left-color: #3B82F6 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">minutes2action</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-nav-label">Navigation</div>', unsafe_allow_html=True)
    menu = st.radio("", ["Home", "Analyse Meeting", "About"], label_visibility="collapsed")
    st.markdown("""
    <div class="sidebar-footer">
        Built for <strong>Hackathon 2024</strong><br>
        Gemini AI · Streamlit · Python
    </div>
    """, unsafe_allow_html=True)


# ── HOME ─────────────────────────────────────────────────────
if menu == "Home":

    st.markdown("""
    <div class="page-header">
        <div class="eyebrow">AI-powered productivity</div>
        <h1>Meetings that actually<br>produce results.</h1>
        <p>Paste any meeting transcript and instantly get structured tasks, owners, deadlines — and direct links to create reminders.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-pills">
        <span class="pill">✦ AI task extraction</span>
        <span class="pill">✦ Owner detection</span>
        <span class="pill">✦ Deadline parsing</span>
        <span class="pill">✦ Google Calendar links</span>
        <span class="pill">✦ Notion integration</span>
        <span class="pill">✦ JSON export</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">How it works</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="how-grid">
        <div class="how-card">
            <div class="step-num">Step 01</div>
            <h3>Paste your transcript</h3>
            <p>Copy any meeting notes or recording transcript into the input area.</p>
        </div>
        <div class="how-card">
            <div class="step-num">Step 02</div>
            <h3>AI extracts everything</h3>
            <p>Gemini AI identifies action items, owners, deadlines, and dependencies.</p>
        </div>
        <div class="how-card">
            <div class="step-num">Step 03</div>
            <h3>Take action instantly</h3>
            <p>Create reminders, push to Notion, or export the structured task list.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── ANALYSE ──────────────────────────────────────────────────
elif menu == "Analyse Meeting":

    st.markdown("""
    <div class="page-header">
        <div class="eyebrow">Analyse</div>
        <h1>Extract action items</h1>
        <p>Paste your meeting transcript below. The AI will identify every task, owner, and deadline.</p>
    </div>
    """, unsafe_allow_html=True)

    DEMO = """Niharika will integrate the Ingram API by Friday.
Toby will review the pipeline changes once credentials are received.
Rachel will send API credentials tomorrow morning.
We decided to go with the REST API over SOAP.
James will write up the deployment checklist by end of next week.
Deployment is blocked until pipeline testing is complete."""

    col_input, col_demo = st.columns([5, 1])
    with col_demo:
        if st.button("Load demo"):
            st.session_state["demo_loaded"] = True

    transcript_value = DEMO if st.session_state.get("demo_loaded") else ""

    transcript = st.text_area(
        "Meeting transcript",
        value=transcript_value,
        height=220,
        placeholder="Niharika will integrate the Ingram API by Friday.\nToby will review the pipeline.\nRachel will send credentials tomorrow.",
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    analyze = st.button("⚡ Analyse Meeting")

    if analyze:
        if not transcript.strip():
            st.warning("Please paste a meeting transcript first.")
            st.stop()

        with st.spinner("AI is reading your meeting..."):
            response = extract_tasks(transcript)
            try:
                data = json.loads(response)
                tasks = data.get("tasks", [])
                decisions = data.get("decisions", [])
            except Exception:
                st.error("Could not parse AI response. Raw output below:")
                st.code(response)
                st.stop()

        if not tasks:
            st.info("No tasks were detected in this transcript.")
            st.stop()

        st.session_state["tasks"] = tasks
        st.session_state["decisions"] = decisions

    if "tasks" in st.session_state:
        tasks = st.session_state["tasks"]
        decisions = st.session_state.get("decisions", [])

        owners = len(set(t.get("owner", "") for t in tasks if t.get("owner")))
        with_deadline = sum(1 for t in tasks if t.get("deadline") and t["deadline"] != "null")

        st.markdown(f"""
        <div class="stats-bar">
            <div class="stat-item"><div class="stat-num">{len(tasks)}</div><div class="stat-label">tasks found</div></div>
            <div class="stat-divider"></div>
            <div class="stat-item"><div class="stat-num">{owners}</div><div class="stat-label">owners</div></div>
            <div class="stat-divider"></div>
            <div class="stat-item"><div class="stat-num">{with_deadline}</div><div class="stat-label">with deadline</div></div>
            <div class="stat-divider"></div>
            <div class="stat-item"><div class="stat-num">{len(decisions)}</div><div class="stat-label">decisions</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-heading">Action items</div>', unsafe_allow_html=True)

        for t in tasks:
            import html as _html
            task_name = _html.escape(t.get("task") or "Task")
            owner     = _html.escape(t.get("owner") or "Unassigned")
            deadline  = _html.escape(t.get("deadline") or "No deadline")
            depends   = t.get("depends_on")
            link      = generate_reminder(t.get("task") or "Task")

            depends_html = (
                '<span class="task-badge">Blocked by: ' + _html.escape(str(depends)) + '</span>'
                if depends and str(depends) not in ("null", "None", "")
                else ""
            )

            card_html = (
                '<div class="task-card-wrap">'
                  '<div class="task-name">' + task_name + '</div>'
                  '<div class="task-meta">'
                    '<span class="task-meta-item">&#128100; <strong>' + owner + '</strong></span>'
                    '<span class="task-meta-item">&#128197; ' + deadline + '</span>'
                    + depends_html +
                  '</div>'
                '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)
            st.link_button("📅 Add to Google Calendar", link)

        if decisions:
            st.markdown('<div class="section-heading">Decisions made</div>', unsafe_allow_html=True)
            for d in decisions:
                import html as _html
                safe_d = _html.escape(str(d))
                st.markdown(
                    '<div style="background:#F0F5FF;border-left:3px solid #3B82F6;border-radius:0 10px 10px 0;'
                    'padding:0.6rem 1rem;margin-bottom:0.5rem;font-size:0.88rem;color:#1E3A8A;">'
                    + safe_d + '</div>',
                    unsafe_allow_html=True
                )

        st.markdown('<div class="section-heading">Full task table</div>', unsafe_allow_html=True)
        df = pd.DataFrame(tasks)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown('<div class="section-heading">Export</div>', unsafe_allow_html=True)
        json_str = json.dumps({"tasks": tasks, "decisions": decisions}, indent=2)
        st.download_button(
            label="⬇ Download as JSON",
            data=json_str,
            file_name="minutes2action_output.json",
            mime="application/json"
        )


# ── ABOUT ────────────────────────────────────────────────────
elif menu == "About":

    st.markdown("""
    <div class="page-header">
        <div class="eyebrow">About</div>
        <h1>minutes2action</h1>
        <p>An AI tool that turns meeting transcripts into structured, actionable tasks — built in 15 hours for a hackathon.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="about-card">
            <h3>The problem</h3>
            <p>Meetings produce notes but rarely produce structured action plans. Tasks get lost, owners are unclear, and nothing ships.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="about-card">
            <h3>Features</h3>
            <ul>
                <li>AI-powered task extraction</li>
                <li>Owner and deadline detection</li>
                <li>Dependency mapping</li>
                <li>Google Calendar reminder links</li>
                <li>JSON export</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="about-card">
            <h3>Built with</h3>
            <ul>
                <li>Gemini 1.5 Flash (AI extraction)</li>
                <li>Python + Streamlit (UI)</li>
                <li>Notion API (task creation)</li>
                <li>Google Calendar link generator</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="about-card">
            <h3>The team</h3>
            <p>Built for Hackathon 2024. Total cost: £0. Total time: ~15 hours.</p>
        </div>
        """, unsafe_allow_html=True)