import streamlit as st
import pandas as pd


# ============================================================
# CHATBOT IMPORT
# ============================================================

try:
    from chatbot_engine import answer_question

except Exception as e:

    answer_question = None

    IMPORT_ERROR = str(e)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="College Assistant Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# FUTURISTIC NEON CSS
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

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


/* =========================================================
   HEADER
   ========================================================= */

header[data-testid="stHeader"] {

    background:
        #020617 !important;

    border-bottom:
        1px solid rgba(139, 92, 246, 0.35) !important;

    z-index:
        999999 !important;
}


/* =========================================================
   MAIN CONTAINER
   ========================================================= */

.block-container {

    max-width:
        1200px !important;

    padding-top:
        3.5rem !important;

    padding-bottom:
        8rem !important;

    position:
        relative !important;

    z-index:
        2 !important;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

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

    z-index:
        999998 !important;
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


/* =========================================================
   SIDEBAR NAVIGATION
   ========================================================= */

[data-testid="stSidebarNav"] {

    display:
        block !important;

    visibility:
        visible !important;

    opacity:
        1 !important;

    padding:
        12px 10px 8px 10px !important;

    margin-bottom:
        8px !important;
}


[data-testid="stSidebarNav"] * {

    visibility:
        visible !important;

    opacity:
        1 !important;
}


[data-testid="stSidebarNav"] a {

    display:
        flex !important;

    align-items:
        center !important;

    width:
        100% !important;

    min-height:
        42px !important;

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


/* =========================================================
   SIDEBAR LOGO
   ========================================================= */

.sidebar-logo {

    text-align:
        center;

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


.sidebar-example {

    color:
        #94a3b8;

    font-size:
        11px;

    line-height:
        1.9;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {

    width:
        100%;

    box-sizing:
        border-box;

    padding:
        30px;

    margin:
        0 0 22px 0;

    border-radius:
        20px;

    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(168, 85, 247, 0.15),
            transparent 55%
        ),
        rgba(2, 6, 23, 0.86);

    border:
        1px solid rgba(139, 92, 246, 0.42);

    box-shadow:
        0 0 35px rgba(139, 92, 246, 0.08);

    text-align:
        center;
}


.hero-icon {

    font-size:
        48px;

    margin-bottom:
        12px;

    filter:
        drop-shadow(0 0 8px #d946ef)
        drop-shadow(0 0 18px #06b6d4);
}


.hero-title {

    color:
        #f8fafc;

    font-size:
        39px;

    font-weight:
        900;

    letter-spacing:
        1px;

    line-height:
        1.15;

    margin-bottom:
        12px;
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
        1.7;

    max-width:
        900px;

    margin:
        auto;
}


/* =========================================================
   WELCOME
   ========================================================= */

.welcome-card {

    padding:
        24px 28px;

    margin-bottom:
        24px;

    border-radius:
        16px;

    background:
        linear-gradient(
            135deg,
            rgba(124, 58, 237, 0.12),
            rgba(6, 182, 212, 0.06)
        );

    border:
        1px solid rgba(139, 92, 246, 0.34);

    box-shadow:
        0 0 25px rgba(99, 102, 241, 0.06);
}


.welcome-title {

    color:
        #f8fafc;

    font-size:
        20px;

    font-weight:
        800;

    margin-bottom:
        12px;
}


.welcome-text {

    color:
        #94a3b8;

    font-size:
        14px;

    line-height:
        1.75;
}


.welcome-text b {

    color:
        #22d3ee;
}


/* =========================================================
   SECTION LABEL
   ========================================================= */

.section-label {

    color:
        #94a3b8;

    font-size:
        11px;

    font-weight:
        800;

    letter-spacing:
        1.7px;

    margin:
        20px 0 10px 0;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {

    background:
        linear-gradient(
            135deg,
            rgba(9, 17, 38, 0.96),
            rgba(7, 13, 30, 0.96)
        ) !important;

    color:
        #cbd5e1 !important;

    border:
        1px solid rgba(139, 92, 246, 0.40) !important;

    border-radius:
        10px !important;

    min-height:
        45px !important;

    font-weight:
        600 !important;
}


.stButton > button:hover {

    color:
        #ffffff !important;

    border-color:
        #d946ef !important;

    box-shadow:
        0 0 18px rgba(217, 70, 239, 0.18) !important;
}


/* =========================================================
   CHAT MESSAGES
   ========================================================= */

[data-testid="stChatMessage"] {

    background:
        linear-gradient(
            135deg,
            rgba(7, 13, 32, 0.92),
            rgba(4, 10, 24, 0.96)
        ) !important;

    border:
        1px solid rgba(99, 102, 241, 0.28) !important;

    border-radius:
        15px !important;

    margin-bottom:
        14px !important;
}


[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {

    color:
        #cbd5e1 !important;

    line-height:
        1.65 !important;
}


/* =========================================================
   RECOMMENDATION RESULTS
   ========================================================= */

.results-wrapper {

    margin:
        24px 0 28px 0;
}


.results-header {

    display:
        flex;

    justify-content:
        space-between;

    align-items:
        center;

    margin-bottom:
        14px;

    gap:
        15px;
}


.results-title {

    color:
        #f8fafc;

    font-size:
        21px;

    font-weight:
        850;
}


.results-count {

    color:
        #22d3ee;

    background:
        rgba(34, 211, 238, 0.08);

    border:
        1px solid rgba(34, 211, 238, 0.25);

    padding:
        6px 12px;

    border-radius:
        20px;

    font-size:
        12px;

    font-weight:
        800;

    white-space:
        nowrap;
}


.recommendation-card {

    width:
        100%;

    box-sizing:
        border-box;

    padding:
        19px 20px;

    margin-bottom:
        12px;

    border-radius:
        15px;

    background:
        linear-gradient(
            135deg,
            rgba(8, 15, 35, 0.98),
            rgba(4, 10, 25, 0.98)
        );

    border:
        1px solid rgba(99, 102, 241, 0.32);

    box-shadow:
        0 0 20px rgba(99, 102, 241, 0.05);

    transition:
        all 0.25s ease;
}


.recommendation-card:hover {

    border-color:
        rgba(168, 85, 247, 0.70);

    box-shadow:
        0 0 25px rgba(168, 85, 247, 0.12);

    transform:
        translateY(-1px);
}


.recommendation-rank {

    color:
        #22d3ee;

    font-size:
        11px;

    font-weight:
        850;

    letter-spacing:
        1.2px;

    margin-bottom:
        6px;
}


.recommendation-name {

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


.recommendation-info {

    color:
        #94a3b8;

    font-size:
        12px;

    line-height:
        1.85;
}


.recommendation-info strong {

    color:
        #cbd5e1;
}


.chance-badge {

    display:
        inline-block;

    margin-top:
        9px;

    padding:
        5px 10px;

    border-radius:
        20px;

    color:
        #c4b5fd;

    background:
        rgba(124, 58, 237, 0.13);

    border:
        1px solid rgba(124, 58, 237, 0.38);

    font-size:
        11px;

    font-weight:
        800;
}


/* =========================================================
   CHAT INPUT
   ========================================================= */

[data-testid="stBottom"] {

    background:
        #020617 !important;

    background-color:
        #020617 !important;

    border-top:
        1px solid rgba(139, 92, 246, 0.25) !important;

    box-shadow:
        none !important;

    z-index:
        999999 !important;
}


[data-testid="stBottom"] > div {

    background:
        #020617 !important;

    background-color:
        #020617 !important;

    box-shadow:
        none !important;
}


[data-testid="stBottomBlockContainer"] {

    background:
        #020617 !important;

    background-color:
        #020617 !important;

    box-shadow:
        none !important;
}


[data-testid="stChatInput"] {

    background:
        transparent !important;

    border:
        none !important;

    box-shadow:
        none !important;

    padding:
        0 !important;
}


[data-testid="stChatInput"] > div {

    background:
        #070d20 !important;

    background-color:
        #070d20 !important;

    border:
        1px solid rgba(139, 92, 246, 0.55) !important;

    border-radius:
        16px !important;

    box-shadow:
        0 0 18px rgba(99, 102, 241, 0.08) !important;

    min-height:
        52px !important;
}


[data-testid="stChatInput"] div[data-baseweb="textarea"] {

    background:
        #070d20 !important;

    background-color:
        #070d20 !important;

    border:
        none !important;

    box-shadow:
        none !important;
}


[data-testid="stChatInput"] div[data-baseweb="textarea"] > div {

    background:
        #070d20 !important;

    background-color:
        #070d20 !important;

    border:
        none !important;

    box-shadow:
        none !important;
}


[data-testid="stChatInput"] textarea {

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

    font-size:
        15px !important;
}


[data-testid="stChatInput"] textarea:focus {

    color:
        #ffffff !important;

    -webkit-text-fill-color:
        #ffffff !important;

    caret-color:
        #22d3ee !important;

    outline:
        none !important;
}


[data-testid="stChatInput"] textarea::placeholder {

    color:
        #64748b !important;

    opacity:
        1 !important;
}


[data-testid="stChatInput"] button {

    color:
        #22d3ee !important;

    background:
        transparent !important;

    border:
        none !important;

    box-shadow:
        none !important;
}


[data-testid="stChatInput"] button:hover {

    color:
        #67e8f9 !important;

    background:
        rgba(34, 211, 238, 0.08) !important;

    border-radius:
        10px !important;
}


[data-testid="stChatInput"] button svg {

    color:
        #22d3ee !important;

    fill:
        #22d3ee !important;

    stroke:
        #22d3ee !important;
}


[data-testid="stChatInput"]:focus-within > div {

    border-color:
        #d946ef !important;

    box-shadow:
        0 0 20px rgba(217, 70, 239, 0.15),
        0 0 30px rgba(6, 182, 212, 0.05) !important;
}


/* =========================================================
   SCROLLBAR
   ========================================================= */

::-webkit-scrollbar {

    width:
        8px;

    height:
        8px;
}


::-webkit-scrollbar-track {

    background:
        #020617;
}


::-webkit-scrollbar-thumb {

    background:
        linear-gradient(
            180deg,
            #7c3aed,
            #06b6d4
        );

    border-radius:
        10px;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 800px) {

    .block-container {

        padding-top:
            2.5rem !important;
    }


    .hero-title {

        font-size:
            28px;
    }


    .hero {

        padding:
            24px 18px;
    }


    .results-header {

        align-items:
            flex-start;

        flex-direction:
            column;
    }


    [data-testid="stChatInput"] > div {

        border-radius:
            13px !important;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


if "quick_question" not in st.session_state:

    st.session_state.quick_question = None


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
            NAVIGATION
        </div>
        """
    )


    st.html(
        """
        <div class="sidebar-card">

            <div class="sidebar-card-title">
                💬 MAIN CHATBOT
            </div>

            Ask questions about:

            <br>• TNEA
            <br>• Colleges
            <br>• Cutoffs
            <br>• Engineering branches
            <br>• Counselling

        </div>
        """
    )


    st.html(
        """
        <div class="sidebar-section">
            EXAMPLES
        </div>

        <div class="sidebar-example">

            💡 What is TNEA?

            <br>

            💻 CSE vs AI & DS?

            <br>

            📊 Which branch is best?

            <br>

            🏫 What colleges can I get?

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

            COLLEGE

            <span class="gradient-text">
                ASSISTANT
            </span>

        </div>

        <div class="hero-subtitle">

            Your AI-powered guide for

            <b style="color:#22d3ee;">
                TNEA
            </b>,

            colleges, cutoffs,
            engineering branches,
            counselling and admissions.

        </div>

    </div>
    """
)


# ============================================================
# WELCOME CARD
# ============================================================

if len(st.session_state.messages) == 0:

    st.html(
        """
        <div class="welcome-card">

            <div class="welcome-title">
                🤖 Welcome to College Assistant
            </div>

            <div class="welcome-text">

                Hi! 👋 I'm your College Assistant.

                <br><br>

                Ask me anything about TNEA,
                colleges, cutoffs,
                engineering branches and counselling.

                <br><br>

                You can also give your requirements:

                <br><br>

                <b>
                "My cutoff is 180.
                I am OC.
                I want CSE in Chennai."
                </b>

            </div>

        </div>
        """
    )


# ============================================================
# DISPLAY CHAT HISTORY + SAVED RECOMMENDATIONS
# ============================================================

for message in st.session_state.messages:

    role = message.get(
        "role",
        "assistant"
    )

    content = message.get(
        "content",
        ""
    )

    recommendations = message.get(
        "recommendations",
        []
    )


    with st.chat_message(
        role,
        avatar=(
            "👤"
            if role == "user"
            else "🤖"
        )
    ):

        st.markdown(content)


        # ====================================================
        # DISPLAY COLLEGE RECOMMENDATIONS
        # ====================================================

        if (
            role == "assistant"
            and recommendations
        ):

            st.html(
                f"""
                <div class="results-wrapper">

                    <div class="results-header">

                        <div class="results-title">
                            🎯 Recommended Colleges
                        </div>

                        <div class="results-count">
                            {len(recommendations)}
                            matching colleges
                        </div>

                    </div>

                </div>
                """
            )


            for college in recommendations:

                rank = college.get(
                    "rank",
                    "-"
                )


                college_name = college.get(
                    "college_name",
                    "College"
                )


                location = college.get(
                    "location",
                    "Not specified"
                )


                branch = college.get(
                    "branch",
                    "Not specified"
                )


                cutoff = college.get(
                    "cutoff",
                    None
                )


                chance = college.get(
                    "chance",
                    "Data unavailable"
                )


                difference = college.get(
                    "cutoff_difference",
                    None
                )


                if cutoff is not None:

                    cutoff_text = (
                        f"{float(cutoff):.2f}"
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
                    <div class="recommendation-card">

                        <div class="recommendation-rank">

                            RECOMMENDATION #{rank}

                        </div>


                        <div class="recommendation-name">

                            🏫 {college_name}

                        </div>


                        <div class="recommendation-info">

                            <strong>
                                📍 Location:
                            </strong>

                            {location}

                            <br>


                            <strong>
                                🎓 Branch:
                            </strong>

                            {branch}

                            <br>


                            <strong>
                                📊 Previous Cutoff:
                            </strong>

                            {cutoff_text}

                            <br>


                            <strong>
                                📈 Cutoff Difference:
                            </strong>

                            {difference_text}

                            <br>


                            <span class="chance-badge">

                                Chance:
                                {chance}

                            </span>

                        </div>

                    </div>
                    """
                )


# ============================================================
# RECOMMENDED QUESTIONS
# ============================================================

st.html(
    """
    <div class="section-label">

        ⚡ RECOMMENDED QUESTIONS

    </div>
    """
)


questions = [

    "What is TNEA?",

    "CSE vs AI & DS?",

    "Which branch is best?",

    "What colleges can I get?"

]


columns = st.columns(4)


for index, question in enumerate(questions):

    with columns[index]:

        if st.button(
            question,
            key=f"question_{index}",
            use_container_width=True
        ):

            st.session_state.quick_question = question

            st.rerun()


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Ask about colleges, TNEA, cutoffs, branches..."
)


# ============================================================
# QUICK QUESTION
# ============================================================

if st.session_state.quick_question:

    user_input = st.session_state.quick_question

    st.session_state.quick_question = None


# ============================================================
# PROCESS USER QUESTION
# ============================================================

if user_input:

    user_input = user_input.strip()


    if user_input:

        # ----------------------------------------------------
        # SAVE USER MESSAGE
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role":
                    "user",

                "content":
                    user_input
            }
        )


        # ----------------------------------------------------
        # GET ANSWER + RECOMMENDATIONS
        # ----------------------------------------------------

        reply = ""

        recommendations = []


        if answer_question is not None:

            try:

                result = answer_question(
                    user_input,
                    st.session_state.messages
                )


                # =================================================
                # IMPORTANT:
                # answer_question RETURNS:
                #
                # (reply, recommendations)
                # =================================================

                if isinstance(
                    result,
                    tuple
                ):

                    reply = result[0]

                    if len(result) > 1:

                        recommendations = (
                            result[1]
                            or []
                        )


                elif isinstance(
                    result,
                    dict
                ):

                    reply = result.get(
                        "answer",
                        result.get(
                            "response",
                            ""
                        )
                    )

                    recommendations = (
                        result.get(
                            "recommendations",
                            []
                        )
                        or []
                    )


                else:

                    reply = str(result)


            except Exception as e:

                reply = (
                    "Sorry, I couldn't process "
                    "your question."
                )

                recommendations = []

                print(
                    "CHATBOT ERROR:",
                    repr(e)
                )


        else:

            reply = (
                "Chatbot engine could not be loaded."
            )


        # ----------------------------------------------------
        # SAVE ASSISTANT RESPONSE + RECOMMENDATIONS
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role":
                    "assistant",

                "content":
                    reply,

                "recommendations":
                    recommendations
            }
        )


        # ----------------------------------------------------
        # RERUN
        # ----------------------------------------------------

        st.rerun()