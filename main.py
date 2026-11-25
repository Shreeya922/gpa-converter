

# =====================================================
# CGPA HUB - COMPLETE MAIN APPLICATION
# Pokhara University Undergraduate Grading System
# =====================================================

import streamlit as st
import pandas as pd

from grade_system import DEFAULT_SCALE, validate_scale
from quick_converter import render_quick_mode
from advanced_calculator import render_advanced_mode


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="CGPA Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# POKHARA UNIVERSITY GRADE POINTS
# =====================================================

PU_GRADE_POINTS = {
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "F": 0.0
}


# =====================================================
# CGPA TO PERCENTAGE CONVERSION RANGES
# =====================================================

def get_pu_percentage_range(cgpa):

    if cgpa == 4.0:
        return "90% - 100%"

    elif 3.7 <= cgpa < 4.0:
        return "85% - 90%"

    elif 3.3 <= cgpa < 3.7:
        return "80% - 85%"

    elif 3.0 <= cgpa < 3.3:
        return "75% - 80%"

    elif 2.7 <= cgpa < 3.0:
        return "70% - 75%"

    elif 2.3 <= cgpa < 2.7:
        return "65% - 70%"

    elif 2.0 <= cgpa < 2.3:
        return "60% - 65%"

    else:
        return None


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(
        120deg,
        #100b2b,
        #25064c,
        #160d35
    );
    color: white;
}

/* Main Container */
.block-container {
    max-width: 1200px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

/* Headings */
h1 {
    color: #c084fc !important;
    font-size: 43px !important;
    font-weight: 900 !important;
    text-align: center;
}

h2, h3 {
    color: #e9d5ff !important;
}

/* Text */
.stApp p,
.stApp label {
    color: #e5ddf5;
}

/* Navigation Brand */
.brand {
    color: #c084fc !important;
    font-size: 25px;
    font-weight: 900;
    padding: 12px;
    background: #09051a;
    border: 1px solid #7043a0;
    border-radius: 12px;
}

/* Buttons */
.stButton > button {
    background: #16a34a !important;
    color: white !important;
    border: 1px solid #22c55e !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    min-height: 42px;
    transition: 0.3s;
}

.stButton > button:hover {
    background: #15803d !important;
    border-color: #86efac !important;
    transform: translateY(-2px);
}

/* Green Select Boxes */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #15803d !important;
    border: 2px solid #22c55e !important;
    border-radius: 10px !important;
    color: white !important;
}

/* Input Fields */
.stTextInput input,
.stNumberInput input {
    background: #382653 !important;
    color: white !important;
    border: 2px solid #22c55e !important;
    border-radius: 10px !important;
}

/* Cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(216,180,254,0.3);
    border-radius: 18px;
    padding: 15px;
}

/* Metric Cards */
div[data-testid="stMetric"] {
    background: rgba(22,163,74,0.15);
    border: 1px solid #22c55e;
    padding: 18px;
    border-radius: 15px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #10091f;
    border-right: 1px solid #513078;
}

/* Radio Buttons */
.stRadio > div {
    background: rgba(168,85,247,0.12);
    padding: 12px;
    border-radius: 12px;
}

/* Success Messages */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* White Dividers */
hr {
    border: none !important;
    border-top: 1px solid white !important;
    opacity: 0.85;
}

/* Footer */
.footer {
    text-align: center;
    color: #c4b5d5 !important;
    padding: 20px;
    font-size: 13px;
}

/* Back To Top */
.back-to-top {
    position: fixed;
    bottom: 25px;
    right: 25px;
    background: #16a34a;
    color: white !important;
    padding: 12px 18px;
    border-radius: 50px;
    text-decoration: none !important;
    font-weight: bold;
    z-index: 999999;
}

