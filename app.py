import streamlit as st
import os
from datetime import datetime
import pandas as pd

MOOD_OPTIONS = ["😊 Happy", "😠 Angry", "😕 Confused", "🎉 Excited"]
# used csv for privacy, can dock to google api if given a company credential
LOG_FILE = "mood_log.csv"

if "page" not in st.session_state:
    st.session_state.page = "start"

col1, col2 = st.columns(2)

with col1:
    if st.button("🖊️ Mood Input"):
        st.session_state.page = "input"

with col2:
    if st.button("📊 Mood Analytics"):
        st.session_state.page = "analytics"

if st.session_state.page == "input":
    selected_mood = st.radio("What's your mood today?", MOOD_OPTIONS)
    comment = st.text_input("Any comments you'd like to add?")

    if st.button("Submit"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = pd.DataFrame([[timestamp, selected_mood, comment]], columns=["timestamp", "mood", "comment"])

        if os.path.exists(LOG_FILE):
            old_log = pd.read_csv(LOG_FILE)
            mood_log = pd.concat([old_log, new_entry], ignore_index=True)
        else:
            mood_log = new_entry

        mood_log.to_csv(LOG_FILE, index=False)
        st.success(f"Mood logged: {selected_mood}")

elif st.session_state.page == "analytics":
    if os.path.exists(LOG_FILE):
        st.subheader("Mood History")
        log_df = pd.read_csv(LOG_FILE)

        log_df["timestamp"] = pd.to_datetime(log_df["timestamp"], errors="coerce", format='mixed')
        log_df["date"] = log_df["timestamp"].dt.date

        st.markdown("Filter Options")

        unique_dates = sorted(log_df["date"].unique(), reverse=True)
        selected_date = st.selectbox("Select a date to view moods:", unique_dates)
        mood_filter = st.multiselect("Filter by mood type (optional):", log_df["mood"].unique())
        filtered_df = log_df[log_df["date"] == selected_date]

        if mood_filter:
            filtered_df = filtered_df[filtered_df["mood"].isin(mood_filter)]

        st.dataframe(filtered_df.sort_values(by="timestamp", ascending=False))

        mood_counts = filtered_df["mood"].value_counts()
        st.subheader("Mood Summary for Selected Date")
        st.bar_chart(mood_counts)

    else:
        st.warning("No mood data logged yet.")