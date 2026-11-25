
# advanced_calculator.py

import streamlit as st
import pandas as pd

from gpa_calculator import calculate_weighted_gpa


def render_advanced_mode(scale):

    st.subheader("Advanced GPA Calculator")

    st.write(
        "Enter your academic details and subject marks."
    )

    with st.form("advanced_gpa_form"):

        st.markdown("### Student Information")

        name = st.text_input("Student Name")

        student_id = st.text_input(
            "Student ID (Optional)"
        )

        faculty = st.text_input(
            "Faculty / Program"
        )

        college = st.text_input(
            "College / University"
        )

        semester = st.selectbox(
            "Select Semester",
            [
                "First Semester",
                "Second Semester",
                "Third Semester",
                "Fourth Semester",
                "Fifth Semester",
                "Sixth Semester",
                "Seventh Semester",
                "Eighth Semester",
                "Other"
            ]
        )

        st.markdown("### Subject Information")

        number_of_subjects = st.number_input(
            "Number of Subjects",
            min_value=1,
            max_value=20,
            value=4,
            step=1
        )

        subjects = []

        for i in range(int(number_of_subjects)):

            st.markdown(f"#### Subject {i + 1}")

            col1, col2 = st.columns(2)

            with col1:

                subject_name = st.text_input(
                    "Subject Name",
                    key=f"name_{i}"
                )

                obtained = st.number_input(
                    "Obtained Marks",
                    min_value=0.0,
                    value=0.0,
                    key=f"obtained_{i}"
                )

            with col2:

                full = st.number_input(
                    "Full Marks",
                    min_value=0.0,
                    value=100.0,
                    key=f"full_{i}"
                )

                credit = st.number_input(
                    "Credit Hours",
                    min_value=0.0,
                    value=3.0,
                    key=f"credit_{i}"
                )

            subjects.append({
                "name": subject_name,
                "obtained": obtained,
                "full": full,
                "credit": credit
            })

        submitted = st.form_submit_button(
            "Calculate My GPA",
            use_container_width=True
        )

    if submitted:

        if not name.strip():
            st.error("Please enter the student name.")
            return

        if not faculty.strip():
            st.error("Please enter your faculty or program.")
            return

        if not college.strip():
            st.error("Please enter your college or university.")
            return

        for subject in subjects:

            if not subject["name"].strip():
                st.error("Please enter all subject names.")
                return

            if subject["full"] <= 0:
                st.error("Full marks must be greater than zero.")
                return

            if subject["obtained"] > subject["full"]:
                st.error(
                    f"Obtained marks cannot exceed full marks "
                    f"for {subject['name']}."
                )
                return

            if subject["credit"] <= 0:
                st.error(
                    f"Credit hours must be greater than zero "
                    f"for {subject['name']}."
                )
                return

        try:

            report = calculate_weighted_gpa(
                subjects,
                scale
            )

        except ValueError as error:

            st.error(str(error))
            return

        st.success("Your GPA report is ready!")

        st.markdown("---")

        st.markdown("## Student Academic Report")

        st.write("**Student Name:**", name)
        st.write("**Student ID:**", student_id or "Not provided")
        st.write("**Faculty:**", faculty)
        st.write("**College:**", college)
        st.write("**Semester:**", semester)

        st.markdown("### Subject-wise Results")

        df = pd.DataFrame(report["subjects"])

        display_df = df[
            [
                "name",
                "obtained",
                "full",
                "credit",
                "percentage",
                "grade",
                "grade_point"
            ]
        ].copy()

        display_df.columns = [
            "Subject",
            "Obtained Marks",
            "Full Marks",
            "Credit Hours",
            "Percentage",
            "Grade",
            "Grade Point"
        ]

        st.dataframe(
            display_df.round(2),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Final Performance")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Overall Percentage",
            f"{report['percentage']:.2f}%"
        )

        col2.metric(
            "Final GPA",
            f"{report['gpa']:.2f}"
        )

        col3.metric(
            "Total Credits",
            f"{report['total_credit']:.2f}"
        )

        csv = display_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Subject Report",
            data=csv,
            file_name="gpa_report.csv",
            mime="text/csv",
            use_container_width=True
        )