.back-to-top:hover {
    background: #15803d;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SESSION STATE
# =====================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "cgpa_reset_counter" not in st.session_state:
    st.session_state.cgpa_reset_counter = 0

if "sgpa_reset_counter" not in st.session_state:
    st.session_state.sgpa_reset_counter = 0


# =====================================================
# TOP ANCHOR
# =====================================================

st.markdown(
    '<div id="top"></div>',
    unsafe_allow_html=True
)


# =====================================================
# NAVIGATION BAR
# =====================================================

st.markdown(
    '<div class="brand">🎓 CGPA Hub</div>',
    unsafe_allow_html=True
)

nav1, nav2, nav3, nav4, nav5 = st.columns(
    [1, 1.5, 1.7, 1.5, 0.8]
)

with nav1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()

with nav2:
    if st.button("📊 GPA Calculator", use_container_width=True):
        st.session_state.page = "GPA Calculator"
        st.rerun()

with nav3:
    if st.button("🔄 CGPA to Percentage", use_container_width=True):
        st.session_state.page = "CGPA to Percentage"
        st.rerun()

with nav4:
    if st.button("📈 SGPA Calculator", use_container_width=True):
        st.session_state.page = "SGPA Calculator"
        st.rerun()

with nav5:
    if st.button("📰 Blog", use_container_width=True):
        st.session_state.page = "Blog"
        st.rerun()


st.divider()


# =====================================================
# HOME PAGE
# =====================================================

if st.session_state.page == "Home":

    st.markdown(
        "<h1>Welcome to CGPA Hub 🎓</h1>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <p style="
        text-align:center;
        color:#d8b4fe;
        font-size:17px;
    ">
        Your smart academic performance calculator.
        Calculate, convert and track your grades easily.
    </p>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("### 📊 GPA Calculator")
            st.write(
                "Calculate your semester GPA and academic performance."
            )

    with col2:
        with st.container(border=True):
            st.markdown("### 🔄 CGPA Converter")
            st.write(
                "Convert your CGPA into the published percentage range."
            )

    with col3:
        with st.container(border=True):
            st.markdown("### 📚 SGPA Calculator")
            st.write(
                "Calculate SGPA using subject grades and credits."
            )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Open GPA Calculator", use_container_width=True):
            st.session_state.page = "GPA Calculator"
            st.rerun()

    with col2:
        if st.button("Open CGPA Converter", use_container_width=True):
            st.session_state.page = "CGPA to Percentage"
            st.rerun()

    with col3:
        if st.button("Open SGPA Calculator", use_container_width=True):
            st.session_state.page = "SGPA Calculator"
            st.rerun()


# =====================================================
# EXISTING GPA CALCULATOR PAGE
# =====================================================

elif st.session_state.page == "GPA Calculator":

    st.markdown(
        "<h1>CGPA Calculator</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>"
        "Calculate your academic performance."
        "</p>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown("## ⚙️ Grading Settings")

    grading_option = st.sidebar.selectbox(
        "Choose Grading System",
        [
            "Example 4.0 Grading Scale",
            "Custom Grading Scale"
        ]
    )

    if grading_option == "Example 4.0 Grading Scale":

        selected_scale = DEFAULT_SCALE

    else:

        default_table = pd.DataFrame(DEFAULT_SCALE)

        custom_table = st.sidebar.data_editor(
            default_table,
            num_rows="dynamic",
            use_container_width=True,
            key="custom_grading_table"
        )

        selected_scale = custom_table.to_dict(
            orient="records"
        )

    try:

        validate_scale(selected_scale)
        scale_is_valid = True

    except (ValueError, TypeError, KeyError) as error:

        scale_is_valid = False
        st.sidebar.error(str(error))

    st.sidebar.info(
        "Customize the grading ranges according to your university."
    )

    st.markdown("### 🧮 Choose Your Calculator")

    mode = st.radio(
        "Select Calculator Mode",
        [
            "Simple Percentage Converter",
            "Advanced GPA Calculator"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )

    if scale_is_valid:

        if mode == "Simple Percentage Converter":

            render_quick_mode(selected_scale)

        else:

            render_advanced_mode(selected_scale)

    else:

        st.error(
            "Please correct your grading scale before calculating."
        )


# =====================================================
# CGPA TO PERCENTAGE PAGE
# =====================================================

elif st.session_state.page == "CGPA to Percentage":

    st.markdown(
        "<h1>CGPA to Percentage Converter</h1>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <p style="text-align:center; color:#d8b4fe;">
        Convert your Pokhara University CGPA into its
        published percentage range.
    </p>
    """, unsafe_allow_html=True)

    st.write("")

    with st.container(border=True):

        st.markdown("### 🎓 Enter Your CGPA")

        cgpa_key = (
            f"cgpa_input_{st.session_state.cgpa_reset_counter}"
        )

        cgpa = st.number_input(
            "Your CGPA (4.0 scale)",
            min_value=0.0,
            max_value=4.0,
            value=3.0,
            step=0.01,
            format="%.2f",
            key=cgpa_key
        )

        col1, col2 = st.columns(2)

        with col1:

            calculate = st.button(
                "🔄 Convert to Percentage",
                use_container_width=True
            )

        with col2:

            reset = st.button(
                "↩️ Reset",
                use_container_width=True
            )

        if calculate:

            percentage_range = get_pu_percentage_range(cgpa)

            if percentage_range is not None:

                st.session_state.cgpa_result = {
                    "cgpa": cgpa,
                    "percentage": percentage_range
                }

            else:

                st.session_state.cgpa_result = None

                st.warning(
                    "The published conversion table does not "
                    "provide a percentage range for this CGPA."
                )

        if reset:

            st.session_state.cgpa_reset_counter += 1

            st.session_state.pop("cgpa_result", None)

            st.rerun()

    # Display Result

    if st.session_state.get("cgpa_result"):

        result = st.session_state.cgpa_result

        st.write("")

        st.success("CGPA conversion completed!")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Your CGPA",
                f"{result['cgpa']:.2f} / 4.00"
            )

        with col2:

            st.metric(
                "Percentage Range",
                result["percentage"]
            )

        st.info(
            "This is the published percentage range, "
            "not an exact individual percentage certificate. "
            "Contact Pokhara University's Examination Office "
            "for official conversion."
        )

    st.divider()

    with st.expander("View Pokhara University Conversion Table"):

        conversion_data = {
            "CGPA": [
                "4.0",
                "3.7 - below 4.0",
                "3.3 - below 3.7",
                "3.0 - below 3.3",
                "2.7 - below 3.0",
                "2.3 - below 2.7",
                "2.0 - below 2.3"
            ],
            "Percentage Range": [
                "90% - 100%",
                "85% - 90%",
                "80% - 85%",
                "75% - 80%",
                "70% - 75%",
                "65% - 70%",
                "60% - 65%"
            ]
        }

        st.dataframe(
            pd.DataFrame(conversion_data),
            use_container_width=True,
            hide_index=True
        )


# =====================================================
# SGPA CALCULATOR PAGE
# =====================================================

elif st.session_state.page == "SGPA Calculator":

    st.markdown(
        "<h1>SGPA Calculator</h1>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <p style="text-align:center; color:#d8b4fe;">
        Calculate your Semester Grade Point Average
        using Pokhara University's undergraduate grading system.
    </p>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("### 📚 Enter Your Subject Details")

    st.info(
        "Enter each subject name, its credit hours, "
        "and the grade you received."
    )

    # Create initial subject rows

    initial_subjects = pd.DataFrame({
        "Subject Name": ["", "", ""],
        "Credits": [3.0, 3.0, 3.0],
        "Grade": ["A", "A", "A"]
    })

    editor_key = (
        f"sgpa_editor_{st.session_state.sgpa_reset_counter}"
    )

    edited_subjects = st.data_editor(
        initial_subjects,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key=editor_key,

        column_config={

            "Subject Name": st.column_config.TextColumn(
                "Subject Name",
                help="Enter the subject name."
            ),

            "Credits": st.column_config.NumberColumn(
                "Credit Hours",
                min_value=0.5,
                max_value=10.0,
                step=0.5,
                format="%.1f"
            ),

            "Grade": st.column_config.SelectboxColumn(
                "Grade",
                options=list(PU_GRADE_POINTS.keys()),
                required=True
            )
        }
    )

    col1, col2 = st.columns(2)

    with col1:

        calculate_sgpa = st.button(
            "📊 Calculate SGPA",
            use_container_width=True
        )

    with col2:

        reset_sgpa = st.button(
            "↩️ Reset Subjects",
            use_container_width=True
        )

    # Reset subjects

    if reset_sgpa:

        st.session_state.sgpa_reset_counter += 1

        st.session_state.pop("sgpa_result", None)

        st.rerun()

    # Calculate SGPA

    if calculate_sgpa:

        total_credits = 0.0
        total_honor_points = 0.0

        valid_subjects = []
        errors = []

        for index, row in edited_subjects.iterrows():

            subject = row["Subject Name"]

            if pd.isna(subject) or not str(subject).strip():
                continue

            subject = str(subject).strip()

            credits = row["Credits"]
            grade = row["Grade"]

            if pd.isna(credits) or credits <= 0:

                errors.append(
                    f"Invalid credit hours for {subject}."
                )

                continue

            if pd.isna(grade) or grade not in PU_GRADE_POINTS:

                errors.append(
                    f"Please select a valid grade for {subject}."
                )

                continue

            grade_point = PU_GRADE_POINTS[grade]

            honor_points = grade_point * float(credits)

            total_credits += float(credits)

            total_honor_points += honor_points

            valid_subjects.append({
                "Subject": subject,
                "Credits": float(credits),
                "Grade": grade,
                "Grade Point": grade_point,
                "Honor Points": honor_points
            })

        if errors:

            st.session_state.pop("sgpa_result", None)

            for error in errors:
                st.error(error)

        elif len(valid_subjects) == 0:

            st.session_state.pop("sgpa_result", None)

            st.warning(
                "Please enter at least one subject before calculating."
            )

        elif total_credits == 0:

            st.error("Total credits cannot be zero.")

        else:

            sgpa = total_honor_points / total_credits

            st.session_state.sgpa_result = {
                "sgpa": sgpa,
                "total_credits": total_credits,
                "total_honor_points": total_honor_points,
                "subjects": valid_subjects
            }

    # Display SGPA Result

    if st.session_state.get("sgpa_result"):

        result = st.session_state.sgpa_result

        st.write("")

        st.success("Your SGPA has been calculated successfully!")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Your SGPA",
                f"{result['sgpa']:.2f} / 4.00"
            )

        with col2:

            st.metric(
                "Total Credits",
                f"{result['total_credits']:.1f}"
            )

        with col3:

            st.metric(
                "Total Honor Points",
                f"{result['total_honor_points']:.2f}"
            )

        st.markdown("### 📋 Subject Calculation Details")

        st.dataframe(
            pd.DataFrame(result["subjects"]),
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "SGPA = Total Honor Points / Total Credits"
        )

    st.divider()

    with st.expander("View Pokhara University Grade Points"):

        grade_table = pd.DataFrame({
            "Letter Grade": list(PU_GRADE_POINTS.keys()),
            "Grade Point": list(PU_GRADE_POINTS.values())
        })

        st.dataframe(
            grade_table,
            use_container_width=True,
            hide_index=True
        )


# =====================================================
# BLOG PAGE
# =====================================================

elif st.session_state.page == "Blog":

    st.markdown(
        "<h1>CGPA Hub Blog 📰</h1>",
        unsafe_allow_html=True
    )

    st.markdown("### Academic Tips and Information")

    st.write(
        "Learn about GPA, CGPA, SGPA, grading systems "
        "and academic performance."
    )

    with st.container(border=True):

        st.markdown("### 📘 What is SGPA?")

        st.write(
            "SGPA means Semester Grade Point Average. "
            "It represents your academic performance "
            "during one semester."
        )

    with st.container(border=True):

        st.markdown("### 📗 What is CGPA?")

        st.write(
            "CGPA means Cumulative Grade Point Average. "
            "It represents your academic performance "
            "across completed semesters."
        )

    with st.container(border=True):

        st.markdown("### 📙 What are Credit Hours?")

        st.write(
            "Credit hours represent the academic weight "
            "assigned to a particular subject."
        )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown("""
<div class="footer">
    🎓 CGPA Hub | Built with Python and Streamlit
    <br>
    Calculate Smart. Track Your Progress. Achieve More.
    <br>
    Pokhara University Undergraduate Grading System
</div>
""", unsafe_allow_html=True)


# =====================================================
# BACK TO TOP
# =====================================================

st.markdown("""
<a href="#top" class="back-to-top">
    ↑ Back to Top
</a>
""", unsafe_allow_html=True)
