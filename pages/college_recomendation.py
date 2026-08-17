import streamlit as st
import pandas as pd

from recommendation_engine import recommend, prepare_data


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="College Recommendation System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def get_data():
    return prepare_data()


try:
    df = get_data()
    DATA_ERROR = None
except Exception as e:
    df = pd.DataFrame()
    DATA_ERROR = str(e)


# ============================================================
# CONSTANTS
# ============================================================

CATEGORIES = [
    "OC",
    "BC",
    "BCM",
    "MBC",
    "SC",
    "SCA",
    "ST"
]


BRANCHES = [
    "CSE",
    "IT",
    "AI & DS",
    "AI & ML",
    "ECE",
    "EEE",
    "MECHANICAL",
    "CIVIL",
    "AERONAUTICAL",
    "AEROSPACE",
    "BIOTECHNOLOGY",
    "CHEMICAL",
    "AGRICULTURAL"
]


BRANCH_DISPLAY = {

    "CSE":
        "Computer Science and Engineering",

    "IT":
        "Information Technology",

    "AI & DS":
        "Artificial Intelligence and Data Science",

    "AI & ML":
        "Artificial Intelligence and Machine Learning",

    "ECE":
        "Electronics and Communication Engineering",

    "EEE":
        "Electrical and Electronics Engineering",

    "MECHANICAL":
        "Mechanical Engineering",

    "CIVIL":
        "Civil Engineering",

    "AERONAUTICAL":
        "Aeronautical Engineering",

    "AEROSPACE":
        "Aerospace Engineering",

    "BIOTECHNOLOGY":
        "Biotechnology",

    "CHEMICAL":
        "Chemical Engineering",

    "AGRICULTURAL":
        "Agricultural Engineering"
}


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {

        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(124, 58, 237, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(6, 182, 212, 0.12),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #020617 0%,
                #050816 50%,
                #01030a 100%
            ) !important;

        color: #f8fafc !important;
    }


    /* ========================================================
       HEADER
       ======================================================== */

    header[data-testid="stHeader"] {

        background: #020617 !important;

        border-bottom:
            1px solid rgba(139, 92, 246, 0.35) !important;

        z-index: 999999 !important;
    }


    /* ========================================================
       MAIN CONTAINER
       ======================================================== */

    .block-container {

        max-width: 1200px !important;

        padding-top: 3rem !important;

        padding-bottom: 5rem !important;

        position: relative !important;

        z-index: 2 !important;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #020617 0%,
                #030817 55%,
                #01040b 100%
            ) !important;

        border-right:
            1px solid rgba(139, 92, 246, 0.35) !important;
    }


    [data-testid="stSidebar"] > div:first-child {

        background:
            linear-gradient(
                180deg,
                #020617 0%,
                #030817 55%,
                #01040b 100%
            ) !important;
    }


    /* ========================================================
       SIDEBAR NAVIGATION
       ======================================================== */

    [data-testid="stSidebarNav"] {

        display: block !important;

        visibility: visible !important;

        opacity: 1 !important;

        padding:
            12px 10px 8px 10px !important;

        margin-bottom:
            8px !important;
    }


    [data-testid="stSidebarNav"] a {

        display: flex !important;

        align-items: center !important;

        width: 100% !important;

        min-height: 42px !important;

        padding:
            9px 13px !important;

        margin:
            4px 0 !important;

        border-radius:
            11px !important;

        color:
            #e2e8f0 !important;

        background:
            transparent !important;

        border:
            1px solid transparent !important;

        text-decoration:
            none !important;

        transition:
            all 0.25s ease !important;
    }


    [data-testid="stSidebarNav"] a span {

        color:
            #e2e8f0 !important;

        font-size:
            14px !important;

        font-weight:
            600 !important;
    }


    [data-testid="stSidebarNav"] a:hover {

        color:
            #ffffff !important;

        background:
            linear-gradient(
                90deg,
                rgba(168, 85, 247, 0.24),
                rgba(6, 182, 212, 0.10)
            ) !important;

        border:
            1px solid rgba(168, 85, 247, 0.45) !important;

        box-shadow:
            0 0 15px rgba(168, 85, 247, 0.12) !important;
    }


    [data-testid="stSidebarNav"] a[aria-current="page"] {

        color:
            #ffffff !important;

        background:
            linear-gradient(
                90deg,
                rgba(168, 85, 247, 0.30),
                rgba(6, 182, 212, 0.13)
            ) !important;

        border:
            1px solid rgba(168, 85, 247, 0.65) !important;

        box-shadow:
            0 0 18px rgba(168, 85, 247, 0.16) !important;
    }


    [data-testid="stSidebarNav"] a[aria-current="page"] span {

        color:
            #ffffff !important;
    }


    /* ========================================================
       SIDEBAR LOGO
       ======================================================== */

    .sidebar-logo {

        text-align: center;

        padding:
            18px 5px 22px 5px;

        margin:
            4px 5px 18px 5px;

        border-bottom:
            1px solid rgba(139, 92, 246, 0.22);
    }


    .sidebar-logo-icon {

        font-size:
            44px;

        line-height:
            1;

        margin-bottom:
            10px;

        filter:
            drop-shadow(0 0 8px #d946ef)
            drop-shadow(0 0 18px #06b6d4);
    }


    .sidebar-logo-title {

        color:
            #ffffff;

        font-size:
            19px;

        font-weight:
            900;

        letter-spacing:
            1px;

        line-height:
            1.35;
    }


    .sidebar-logo-subtitle {

        color:
            #a78bfa;

        font-size:
            10px;

        letter-spacing:
            2px;

        margin-top:
            7px;
    }


    /* ========================================================
       SIDEBAR SECTIONS
       ======================================================== */

    .sidebar-section {

        color:
            #64748b;

        font-size:
            10px;

        font-weight:
            800;

        letter-spacing:
            2px;

        margin:
            18px 5px 10px 5px;
    }


    .sidebar-card {

        background:
            linear-gradient(
                135deg,
                rgba(168, 85, 247, 0.10),
                rgba(6, 182, 212, 0.05)
            );

        border:
            1px solid rgba(139, 92, 246, 0.30);

        border-radius:
            12px;

        padding:
            14px;

        color:
            #94a3b8;

        font-size:
            12px;

        line-height:
            1.7;
    }


    .sidebar-card-title {

        color:
            #e879f9;

        font-size:
            13px;

        font-weight:
            800;

        margin-bottom:
            8px;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {

        width:
            100%;

        box-sizing:
            border-box;

        padding:
            34px 35px 32px 35px;

        margin:
            0 0 24px 0;

        border-radius:
            22px;

        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(168, 85, 247, 0.18),
                transparent 55%
            ),
            linear-gradient(
                135deg,
                rgba(8, 15, 40, 0.96),
                rgba(4, 11, 27, 0.96)
            );

        border:
            1px solid rgba(139, 92, 246, 0.42);

        box-shadow:
            0 0 35px rgba(139, 92, 246, 0.08);

        text-align:
            center;
    }


    .hero-icon {

        font-size:
            50px;

        line-height:
            1;

        margin-bottom:
            14px;

        filter:
            drop-shadow(0 0 8px #d946ef)
            drop-shadow(0 0 18px #06b6d4);
    }


    .hero-title {

        color:
            #f8fafc;

        font-size:
            38px;

        font-weight:
            900;

        letter-spacing:
            1px;

        line-height:
            1.15;

        margin-bottom:
            13px;
    }


    .gradient-text {

        background:
            linear-gradient(
                90deg,
                #d946ef,
                #a855f7,
                #6366f1,
                #06b6d4,
                #22d3ee
            );

        -webkit-background-clip:
            text;

        -webkit-text-fill-color:
            transparent;
    }


    .hero-subtitle {

        color:
            #94a3b8;

        font-size:
            14px;

        line-height:
            1.75;

        max-width:
            850px;

        margin:
            auto;
    }


    .neon-text {

        color:
            #22d3ee;

        font-weight:
            700;
    }


    /* ========================================================
       FORM SECTION
       ======================================================== */

    .section-card {

        width:
            100%;

        box-sizing:
            border-box;

        padding:
            26px 28px;

        margin-bottom:
            22px;

        border-radius:
            18px;

        background:
            linear-gradient(
                135deg,
                rgba(8, 15, 35, 0.96),
                rgba(4, 10, 25, 0.96)
            );

        border:
            1px solid rgba(139, 92, 246, 0.34);

        box-shadow:
            0 0 25px rgba(99, 102, 241, 0.05);
    }


    .section-title {

        color:
            #f8fafc;

        font-size:
            21px;

        font-weight:
            800;

        margin-bottom:
            6px;
    }


    .section-description {

        color:
            #94a3b8;

        font-size:
            13px;

        line-height:
            1.7;
    }


    /* ========================================================
       LABELS
       ======================================================== */

    label,
    [data-testid="stWidgetLabel"] p {

        color:
            #cbd5e1 !important;

        font-weight:
            650 !important;

        font-size:
            14px !important;
    }


    /* ========================================================
       IMPORTANT INPUT FIX
       TEXT INPUT + NUMBER INPUT
       ======================================================== */

    /*
       Main input containers
    */

    [data-testid="stTextInput"] div[data-baseweb="input"],
    [data-testid="stNumberInput"] div[data-baseweb="input"] {

        background:
            #070d20 !important;

        background-color:
            #070d20 !important;

        border:
            1px solid rgba(139, 92, 246, 0.48) !important;

        border-radius:
            12px !important;

        box-shadow:
            none !important;
    }


    /*
       Inner input wrappers
    */

    [data-testid="stTextInput"] div[data-baseweb="input"] > div,
    [data-testid="stNumberInput"] div[data-baseweb="input"] > div {

        background:
            #070d20 !important;

        background-color:
            #070d20 !important;

        border:
            none !important;

        box-shadow:
            none !important;
    }


    /*
       Actual text fields
    */

    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input {

        background:
            #070d20 !important;

        background-color:
            #070d20 !important;

        color:
            #f8fafc !important;

        -webkit-text-fill-color:
            #f8fafc !important;

        caret-color:
            #22d3ee !important;

        border:
            none !important;

        outline:
            none !important;

        box-shadow:
            none !important;
    }


    /*
       Placeholder text
    */

    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stNumberInput"] input::placeholder {

        color:
            #64748b !important;

        opacity:
            1 !important;

        -webkit-text-fill-color:
            #64748b !important;
    }


    /*
       Chrome / Edge autofill fix
       This prevents the white background when
       the browser fills "Madhu" or other values.
    */

    [data-testid="stTextInput"] input:-webkit-autofill,
    [data-testid="stTextInput"] input:-webkit-autofill:hover,
    [data-testid="stTextInput"] input:-webkit-autofill:focus,
    [data-testid="stNumberInput"] input:-webkit-autofill,
    [data-testid="stNumberInput"] input:-webkit-autofill:hover,
    [data-testid="stNumberInput"] input:-webkit-autofill:focus {

        -webkit-box-shadow:
            0 0 0 1000px #070d20 inset !important;

        box-shadow:
            0 0 0 1000px #070d20 inset !important;

        -webkit-text-fill-color:
            #f8fafc !important;

        background-color:
            #070d20 !important;

        color:
            #f8fafc !important;

        caret-color:
            #22d3ee !important;
    }


    /*
       Focus state
    */

    [data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
    [data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within {

        border-color:
            #d946ef !important;

        box-shadow:
            0 0 15px rgba(217, 70, 239, 0.15) !important;
    }


    /* ========================================================
       NUMBER INPUT +/- BUTTONS
       ======================================================== */

    [data-testid="stNumberInput"] button {

        background:
            #070d20 !important;

        background-color:
            #070d20 !important;

        color:
            #cbd5e1 !important;

        border:
            none !important;
    }


    [data-testid="stNumberInput"] button:hover {

        background:
            rgba(124, 58, 237, 0.20) !important;

        color:
            #22d3ee !important;
    }


    /* ========================================================
       SELECT BOXES
       ======================================================== */

    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {

        background:
            #070d20 !important;

        background-color:
            #070d20 !important;

        border:
            1px solid rgba(139, 92, 246, 0.48) !important;

        border-radius:
            12px !important;

        color:
            #f8fafc !important;
    }


    [data-testid="stSelectbox"] div[data-baseweb="select"] span {

        color:
            #f8fafc !important;
    }


    [data-testid="stSelectbox"] svg {

        color:
            #22d3ee !important;

        fill:
            #22d3ee !important;
    }


    /* ========================================================
       DATASET INFORMATION
       ======================================================== */

    .dataset-info {

        color:
            #94a3b8;

        font-size:
            12px;

        margin-top:
            6px;

        padding-left:
            3px;
    }


    .dataset-info span {

        color:
            #22d3ee;

        font-weight:
            700;
    }


    /* ========================================================
       MAIN BUTTON
       ======================================================== */

    .stButton > button {

        width:
            100% !important;

        min-height:
            48px !important;

        border-radius:
            12px !important;

        border:
            1px solid rgba(168, 85, 247, 0.55) !important;

        background:
            linear-gradient(
                90deg,
                #7c3aed,
                #6366f1,
                #0891b2
            ) !important;

        color:
            #ffffff !important;

        font-size:
            14px !important;

        font-weight:
            800 !important;

        box-shadow:
            0 0 20px rgba(124, 58, 237, 0.18) !important;

        transition:
            all 0.25s ease !important;
    }


    .stButton > button:hover {

        transform:
            translateY(-1px);

        border-color:
            #22d3ee !important;

        box-shadow:
            0 0 25px rgba(34, 211, 238, 0.22) !important;
    }


    /* ========================================================
       RESULTS HEADER
       ======================================================== */

    .results-header {

        display:
            flex;

        align-items:
            center;

        justify-content:
            space-between;

        gap:
            15px;

        margin:
            25px 0 15px 0;
    }


    .results-title {

        color:
            #f8fafc;

        font-size:
            23px;

        font-weight:
            850;
    }


    .results-count {

        color:
            #22d3ee;

        font-size:
            13px;

        font-weight:
            750;

        background:
            rgba(34, 211, 238, 0.08);

        border:
            1px solid rgba(34, 211, 238, 0.22);

        padding:
            7px 12px;

        border-radius:
            20px;
    }


    /* ========================================================
       COLLEGE CARDS
       ======================================================== */

    .college-card {

        background:
            linear-gradient(
                135deg,
                rgba(8, 15, 35, 0.98),
                rgba(4, 10, 25, 0.98)
            );

        border:
            1px solid rgba(99, 102, 241, 0.30);

        border-radius:
            16px;

        padding:
            20px;

        margin-bottom:
            14px;

        box-shadow:
            0 0 22px rgba(99, 102, 241, 0.05);

        transition:
            all 0.2s ease;
    }


    .college-card:hover {

        border-color:
            rgba(168, 85, 247, 0.65);

        box-shadow:
            0 0 25px rgba(168, 85, 247, 0.10);
    }


    .college-rank {

        color:
            #22d3ee;

        font-size:
            12px;

        font-weight:
            800;

        letter-spacing:
            1px;

        margin-bottom:
            7px;
    }


    .college-name {

        color:
            #f8fafc;

        font-size:
            17px;

        font-weight:
            800;

        line-height:
            1.45;

        margin-bottom:
            8px;
    }


    .college-details {

        color:
            #94a3b8;

        font-size:
            12px;

        line-height:
            1.7;
    }


    .college-details strong {

        color:
            #cbd5e1;
    }


    .chance {

        display:
            inline-block;

        margin-top:
            10px;

        padding:
            6px 10px;

        border-radius:
            20px;

        font-size:
            11px;

        font-weight:
            800;

        background:
            rgba(124, 58, 237, 0.13);

        border:
            1px solid rgba(124, 58, 237, 0.35);

        color:
            #c4b5fd;
    }


    /* ========================================================
       EMPTY RESULT
       ======================================================== */

    .empty-card {

        text-align:
            center;

        padding:
            35px 25px;

        border-radius:
            16px;

        background:
            rgba(8, 15, 35, 0.90);

        border:
            1px solid rgba(139, 92, 246, 0.28);
    }


    .empty-icon {

        font-size:
            38px;

        margin-bottom:
            10px;
    }


    .empty-title {

        color:
            #f8fafc;

        font-size:
            18px;

        font-weight:
            800;

        margin-bottom:
            8px;
    }


    .empty-text {

        color:
            #94a3b8;

        font-size:
            13px;

        line-height:
            1.7;
    }


    /* ========================================================
       NOTICE
       ======================================================== */

    .notice {

        margin-top:
            25px;

        padding:
            15px 18px;

        border-radius:
            12px;

        background:
            rgba(234, 179, 8, 0.06);

        border:
            1px solid rgba(234, 179, 8, 0.22);

        color:
            #aeb7c7;

        font-size:
            11px;

        line-height:
            1.7;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 800px) {

        .block-container {

            padding-top:
                2rem !important;
        }


        .hero {

            padding:
                27px 18px;
        }


        .hero-title {

            font-size:
                28px;
        }


        .hero-subtitle {

            font-size:
                13px;
        }


        .section-card {

            padding:
                20px 16px;
        }


        .results-header {

            align-items:
                flex-start;

            flex-direction:
                column;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
        <div class="sidebar-logo">

            <div class="sidebar-logo-icon">
                🎓
            </div>

            <div class="sidebar-logo-title">
                COLLEGE<br>
                ASSISTANT
            </div>

            <div class="sidebar-logo-subtitle">
                AI COLLEGE GUIDE
            </div>

        </div>
        """
    )


    st.html(
        """
        <div class="sidebar-section">
            RECOMMENDATION SYSTEM
        </div>
        """
    )


    st.html(
        """
        <div class="sidebar-card">

            <div class="sidebar-card-title">
                🎯 FIND YOUR COLLEGE
            </div>

            Enter your TNEA details to discover
            colleges that match your cutoff,
            category, district and preferred branch.

        </div>
        """
    )


    st.html(
        """
        <div class="sidebar-section">
            HOW IT WORKS
        </div>

        <div class="sidebar-card">

            <div style="color:#cbd5e1;margin-bottom:6px;">
                01 · Enter your cutoff
            </div>

            <div style="color:#cbd5e1;margin-bottom:6px;">
                02 · Select your category
            </div>

            <div style="color:#cbd5e1;margin-bottom:6px;">
                03 · Choose district
            </div>

            <div style="color:#cbd5e1;">
                04 · Select your branch
            </div>

        </div>
        """
    )


# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div class="hero">

        <div class="hero-icon">
            🎓
        </div>

        <div class="hero-title">
            FIND YOUR
            <span class="gradient-text">
                BEST-FIT COLLEGE
            </span>
        </div>

        <div class="hero-subtitle">
            Get personalized college recommendations using your
            <span class="neon-text">TNEA cutoff</span>,
            category, district and preferred engineering branch.
        </div>

    </div>
    """
)


# ============================================================
# DATA ERROR
# ============================================================

if DATA_ERROR:

    st.html(
        f"""
        <div class="empty-card">

            <div class="empty-icon">
                ⚠️
            </div>

            <div class="empty-title">
                Dataset could not be loaded
            </div>

            <div class="empty-text">
                {DATA_ERROR}
                <br><br>
                Please make sure your
                <b>college_cutoffs.xlsx</b>
                or
                <b>college_cutoffs.csv</b>
                exists inside the
                <b>data</b> folder.
            </div>

        </div>
        """
    )

    st.stop()


# ============================================================
# DISTRICTS
# ============================================================

if "District" in df.columns:

    districts = (
        df["District"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    districts = sorted(
        [
            d
            for d in districts.unique()
            if d and d.lower() != "not specified"
        ]
    )

else:

    districts = []


# ============================================================
# FORM HEADER
# ============================================================

st.html(
    """
    <div class="section-card">

        <div class="section-title">
            📋 Enter Your TNEA Details
        </div>

        <div class="section-description">
            Enter your details below to find colleges that
            best match your cutoff and preferences.
        </div>

    </div>
    """
)


# ============================================================
# STUDENT NAME + CUTOFF
# ============================================================

col1, col2 = st.columns(
    [1, 1],
    gap="large"
)


with col1:

    student_name = st.text_input(
        "Student Name",
        placeholder="Enter your name",
        key="student_name"
    )


with col2:

    cutoff = st.number_input(
        "TNEA Cutoff",
        min_value=0.0,
        max_value=200.0,
        value=180.0,
        step=0.5,
        help="Enter your TNEA cutoff out of 200.",
        key="student_cutoff"
    )


# ============================================================
# DISTRICT + CATEGORY
# ============================================================

col3, col4 = st.columns(
    [1, 1],
    gap="large"
)


with col3:

    selected_district = st.selectbox(
        "Preferred District",
        options=["All Districts"] + districts,
        index=0,
        key="selected_district"
    )


with col4:

    selected_category = st.selectbox(
        "Community Category",
        options=CATEGORIES,
        index=0,
        key="selected_category"
    )


# ============================================================
# BRANCH
# ============================================================

branch_options = [
    f"{branch} — {BRANCH_DISPLAY[branch]}"
    for branch in BRANCHES
]


selected_branch_display = st.selectbox(
    "Preferred Engineering Branch",
    options=branch_options,
    index=0,
    key="selected_branch"
)


selected_branch = selected_branch_display.split(
    " — ",
    1
)[0]


# ============================================================
# DATASET INFORMATION
# ============================================================

district_count = len(districts)


st.html(
    f"""
    <div class="dataset-info">

        📍 <span>{district_count}</span>
        districts available from the dataset

        &nbsp;•&nbsp;

        📊 <span>{len(df):,}</span>
        dataset rows

    </div>
    """
)


st.write("")


# ============================================================
# RECOMMEND BUTTON
# ============================================================

_, button_col, _ = st.columns(
    [1, 1.4, 1]
)


with button_col:

    find_colleges = st.button(
        "🔍  FIND MY BEST-FIT COLLEGES",
        use_container_width=True
    )


# ============================================================
# RECOMMENDATIONS
# ============================================================

if find_colleges:

    try:

        district_for_engine = (
            ""
            if selected_district == "All Districts"
            else selected_district
        )


        results = recommend(
            cutoff=cutoff,
            category=selected_category,
            district=district_for_engine,
            branch=selected_branch,
            limit=None
        )


    except Exception as e:

        results = []


        st.html(
            f"""
            <div class="empty-card">

                <div class="empty-icon">
                    ⚠️
                </div>

                <div class="empty-title">
                    Something went wrong
                </div>

                <div class="empty-text">
                    {str(e)}
                </div>

            </div>
            """
        )


    # ========================================================
    # RESULTS
    # ========================================================

    if results:

        st.html(
            f"""
            <div class="results-header">

                <div class="results-title">
                    🎯 Recommended Colleges
                </div>

                <div class="results-count">
                    {len(results)} matching colleges
                </div>

            </div>
            """
        )


        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        district_text = (
            "All Districts"
            if selected_district == "All Districts"
            else selected_district
        )


        student_text = (
            student_name.strip()
            if student_name.strip()
            else "Student"
        )


        st.html(
            f"""
            <div class="section-card">

                <div style="
                    color:#cbd5e1;
                    font-size:13px;
                    line-height:1.8;
                ">

                    <b style="color:#f8fafc;">
                        👤 {student_text}
                    </b>

                    &nbsp;&nbsp;•&nbsp;&nbsp;

                    Cutoff:

                    <span style="
                        color:#22d3ee;
                        font-weight:800;
                    ">
                        {cutoff:.2f}
                    </span>

                    &nbsp;&nbsp;•&nbsp;&nbsp;

                    Category:

                    <span style="
                        color:#c4b5fd;
                        font-weight:800;
                    ">
                        {selected_category}
                    </span>

                    &nbsp;&nbsp;•&nbsp;&nbsp;

                    District:

                    <span style="
                        color:#c4b5fd;
                        font-weight:800;
                    ">
                        {district_text}
                    </span>

                    <br>

                    Branch:

                    <span style="
                        color:#22d3ee;
                        font-weight:800;
                    ">
                        {BRANCH_DISPLAY.get(
                            selected_branch,
                            selected_branch
                        )}
                    </span>

                </div>

            </div>
            """
        )


        # ----------------------------------------------------
        # COLLEGE CARDS
        # ----------------------------------------------------

        for result in results:

            college_name = result.get(
                "college_name",
                "College"
            )


            district = result.get(
                "district",
                "Not specified"
            )


            branch = result.get(
                "branch",
                "Not specified"
            )


            previous_cutoff = result.get(
                "cutoff",
                None
            )


            chance = result.get(
                "chance",
                "Data unavailable"
            )


            difference = result.get(
                "cutoff_difference",
                None
            )


            if previous_cutoff is not None:

                cutoff_text = (
                    f"{float(previous_cutoff):.2f}"
                )

            else:

                cutoff_text = "N/A"


            if difference is not None:

                difference_text = (
                    f"{float(difference):+.2f}"
                )

            else:

                difference_text = "N/A"


            st.html(
                f"""
                <div class="college-card">

                    <div class="college-rank">
                        RECOMMENDATION #
                        {result.get("rank", "-")}
                    </div>

                    <div class="college-name">
                        🏫 {college_name}
                    </div>

                    <div class="college-details">

                        <strong>📍 District:</strong>
                        {district}

                        <br>

                        <strong>🎓 Branch:</strong>
                        {branch}

                        <br>

                        <strong>📊 Previous Cutoff:</strong>
                        {cutoff_text}

                        <br>

                        <strong>
                            📈 Your Cutoff Difference:
                        </strong>

                        {difference_text}

                        <br>

                        <span class="chance">
                            Chance: {chance}
                        </span>

                    </div>

                </div>
                """
            )


    else:

        # ====================================================
        # NO RESULTS
        # ====================================================

        st.html(
            """
            <div class="empty-card">

                <div class="empty-icon">
                    🔎
                </div>

                <div class="empty-title">
                    No Matching Colleges Found
                </div>

                <div class="empty-text">

                    We couldn't find colleges matching all
                    the selected criteria.

                    <br><br>

                    Try selecting
                    <b>All Districts</b>,
                    another branch, or check your cutoff
                    and category.

                </div>

            </div>
            """
        )


# ============================================================
# DISCLAIMER
# ============================================================

st.html(
    """
    <div class="notice">

        ⚠️ <b>Important:</b>

        Recommendations are based on historical cutoff data
        available in the project dataset. They are intended only
        as guidance and do not guarantee admission.

        Actual TNEA allotment depends on official counselling,
        rank, category, choices, seat availability and other
        factors.

    </div>
    """
)