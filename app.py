import streamlit as st
import json
import pandas as pd

from ai_parser import extract_tasks
from reminder import generate_reminder

# Page config
st.set_page_config(
    page_title="Minutes2Action",
    page_icon="⚡",
    layout="wide"
)

# Header
st.markdown("""
# ⚡ Minutes2Action
### Turn meeting conversations into **clear tasks and actions**
""")

st.write("Paste a meeting transcript below and automatically extract action items, owners, and deadlines.")

st.divider()

# Input Section
st.subheader("📝 Meeting Transcript")

transcript = st.text_area(
    "Paste your transcript here",
    height=220,
    placeholder="Example:\nNiharika will integrate the Ingram API by Friday.\nToby will review the pipeline.\nRachel will send credentials tomorrow."
)

analyze = st.button("🚀 Analyze Meeting")

if analyze:

    if transcript.strip() == "":
        st.warning("Please paste a meeting transcript first.")
        st.stop()

    with st.spinner("🤖 AI is analyzing your meeting..."):

        response = extract_tasks(transcript)

        try:
            data = json.loads(response)
            tasks = data.get("tasks", [])
        except:
            st.error("AI response could not be parsed.")
            st.code(response)
            st.stop()

    if not tasks:
        st.info("No action items found.")
        st.stop()

    df = pd.DataFrame(tasks)

    st.divider()

    # Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric("📋 Action Items", len(tasks))

    with col2:
        owners = df["owner"].nunique() if "owner" in df else 0
        st.metric("👥 Owners Involved", owners)

    st.divider()

    # Action Table
    st.subheader("📋 Extracted Tasks")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    # Reminders Section
    st.subheader("⏰ Create Reminders")

    for t in tasks:

        task_name = t.get("task", "Task")

        link = generate_reminder(task_name)

        with st.container():
            col1, col2 = st.columns([4,1])

            with col1:
                st.write(f"**{task_name}**")

            with col2:
                st.link_button("📅 Reminder", link)

        st.write("")