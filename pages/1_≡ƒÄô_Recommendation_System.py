import streamlit as st
import pandas as pd

from data_loader import load_college_data
from recommendation_engine import recommend


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="College Recommendation System",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# PAGE BACKGROUND
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F6F3FB;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #F6F3FB;
    }

    [data-testid="stHeader"] {
        background-color: #F6F3FB;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background-color: #EEF0F5;
    }

    div.stButton > button {
        border-radius: 10px;
        min-height: 50px;
        font-size: 18px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

try:
    df = load_college_data()
except Exception as e:
    st.error(f"Unable to load college data: {e}")
    st.stop()


# ============================================================
# DISTRICTS
# ============================================================

districts = [
    "Ariyalur",
    "Chengalpattu",
    "Chennai",
    "Coimbatore",
    "Cuddalore",
    "Dharmapuri",
    "Dindigul",
    "Erode",
    "Kanchipuram",
    "Karur",
    "Krishnagiri",
    "Madurai",
    "Nagapattinam",
    "Namakkal",
    "Pudukkottai",
    "Ramanathapuram",
    "Salem",
    "Sivaganga",
    "Thanjavur",
    "Thoothukudi",
    "Tiruchirappalli",
    "Tirunelveli",
    "Tiruppur",
    "Tiruvallur",
    "Vellore",
    "Villupuram",
    "Virudhunagar"
]


# ============================================================
# CATEGORIES
# ============================================================

categories = [
    "OC",
    "BC",
    "BCM",
    "MBC",
    "SC",
    "SCA",
    "ST"
]


# ============================================================
# BRANCHES
# ============================================================

branches = [
    "Computer Science and Engineering",
    "Artificial Intelligence and Data Science",
    "Electronics and Communication Engineering",
    "Electrical and Electronics Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Information Technology",
    "Biomedical Engineering",
    "Chemical Engineering",
    "Automobile Engineering",
    "Computer Science and Engineering (AI and Machine Learning)",
    "Computer Science and Design",
    "Artificial Intelligence and Machine Learning",
    "Cyber Security",
    "Information Technology (SS)"
]


# ============================================================
# TITLE
# ============================================================

st.markdown(
    """
    <h1 style="
        text-align:center;
        font-size:42px;
        margin-bottom:5px;
        color:#17171D;
    ">
        🎓 Find Your Best-Fit College
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        text-align:center;
        font-size:18px;
        color:#77727F;
        margin-bottom:35px;
    ">
        Get personalized college recommendations using your TNEA cutoff,
        category, district and preferred engineering branch.
    </p>
    """,
    unsafe_allow_html=True
)


# ============================================================
# INPUTS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    name = st.text_input(
        "Name",
        placeholder="Enter your name"
    )


with col2:

    district = st.selectbox(
        "District",
        districts,
        index=0
    )


with col3:

    category = st.selectbox(
        "Category",
        categories,
        index=0
    )


# ============================================================
# CUTOFF
# ============================================================

cutoff = st.number_input(
    "TNEA Cutoff",
    min_value=0.0,
    max_value=200.0,
    value=150.0,
    step=0.5,
    format="%.2f"
)


# ============================================================
# BRANCH
# ============================================================

branch = st.selectbox(
    "Preferred Branch",
    branches
)


# ============================================================
# SEARCH BUTTON
# ============================================================

search = st.button(
    "🔎 Find My Colleges",
    type="primary",
    use_container_width=True
)


# ============================================================
# RECOMMENDATIONS
# ============================================================

