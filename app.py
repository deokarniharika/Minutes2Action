import streamlit as st
import json
import pandas as pd

from ai_parser import extract_tasks
from reminder import generate_reminder

st.set_page_config(page_title="Minutes2Action", page_icon="📝")

st.title("📝 Minutes2Action")
st.write("Turn meeting transcripts into actionable tasks.")

# Input box
transcript = st.text_area(
    "Paste your meeting transcript here",
    height=200
)

# Analyze button
if st.button("Analyze Meeting"):

    if transcript.strip() == "":
        st.warning("Please paste a meeting transcript first.")
        st.stop()

    with st.spinner("Analyzing meeting transcript..."):

        response = extract_tasks(transcript)

        try:
            data = json.loads(response)
            tasks = data.get("tasks", [])
        except:
            st.error("AI response could not be parsed.")
            st.write("Raw response:")
            st.code(response)
            st.stop()

    if not tasks:
        st.info("No action items detected.")
        st.stop()

    df = pd.DataFrame(tasks)

    st.subheader("📋 Action Items")
    st.dataframe(df, use_container_width=True)

    st.subheader("⏰ Reminders")

    for t in tasks:
        task_name = t.get("task", "Task")
        link = generate_reminder(task_name)

        st.markdown(f"🔔 **{task_name}**")
        st.markdown(f"[Create Google Calendar reminder]({link})")
        st.write("")