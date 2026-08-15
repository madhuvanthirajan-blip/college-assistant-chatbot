import streamlit as st
import pandas as pd


# ============================================================
# IMPORT YOUR EXISTING CHATBOT ENGINE
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
# COLORS
# ============================================================

BACKGROUND = "#F6F3FB"
BORDER = "#DED6EC"
TEXT = "#30303A"
SECONDARY = "#777780"
PURPLE = "#5533A8"


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main,
.block-container {
    background-color: #F6F3FB !important;
}


/* ----------------------------------------------------------
   STREAMLIT TOP HEADER
   This makes the area around Deploy the same color.
   ---------------------------------------------------------- */

header,
[data-testid="stHeader"],
[data-testid="stToolbar"] {
    background-color: #F6F3FB !important;
}


/* ----------------------------------------------------------
   SIDEBAR
   ---------------------------------------------------------- */

[data-testid="stSidebar"] {
    background-color: #F6F3FB !important;
    border-right: 1px solid #DED6EC !important;
}

[data-testid="stSidebar"] > div:first-child {
    background-color: #F6F3FB !important;
}

[data-testid="stSidebar"] .block-container {
    background-color: #F6F3FB !important;
}


/* ----------------------------------------------------------
   MAIN CONTENT
   ---------------------------------------------------------- */

.block-container {
    max-width: 1200px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 6rem !important;
}


/* ----------------------------------------------------------
   CHAT MESSAGES
   ---------------------------------------------------------- */

[data-testid="stChatMessage"] {
    background-color: #F6F3FB !important;
    border: 1px solid #DED6EC !important;
    border-radius: 16px !important;
    margin-bottom: 14px !important;
    padding: 14px !important;
}


/* ----------------------------------------------------------
   CHAT INPUT
   ---------------------------------------------------------- */

/* ----------------------------------------------------------
   CHAT INPUT + FIXED BOTTOM AREA
   Keep the entire chat-input area the same background
   as the rest of the application.
   ---------------------------------------------------------- */

[data-testid="stBottom"] {
    background-color: #F6F3FB !important;
    background: #F6F3FB !important;
}

[data-testid="stBottom"] > div {
    background-color: #F6F3FB !important;
    background: #F6F3FB !important;
}

[data-testid="stChatInput"] {
    background-color: #F6F3FB !important;
    background: #F6F3FB !important;
    border: 1px solid #DED6EC !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] > div {
    background-color: #F6F3FB !important;
    background: #F6F3FB !important;
    border: 1px solid #DED6EC !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] form {
    background-color: #F6F3FB !important;
    background: #F6F3FB !important;
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] textarea {
    background-color: #F6F3FB !important;
    color: #30303A !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #777780 !important;
}


/* ----------------------------------------------------------
   BUTTONS
   ---------------------------------------------------------- */

.stButton > button {
    background-color: #F6F3FB !important;
    color: #30303A !important;
    border: 1px solid #DED6EC !important;
    border-radius: 10px !important;
}

.stButton > button:hover {
    background-color: #F6F3FB !important;
    color: #5533A8 !important;
    border-color: #5533A8 !important;
}


/* ----------------------------------------------------------
   DATAFRAME
   ---------------------------------------------------------- */

