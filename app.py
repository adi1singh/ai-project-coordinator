import streamlit as st
import pandas as pd

from db import init_db, save_tasks, get_all_tasks
from llm_utils import extract_tasks_from_notes, generate_weekly_status_report, analyze_project_risk


st.set_page_config(page_title="AI Project Coordinator", layout="wide")

init_db()

st.title("AI Project Coordinator for Teams")
st.write("Paste meeting notes below and let AI extract project tasks and generate a weekly status report.")

api_key = st.text_input("Enter your OpenAI API Key", type="password")
meeting_notes = st.text_area("Paste meeting notes here", height=250)

if st.button("Analyze Notes"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    elif not meeting_notes.strip():
        st.error("Please paste some meeting notes.")
    else:
        with st.spinner("Analyzing notes..."):
            tasks = extract_tasks_from_notes(meeting_notes, api_key)
            summary = generate_weekly_status_report(meeting_notes, api_key)
            risk = analyze_project_risk(meeting_notes, api_key)
            

            if tasks:
                save_tasks(tasks)
                st.success("Tasks extracted and saved successfully.")

                st.subheader("Weekly Status Report")
                st.info(summary)

                st.subheader("Extracted Tasks")
                df = pd.DataFrame(tasks)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No tasks were extracted. Try using clearer meeting notes.")

st.subheader("Saved Tasks")

rows = get_all_tasks()

if rows:
    df_saved = pd.DataFrame(
        rows,
        columns=["ID", "Task Name", "Owner", "Due Date", "Priority", "Blocker", "Status"]
    )
    st.dataframe(df_saved, use_container_width=True)
else:
    st.info("No tasks saved yet.")

st.subheader("Project Risk Analysis")

if risk:
    st.write("Overall Risk Level:", risk.get("overall_risk_level"))
    st.write("Delay Probability:", risk.get("delay_probability"))

    st.write("Main Risks:")
    for r in risk.get("main_risks", []):
        st.write("-", r)

    st.write("Recommendation:")
    st.info(risk.get("recommendation"))