if search:

    try:

        results = recommend(
            cutoff,
            category,
            district,
            branch
        )

    except Exception as e:

        st.error(
            f"Error while generating recommendations: {e}"
        )

        results = []


    # ========================================================
    # PROFILE SUMMARY
    # ========================================================

    st.divider()

    st.header("📋 Your Profile Summary")


    profile_columns = st.columns(5)


    # --------------------------------------------------------
    # NAME
    # --------------------------------------------------------

    with profile_columns[0]:

        with st.container(
            border=True,
            height=135
        ):

            st.markdown("👤 **Name**")

            st.markdown(
                f"### {name if name else 'Student'}"
            )


    # --------------------------------------------------------
    # DISTRICT
    # --------------------------------------------------------

    with profile_columns[1]:

        with st.container(
            border=True,
            height=135
        ):

            st.markdown("📍 **District**")

            st.markdown(
                f"### {district}"
            )


    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    with profile_columns[2]:

        with st.container(
            border=True,
            height=135
        ):

            st.markdown("🏷️ **Category**")

            st.markdown(
                f"### {category}"
            )


    # --------------------------------------------------------
    # CUTOFF
    # --------------------------------------------------------

    with profile_columns[3]:

        with st.container(
            border=True,
            height=135
        ):

            st.markdown("📊 **Cutoff**")

            st.markdown(
                f"### {cutoff:.2f}"
            )


    # --------------------------------------------------------
    # BRANCH
    # --------------------------------------------------------

    with profile_columns[4]:

        with st.container(
            border=True,
            height=135
        ):

            st.markdown("💻 **Branch**")

            st.markdown(
                f"**{branch}**"
            )


    # ========================================================
    # NO RESULTS
    # ========================================================

    if not results:

        st.divider()

        st.warning(
            "No matching colleges were found in the current dataset."
        )

        st.stop()


    # ========================================================
    # RESULTS OVERVIEW
    # ========================================================

    st.divider()

    st.header("📊 Results Overview")

    st.write(
        "Your admission possibilities based on previous-year cutoff data."
    )


    # ========================================================
    # CHANCE COUNTS
    # ========================================================

    very_high_count = sum(
        1
        for r in results
        if str(r.get("chance", "")).lower() == "very high"
    )

    high_count = sum(
        1
        for r in results
        if str(r.get("chance", "")).lower() == "high"
    )

    moderate_count = sum(
        1
        for r in results
        if str(r.get("chance", "")).lower() == "moderate"
    )

    low_count = sum(
        1
        for r in results
        if str(r.get("chance", "")).lower() == "low"
    )


    # ========================================================
    # RESULT SUMMARY
    # ========================================================

    result_columns = st.columns(5)


    with result_columns[0]:

        with st.container(
            border=True,
            height=125
        ):

            st.markdown("🏫 **Colleges Found**")

            st.markdown(
                f"## {len(results)}"
            )


    with result_columns[1]:

        with st.container(
            border=True,
            height=125
        ):

            st.markdown("🟢 **Very High**")

            st.markdown(
                f"## {very_high_count}"
            )


    with result_columns[2]:

        with st.container(
            border=True,
            height=125
        ):

            st.markdown("🔵 **High**")

            st.markdown(
                f"## {high_count}"
            )


    with result_columns[3]:

        with st.container(
            border=True,
            height=125
        ):

            st.markdown("🟠 **Moderate**")

            st.markdown(
                f"## {moderate_count}"
            )


    with result_columns[4]:

        with st.container(
            border=True,
            height=125
        ):

            st.markdown("🔴 **Low**")

            st.markdown(
                f"## {low_count}"
            )


    # ========================================================
    # TOP PICKS
    # ========================================================

    st.divider()

    st.header("⭐ Top Picks For You")

    st.write(
        "Colleges with the best admission chances."
    )


    top_results = results[:3]

    top_columns = st.columns(3)


    # ========================================================
    # TOP PICK CARDS
    # ========================================================

    for i, college in enumerate(top_results):

        with top_columns[i]:

            # Fixed height makes ALL three boxes equal
            with st.container(
                border=True,
                height=450
            ):

                rank = college.get(
                    "rank",
                    i + 1
                )

                college_name = college.get(
                    "college_name",
                    "College"
                )

                college_district = college.get(
                    "district",
                    district
                )

                college_branch = college.get(
                    "branch",
                    branch
                )

                previous_cutoff = college.get(
                    "cutoff",
                    0
                )

                difference = college.get(
                    "cutoff_difference",
                    0
                )

                chance = college.get(
                    "chance",
                    "Unknown"
                )


                # --------------------------------------------
                # RANK
                # --------------------------------------------

                st.markdown(
                    f"### 🏆 #{rank}"
                )


                # --------------------------------------------
                # COLLEGE NAME
                # --------------------------------------------

                st.markdown(
                    f"**{college_name}**"
                )


                st.write("")


                # --------------------------------------------
                # DISTRICT
                # --------------------------------------------

                st.markdown(
                    f"📍 **District:** {college_district}"
                )


                st.write("")


                # --------------------------------------------
                # BRANCH
                # --------------------------------------------

                st.markdown(
                    f"💻 **Branch:** {college_branch}"
                )


                st.write("")


                # --------------------------------------------
                # PREVIOUS CUTOFF
                # --------------------------------------------

                try:

                    previous_cutoff = float(
                        previous_cutoff
                    )

                    st.markdown(
                        f"📊 **Previous Cutoff:** "
                        f"{previous_cutoff:.2f}"
                    )

                except Exception:

                    st.markdown(
                        f"📊 **Previous Cutoff:** "
                        f"{previous_cutoff}"
                    )


                st.write("")


                # --------------------------------------------
                # YOUR CUTOFF
                # --------------------------------------------

                st.markdown(
                    f"🎯 **Your Cutoff:** {cutoff:.2f}"
                )


                st.write("")


                # --------------------------------------------
                # DIFFERENCE
                # --------------------------------------------

                try:

                    difference = float(
                        difference
                    )

                    st.markdown(
                        f"📈 **Difference:** "
                        f"{difference:+.2f}"
                    )

                except Exception:

                    st.markdown(
                        f"📈 **Difference:** "
                        f"{difference}"
                    )


                st.write("")


                # --------------------------------------------
                # ADMISSION CHANCE
                # --------------------------------------------

                if str(chance).lower() == "very high":

                    st.success(
                        f"🎓 Admission Chance: {chance}"
                    )

                elif str(chance).lower() == "high":

                    st.info(
                        f"🎓 Admission Chance: {chance}"
                    )

                elif str(chance).lower() == "moderate":

                    st.warning(
                        f"🎓 Admission Chance: {chance}"
                    )

                else:

                    st.error(
                        f"🎓 Admission Chance: {chance}"
                    )


    # ========================================================
    # ALL MATCHING COLLEGES
    # ========================================================

    st.divider()

    st.header("🏫 All Matching Colleges")


    table_data = []


    for r in results:

        table_data.append(
            {
                "Rank": r.get(
                    "rank",
                    ""
                ),

                "College Name": r.get(
                    "college_name",
                    ""
                ),

                "District": r.get(
                    "district",
                    district
                ),

                "Branch": r.get(
                    "branch",
                    ""
                ),

                "Previous Cutoff": r.get(
                    "cutoff",
                    ""
                ),

                "Your Cutoff": cutoff,

                "Difference": r.get(
                    "cutoff_difference",
                    ""
                ),

                "Admission Chance": r.get(
                    "chance",
                    ""
                )
            }
        )


    result_df = pd.DataFrame(
        table_data
    )


    # ========================================================
    # TABLE
    # ========================================================

    st.dataframe(
        result_df,
        use_container_width=True,
        hide_index=True,

        column_config={

            "Rank": st.column_config.NumberColumn(
                "Rank",
                width="small"
            ),

            "College Name": st.column_config.TextColumn(
                "College Name",
                width="large"
            ),

            "District": st.column_config.TextColumn(
                "District",
                width="medium"
            ),

            "Branch": st.column_config.TextColumn(
                "Branch",
                width="large"
            ),

            "Previous Cutoff": st.column_config.NumberColumn(
                "Previous Cutoff",
                format="%.2f"
            ),

            "Your Cutoff": st.column_config.NumberColumn(
                "Your Cutoff",
                format="%.2f"
            ),

            "Difference": st.column_config.NumberColumn(
                "Difference",
                format="%+.2f"
            ),

            "Admission Chance": st.column_config.TextColumn(
                "Admission Chance",
                width="medium"
            )
        }
    )


    # ========================================================
    # FOOTER
    # ========================================================

    st.caption(
        f"Showing {len(results)} matching colleges. "
        "Previous-year cutoff data is only a reference "
        "and does not guarantee admission."
    )