[data-testid="stDataFrame"] {
    border: 1px solid #DED6EC !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}


/* ----------------------------------------------------------
   INFO / ALERT BOXES
   ---------------------------------------------------------- */

[data-testid="stAlert"] {
    background-color: #F6F3FB !important;
    border: 1px solid #DED6EC !important;
}


/* ----------------------------------------------------------
   DIVIDERS
   ---------------------------------------------------------- */

hr {
    border-color: #DED6EC !important;
}


/* ----------------------------------------------------------
   REMOVE EXTRA TOP SPACE
   ---------------------------------------------------------- */

[data-testid="stDecoration"] {
    background-color: #F6F3FB !important;
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

    st.markdown(
        "## 🎓 College Assistant"
    )

    st.caption(
        "Your AI College Guide"
    )

    st.divider()

    st.markdown(
        "### 💬 Main Chatbot"
    )

    st.write(
        "Ask questions about:"
    )

    st.write("• TNEA")
    st.write("• Colleges")
    st.write("• Cutoffs")
    st.write("• Engineering branches")
    st.write("• Counselling")

    st.divider()

    st.markdown(
        "### Examples"
    )

    st.write(
        "• What is TNEA?"
    )

    st.write(
        "• CSE vs AI & DS?"
    )

    st.write(
        "• Which branch is best?"
    )

    st.write(
        "• What colleges can I get?"
    )


# ============================================================
# MAIN TITLE
# ============================================================

st.markdown(
    "# 🎓 College Assistant Chatbot"
)

st.markdown(
    "Ask anything about TNEA, colleges, cutoffs, "
    "branches, counselling and your recommendations."
)


# ============================================================
# WELCOME MESSAGE
# ============================================================

if len(st.session_state.messages) == 0:

    st.info(
        """
        👋 **Hi! I'm your College Assistant.**

        Ask me anything about TNEA, colleges, cutoffs,
        engineering branches and counselling.

        You can also give your requirements, for example:

        **My cutoff is 180. I am OC. I want CSE in Chennai.**

        I will search the available college cutoff data
        and show the matching colleges.
        """
    )


# ============================================================
# HELPER FUNCTION
# ============================================================

def clean_recommendations(data):

    """
    Converts recommendation output into a clean list of
    dictionaries.

    Supports:
        - list of dictionaries
        - pandas DataFrame
        - dictionary
    """

    if data is None:
        return []

    # --------------------------------------------------------
    # DataFrame
    # --------------------------------------------------------

    if isinstance(data, pd.DataFrame):

        if data.empty:
            return []

        return data.to_dict(
            orient="records"
        )

    # --------------------------------------------------------
    # List
    # --------------------------------------------------------

    if isinstance(data, list):

        cleaned = []

        for item in data:

            if isinstance(item, dict):

                cleaned.append(item)

        return cleaned

    # --------------------------------------------------------
    # Dictionary
    # --------------------------------------------------------

    if isinstance(data, dict):

        # If dictionary contains recommendations
        if "recommendations" in data:

            return clean_recommendations(
                data["recommendations"]
            )

        return [data]

    return []


# ============================================================
# DISPLAY COLLEGE RECOMMENDATIONS
# ============================================================

def display_colleges(recommendations):

    recommendations = clean_recommendations(
        recommendations
    )

    if not recommendations:
        return

    # --------------------------------------------------------
    # Remove internal fields from display
    # --------------------------------------------------------

    cleaned_rows = []

    for index, item in enumerate(
        recommendations,
        start=1
    ):

        row = dict(item)

        # Remove internal profile information
        row.pop("_profile", None)

        # Remove unnecessary internal fields
        row.pop("profile", None)

        cleaned_rows.append(row)

    if not cleaned_rows:
        return

    # --------------------------------------------------------
    # Convert to DataFrame
    # --------------------------------------------------------

    df = pd.DataFrame(
        cleaned_rows
    )

    # --------------------------------------------------------
    # Remove completely empty columns
    # --------------------------------------------------------

    df = df.dropna(
        axis=1,
        how="all"
    )

    # --------------------------------------------------------
    # Remove completely empty rows
    # --------------------------------------------------------

    df = df.dropna(
        axis=0,
        how="all"
    )

    # --------------------------------------------------------
    # Reset index
    # --------------------------------------------------------

    df = df.reset_index(
        drop=True
    )

    # --------------------------------------------------------
    # Create rank if it doesn't exist
    # --------------------------------------------------------

    if "Rank" not in df.columns:

        if "rank" not in df.columns:

            df.insert(
                0,
                "Rank",
                range(
                    1,
                    len(df) + 1
                )
            )

    # --------------------------------------------------------
    # Rename common column names
    # --------------------------------------------------------

    rename_map = {}

    if "rank" in df.columns:
        rename_map["rank"] = "Rank"

    if "college_name" in df.columns:
        rename_map[
            "college_name"
        ] = "College Name"

    if "college" in df.columns:
        rename_map[
            "college"
        ] = "College Name"

    if "district" in df.columns:
        rename_map[
            "district"
        ] = "District"

    if "branch" in df.columns:
        rename_map[
            "branch"
        ] = "Branch"

    if "cutoff" in df.columns:
        rename_map[
            "cutoff"
        ] = "Previous Cutoff"

    if "chance" in df.columns:
        rename_map[
            "chance"
        ] = "Chance"

    df = df.rename(
        columns=rename_map
    )

    # --------------------------------------------------------
    # Remove duplicate Rank column
    # --------------------------------------------------------

    if (
        "Rank" in df.columns
        and
        df.columns.tolist().count("Rank") > 1
    ):

        df = df.loc[
            :,
            ~df.columns.duplicated()
        ]

    # --------------------------------------------------------
    # Keep only useful columns
    #
    # This prevents duplicate rank/category columns.
    # --------------------------------------------------------

    preferred_columns = [
        "Rank",
        "College Name",
        "District",
        "Branch",
        "Previous Cutoff",
        "Chance"
    ]

    available_columns = [
        column
        for column in preferred_columns
        if column in df.columns
    ]

    if available_columns:

        df = df[
            available_columns
        ]

    # --------------------------------------------------------
    # FINAL REMOVE EMPTY ROWS
    # --------------------------------------------------------

    df = df.dropna(
        how="all"
    )

    # Remove rows where every displayed value is blank
    df = df[
        ~df.astype(str)
        .apply(
            lambda row:
            row.str.strip().eq("").all(),
            axis=1
        )
    ]

    df = df.reset_index(
        drop=True
    )

    # --------------------------------------------------------
    # If no colleges
    # --------------------------------------------------------

    if df.empty:

        st.warning(
            "No matching colleges were found."
        )

        return

    # --------------------------------------------------------
    # SINGLE RECOMMENDATION BOX
    # --------------------------------------------------------

    st.subheader(
        "🏫 Matching Colleges"
    )

    st.caption(
        f"Showing all {len(df)} matching college(s) "
        "from the available cutoff data."
    )

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # Dynamic height prevents blank rows.
    # --------------------------------------------------------

    row_height = 35

    header_height = 38

    calculated_height = (
        header_height
        +
        (len(df) * row_height)
        +
        10
    )

    calculated_height = max(
        80,
        min(
            calculated_height,
            700
        )
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=calculated_height
    )


# ============================================================
# PROCESS CHATBOT RESPONSE
# ============================================================

def process_question(question):

    if answer_question is None:

        return (
            "The chatbot engine could not be imported. "
            "Please check `chatbot_engine.py`.",
            []
        )

    try:

        # ----------------------------------------------------
        # First try the newer two-argument format
        # ----------------------------------------------------

        result = answer_question(
            question,
            st.session_state.messages
        )

    except TypeError:

        try:

            # ------------------------------------------------
            # Fallback for your original one-argument function
            # ------------------------------------------------

            result = answer_question(
                question
            )

        except Exception as error:

            print(
                "CHATBOT ERROR:",
                repr(error)
            )

            return (
                "Sorry, I couldn't process that question. "
                "Please check the terminal for the error.",
                []
            )

    except Exception as error:

        print(
            "CHATBOT ERROR:",
            repr(error)
        )

        return (
            "Sorry, I couldn't process that question. "
            "Please check the terminal for the error.",
            []
        )

    # ========================================================
    # HANDLE DIFFERENT RETURN FORMATS
    # ========================================================

    reply = ""
    recommendations = []

    # --------------------------------------------------------
    # Tuple
    # --------------------------------------------------------

    if isinstance(result, tuple):

        if len(result) >= 1:
            reply = result[0]

        if len(result) >= 2:
            recommendations = result[1]

    # --------------------------------------------------------
    # Dictionary
    # --------------------------------------------------------

    elif isinstance(result, dict):

        reply = result.get(
            "answer",
            result.get(
                "response",
                result.get(
                    "message",
                    ""
                )
            )
        )

        recommendations = result.get(
            "recommendations",
            result.get(
                "colleges",
                []
            )
        )

    # --------------------------------------------------------
    # String
    # --------------------------------------------------------

    elif isinstance(result, str):

        reply = result

    # --------------------------------------------------------
    # Anything else
    # --------------------------------------------------------

    else:

        reply = str(result)

    recommendations = clean_recommendations(
        recommendations
    )

    return (
        reply,
        recommendations
    )


# ============================================================
# DISPLAY PREVIOUS CHAT
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

        if content:

            st.markdown(
                content
            )

        if recommendations:

            display_colleges(
                recommendations
            )


# ============================================================
# RECOMMENDED QUESTIONS
# ============================================================

st.markdown(
    "##### Recommended Questions"
)

columns = st.columns(4)

questions = [
    "What is TNEA?",
    "CSE vs AI & DS?",
    "Which branch is best?",
    "What colleges can I get?"
]

for index, question in enumerate(
    questions
):

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
# QUICK QUESTION HANDLING
# ============================================================

if st.session_state.quick_question:

    user_input = (
        st.session_state.quick_question
    )

    st.session_state.quick_question = None


# ============================================================
# SEND MESSAGE
# ============================================================

if user_input:

    user_input = user_input.strip()

    if user_input:

        # ----------------------------------------------------
        # Save user message
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        # ----------------------------------------------------
        # Get AI response
        # ----------------------------------------------------

        with st.spinner(
            "Thinking..."
        ):

            reply, recommendations = process_question(
                user_input
            )

        # ----------------------------------------------------
        # Save assistant response
        # ----------------------------------------------------

        assistant_message = {
            "role": "assistant",
            "content": reply
        }

        if recommendations:

            assistant_message[
                "recommendations"
            ] = recommendations

        st.session_state.messages.append(
            assistant_message
        )

        # ----------------------------------------------------
        # Refresh
        # ----------------------------------------------------

        st.rerun()