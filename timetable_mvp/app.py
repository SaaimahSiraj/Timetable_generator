import streamlit as st
import pandas as pd
from scheduler import generate_schedule

# Page config
st.set_page_config(page_title="📅 Course Timetable Generator", layout="wide")

st.title("📅 University Timetable Generator")
st.write("Upload course, room, instructor, timeslot, and enrollment CSVs to generate a clash-free timetable.")

# Sidebar uploads
st.sidebar.header("Upload Input CSVs")
uploaded_courses = st.sidebar.file_uploader("Courses CSV", type="csv")
uploaded_rooms = st.sidebar.file_uploader("Rooms CSV", type="csv")
uploaded_instructors = st.sidebar.file_uploader("Instructors CSV", type="csv")
uploaded_timeslots = st.sidebar.file_uploader("Timeslots CSV", type="csv")
uploaded_enrollments = st.sidebar.file_uploader("Enrollments CSV", type="csv")

if st.sidebar.button("🚀 Generate Timetable"):
    if all([uploaded_courses, uploaded_rooms, uploaded_instructors, uploaded_timeslots, uploaded_enrollments]):
        try:
            # Read CSVs
            courses = pd.read_csv(uploaded_courses)
            rooms = pd.read_csv(uploaded_rooms)
            instructors = pd.read_csv(uploaded_instructors)
            slots = pd.read_csv(uploaded_timeslots)
            enrollments = pd.read_csv(uploaded_enrollments)

            # Generate timetable
            schedule = generate_schedule(courses, rooms, instructors, slots, enrollments)

            # Success
            st.success("✅ Timetable generated successfully!")
            st.dataframe(schedule)

            # Download option
            csv = schedule.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Timetable CSV", csv, "schedule.csv", "text/csv"
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please upload **all 5 CSV files** before generating the timetable.")
