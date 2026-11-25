
# quick_converter.py

import streamlit as st

from grade_system import get_grade, percentage_to_gpa


def render_quick_mode(scale):

    st.subheader("Quick Percentage to GPA Converter")

    st.write(
        "Enter your percentage and choose your conversion method."
    )

    with st.form("quick_gpa_form"):

        percentage = st.number_input(
            "Enter your percentage (%)",
            min_value=0.0,
            max_value=100.0,
            value=83.0,
            step=0.5
        )

        method = st.radio(
            "Choose conversion method",
            [
                "University Grade Range",
                "Mathematical Conversion"
            ]
        )

        maximum_gpa = st.selectbox(
            "Choose maximum GPA scale",
            [4.0, 5.0],
            disabled=(method == "University Grade Range")
        )

        submitted = st.form_submit_button(
            "Convert to GPA",
            use_container_width=True
        )

    if submitted:

        if method == "University Grade Range":

            grade, gpa = get_grade(percentage, scale)

            st.success("Conversion completed!")

            col1, col2, col3 = st.columns(3)

            col1.metric("Percentage", f"{percentage:.2f}%")
            col2.metric("Letter Grade", grade)
            col3.metric("GPA", f"{gpa:.2f}")

        else:

            gpa = percentage_to_gpa(
                percentage,
                maximum_gpa
            )

            st.success("Conversion completed!")

            col1, col2 = st.columns(2)

            col1.metric("Percentage", f"{percentage:.2f}%")
            col2.metric("Estimated GPA", f"{gpa:.2f}")

            st.info(
                "This is a mathematical estimate, "
                "not necessarily your university's official GPA."
            )
