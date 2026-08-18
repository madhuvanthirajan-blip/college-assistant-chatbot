import os
import re
from typing import Optional, Tuple, List, Dict

import pandas as pd

from data_loader import load_college_data


# ============================================================
# CATEGORIES
# ============================================================

CATEGORIES = [
    "OC",
    "BC",
    "BCM",
    "MBC",
    "SC",
    "SCA",
    "ST",
]


# ============================================================
# BRANCH ALIASES
# ============================================================

BRANCH_ALIASES = {

    "CSE": [
        "cse",
        "cs",
        "computer science",
        "computer science engineering",
        "computer science and engineering",
    ],

    "IT": [
        "it",
        "information technology",
        "information tech",
    ],

    "AI_DS": [
        "ai ds",
        "ai&ds",
        "ai and ds",
        "ai data science",
        "ai and data science",
        "artificial intelligence and data science",
        "artificial intelligence & data science",
        "aids",
    ],

    "AI_ML": [
        "ai ml",
        "ai&ml",
        "ai and ml",
        "ai machine learning",
        "ai and machine learning",
        "artificial intelligence and machine learning",
        "artificial intelligence & machine learning",
        "aiml",
    ],

    "ECE": [
        "ece",
        "electronics",
        "electronics communication",
        "electronics and communication",
        "electronics and communication engineering",
    ],

    "EEE": [
        "eee",
        "electrical",
        "electrical electronics",
        "electrical and electronics",
        "electrical and electronics engineering",
    ],

    "MECHANICAL": [
        "mech",
        "mechanical",
        "mechanical engineering",
    ],

    "CIVIL": [
        "civil",
        "civil engineering",
    ],

    "AERONAUTICAL": [
        "aero",
        "aeronautical",
        "aeronautical engineering",
    ],

    "AEROSPACE": [
        "aerospace",
        "aerospace engineering",
    ],

    "BIOTECHNOLOGY": [
        "biotech",
        "bio tech",
        "biotechnology",
        "biotechnology engineering",
    ],

    "CHEMICAL": [
        "chemical",
        "chemical engineering",
    ],

    "AGRICULTURAL": [
        "agri",
        "agriculture",
        "agricultural",
        "agricultural engineering",
    ],
}


# ============================================================
# CATEGORY ALIASES
# ============================================================

CATEGORY_ALIASES = {

    "OC": [
        "oc",
        "open",
        "open category",
        "general",
        "general category",
        "open competition",
    ],

    "BC": [
        "bc",
        "bc category",
        "backward class",
        "backward classes",
    ],

    "BCM": [
        "bcm",
        "bcm category",
        "bc muslim",
        "backward class muslim",
        "backward classes muslim",
    ],

    "MBC": [
        "mbc",
        "mbc category",
        "most backward class",
        "most backward classes",
    ],

    "SC": [
        "sc",
        "sc category",
        "scheduled caste",
    ],

    "SCA": [
        "sca",
        "sca category",
        "scheduled caste arunthathiyar",
        "arunthathiyar",
    ],

    "ST": [
        "st",
        "st category",
        "scheduled tribe",
    ],
}


# ============================================================
# DISTRICT ALIASES
# ============================================================

DISTRICT_ALIASES = {

    "Chennai": [
        "chennai",
        "madras",
    ],

    "Coimbatore": [
        "coimbatore",
        "kovai",
    ],

    "Madurai": [
        "madurai",
    ],

    "Tiruchirappalli": [
        "tiruchirappalli",
        "tiruchirapalli",
        "trichy",
        "tiruchi",
    ],

    "Salem": [
        "salem",
    ],

    "Erode": [
        "erode",
    ],

    "Tirunelveli": [
        "tirunelveli",
        "nellai",
    ],

    "Vellore": [
        "vellore",
    ],

    "Kanchipuram": [
        "kanchipuram",
        "kancheepuram",
    ],

    "Tiruvallur": [
        "tiruvallur",
        "thiruvallur",
        "tiruvallur district",
        "thiruvallur district",
    ],

    "Chengalpattu": [
        "chengalpattu",
        "chengalpet",
    ],

    "Thanjavur": [
        "thanjavur",
        "tanjore",
    ],

    "Dindigul": [
        "dindigul",
    ],

    "Thoothukudi": [
        "thoothukudi",
        "tuticorin",
    ],

    "Virudhunagar": [
        "virudhunagar",
    ],

    "Namakkal": [
        "namakkal",
    ],

    "Karur": [
        "karur",
    ],

    "Cuddalore": [
        "cuddalore",
    ],

    "Dharmapuri": [
        "dharmapuri",
    ],

    "Krishnagiri": [
        "krishnagiri",
    ],

    "Pudukkottai": [
        "pudukkottai",
    ],

    "Ramanathapuram": [
        "ramanathapuram",
        "ramnad",
    ],

    "Sivaganga": [
        "sivaganga",
    ],

    "Tenkasi": [
        "tenkasi",
    ],

    "The Nilgiris": [
        "nilgiris",
        "ooty",
    ],

    "Tiruppur": [
        "tiruppur",
    ],

    "Ariyalur": [
        "ariyalur",
    ],

    "Perambalur": [
        "perambalur",
    ],

    "Nagapattinam": [
        "nagapattinam",
    ],

    "Mayiladuthurai": [
        "mayiladuthurai",
    ],

    "Villupuram": [
        "villupuram",
        "viluppuram",
    ],

    "Kallakurichi": [
        "kallakurichi",
    ],
}


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(value) -> str:

    if value is None:
        return ""

    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass

    return re.sub(
        r"\s+",
        " ",
        str(value)
    ).strip()


def normalize_text(value) -> str:

    text = clean_text(value).lower()

    text = text.replace("&", " and ")

    text = text.replace("+", " plus ")

    text = re.sub(
        r"[^a-z0-9]+",
        " ",
        text
    )

    return re.sub(
        r"\s+",
        " ",
        text
    ).strip()


def phrase_matches(
    text: str,
    phrase: str
) -> bool:

    text = normalize_text(text)

    phrase = normalize_text(
        phrase
    )

    if not text or not phrase:
        return False

    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(phrase)
        + r"(?![a-z0-9])"
    )

    return re.search(
        pattern,
        text
    ) is not None


# ============================================================
# CATEGORY
# ============================================================

def normalize_category(
    value: str
) -> Optional[str]:

    text = normalize_text(
        value
    )

    for category, aliases in CATEGORY_ALIASES.items():

        if text == normalize_text(
            category
        ):
            return category

        for alias in aliases:

            if text == normalize_text(
                alias
            ):
                return category

    return None


def extract_category(
    text: str
) -> Optional[str]:

    normalized = normalize_text(
        text
    )

    candidates = []

    for category, aliases in CATEGORY_ALIASES.items():

        for alias in aliases:

            if phrase_matches(
                normalized,
                alias
            ):

                candidates.append(
                    (
                        len(
                            normalize_text(
                                alias
                            )
                        ),
                        category
                    )
                )

    if candidates:

        return max(
            candidates
        )[1]

    return None


# ============================================================
# BRANCH
# ============================================================

def normalize_branch(
    value: str
) -> Optional[str]:

    text = normalize_text(
        value
    )

    if not text:
        return None

    for canonical, aliases in BRANCH_ALIASES.items():

        if text == normalize_text(
            canonical
        ):
            return canonical

        for alias in aliases:

            if text == normalize_text(
                alias
            ):
                return canonical

    return None


def extract_branch(
    text: str
) -> Optional[str]:

    normalized = normalize_text(
        text
    )

    candidates = []

    for canonical, aliases in BRANCH_ALIASES.items():

        for alias in aliases:

            if phrase_matches(
                normalized,
                alias
            ):

                candidates.append(
                    (
                        len(
                            normalize_text(
                                alias
                            )
                        ),
                        canonical
                    )
                )

    if candidates:

        return max(
            candidates
        )[1]

    return None


def branch_matches(
    actual_branch: str,
    requested_branch: str
) -> bool:

    actual = normalize_text(
        actual_branch
    )

    requested = normalize_branch(
        requested_branch
    )

    if not requested:
        return False

    if requested == "CSE":

        return (
            "computer science and engineering"
            in actual
        )

    if requested == "IT":

        return (
            "information technology"
            in actual
        )

    if requested == "AI_DS":

        return (
            "artificial intelligence and data science"
            in actual
            or
            "ai and data science"
            in actual
        )

    if requested == "AI_ML":

        return (
            "artificial intelligence and machine learning"
            in actual
            or
            "ai and machine learning"
            in actual
        )

    if requested == "ECE":

        return (
            "electronics and communication"
            in actual
        )

    if requested == "EEE":

        return (
            "electrical and electronics"
            in actual
        )

    mapping = {

        "MECHANICAL":
            "mechanical engineering",

        "CIVIL":
            "civil engineering",

        "AERONAUTICAL":
            "aeronautical engineering",

        "AEROSPACE":
            "aerospace engineering",

        "BIOTECHNOLOGY":
            "biotechnology",

        "CHEMICAL":
            "chemical engineering",

        "AGRICULTURAL":
            "agricultural engineering",
    }

    expected = mapping.get(
        requested
    )

    if expected:

        return expected in actual

    return False


# ============================================================
# DISTRICT EXTRACTION
# ============================================================

def extract_location(
    text: str
) -> Optional[str]:

    normalized = normalize_text(
        text
    )

    candidates = []

    for district, aliases in DISTRICT_ALIASES.items():

        for alias in aliases:

            if phrase_matches(
                normalized,
                alias
            ):

                candidates.append(
                    (
                        len(
                            normalize_text(
                                alias
                            )
                        ),
                        district
                    )
                )

    if candidates:

        return max(
            candidates
        )[1]

    return None


# ============================================================
# DISTRICT NORMALIZATION
# ============================================================

def normalize_district(
    value: str
) -> Optional[str]:

    if not value:
        return None

    text = normalize_text(
        value
    )

    for district, aliases in DISTRICT_ALIASES.items():

        if text == normalize_text(
            district
        ):
            return district

        for alias in aliases:

            if text == normalize_text(
                alias
            ):
                return district

    return clean_text(
        value
    )


# ============================================================
# STRICT DISTRICT MATCH
# ============================================================

def district_matches(
    actual_district: str,
    requested_district: str
) -> bool:

    if not actual_district:
        return False

    requested = normalize_district(
        requested_district
    )

    actual = normalize_district(
        actual_district
    )

    if not requested or not actual:
        return False

    return (
        normalize_text(actual)
        ==
        normalize_text(requested)
    )


# ============================================================
# CUTOFF EXTRACTION
# ============================================================

def extract_cutoff(
    text: str
) -> Optional[float]:

    patterns = [

        r"(?:cut[\s-]?off|cutoff)"
        r"\s*(?:is|was|of|=|:|-)?\s*"
        r"(\d{2,3}(?:\.\d+)?)",

        r"(?:score|scored|mark|marks)"
        r"\s*(?:is|was|of|=|:|-)?\s*"
        r"(\d{2,3}(?:\.\d+)?)",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.I
        )

        if match:

            try:

                value = float(
                    match.group(1)
                )

                if 50 <= value <= 200:

                    return value

            except Exception:
                pass

    numbers = re.findall(
        r"\b\d{2,3}(?:\.\d+)?\b",
        text
    )

    for raw in numbers:

        try:

            value = float(
                raw
            )

            if 50 <= value <= 200:

                return value

        except Exception:
            pass

    return None


# ============================================================
# CURRENT MESSAGE DETAILS
# ============================================================

def extract_current_details(
    text: str
) -> Dict:

    details = {}

    cutoff = extract_cutoff(
        text
    )

    if cutoff is not None:

        details["cutoff"] = cutoff

    category = extract_category(
        text
    )

    if category:

        details["category"] = category

    branch = extract_branch(
        text
    )

    if branch:

        details["branch"] = branch

    location = extract_location(
        text
    )

    if location:

        details["location"] = location

    return details


# ============================================================
# FOLLOW-UP
# ============================================================

def is_followup(
    text: str
) -> bool:

    normalized = normalize_text(
        text
    )

    followup_phrases = [

        "what about",

        "how about",

        "same cutoff",

        "same mark",

        "same marks",

        "same score",

        "same branch",

        "same location",

        "same college",

        "and in",

        "then in",

        "for the same",

        "with the same",
    ]

    for phrase in followup_phrases:

        if phrase in normalized:

            return True

    words = normalized.split()

    if len(words) <= 4:

        if (
            extract_category(text)
            or
            extract_branch(text)
            or
            extract_location(text)
        ):

            return True

    return False


# ============================================================
# DETAILS + HISTORY
# ============================================================

def extract_details(
    text: str,
    history=None
) -> Dict:

    current = extract_current_details(
        text
    )

    # --------------------------------------------------------
    # New question.
    # --------------------------------------------------------

    if not is_followup(text):

        return current

    previous = {}

    if history:

        for message in reversed(
            history
        ):

            if message.get(
                "role"
            ) != "user":

                continue

            previous_text = (
                message.get(
                    "content",
                    ""
                )
                or
                ""
            ).strip()

            if not previous_text:

                continue

            old_details = (
                extract_current_details(
                    previous_text
                )
            )

            for key, value in old_details.items():

                if key not in previous:

                    previous[key] = value

            if len(previous) >= 4:

                break

    details = dict(
        previous
    )

    # Current message ALWAYS wins.
    details.update(
        current
    )

    return details


# ============================================================
# FIND COLUMN
# ============================================================

def find_column(
    df: pd.DataFrame,
    names: List[str]
) -> Optional[str]:

    normalized_columns = {

        normalize_text(column):
            column

        for column in df.columns
    }

    for name in names:

        key = normalize_text(
            name
        )

        if key in normalized_columns:

            return normalized_columns[
                key
            ]

    return None


# ============================================================
# COLLEGE LOCATION FALLBACK
# ============================================================

def extract_location_from_college_name(
    college_name: str
) -> str:

    text = normalize_text(
        college_name
    )

    candidates = []

    for district, aliases in DISTRICT_ALIASES.items():

        for alias in aliases:

            if phrase_matches(
                text,
                alias
            ):

                candidates.append(
                    (
                        len(
                            normalize_text(
                                alias
                            )
                        ),
                        district
                    )
                )

    if candidates:

        return max(
            candidates
        )[1]

    return "Not specified"


# ============================================================
# RECOMMENDATION INTENT
# ============================================================

def recommendation_requested(
    text: str,
    details: Dict
) -> bool:

    normalized = normalize_text(
        text
    )

    informational = [

        "what is",

        "what are",

        "explain",

        "define",

        "tell me about",

        "how does",

        "how do",

        "why is",

        "why are",
    ]

    if any(
        normalized.startswith(
            phrase
        )
        for phrase in informational
    ):

        return False

    recommendation_phrases = [

        "college",

        "colleges",

        "college option",

        "college options",

        "which college",

        "which colleges",

        "what college",

        "what colleges",

        "recommend",

        "recommendation",

        "recommendations",

        "suggest colleges",

        "college suggestions",

        "possible colleges",

        "eligible colleges",

        "admission chance",

        "admission chances",

        "where can i get",

        "where can i study",

        "can i get",

        "what can i get",

        "my chances",

        "show colleges",

        "list colleges",

        "find colleges",

        "i need college",

        "i need colleges",

        "want college",

        "want colleges",
    ]

    if any(
        phrase in normalized
        for phrase in recommendation_phrases
    ):

        return True

    if (
        details.get("cutoff") is not None
        and
        (
            details.get("category")
            or
            details.get("branch")
            or
            details.get("location")
        )
    ):

        return True

    return False


# ============================================================
# GET RECOMMENDATIONS
# ============================================================

def get_recommendations(
    cutoff: float,
    category: Optional[str],
    location: Optional[str] = None,
    branch: Optional[str] = None
) -> List[Dict]:

    try:

        df = load_college_data()

    except Exception as error:

        print(
            "DATA LOADING ERROR:",
            repr(error)
        )

        return []

    if (
        df is None
        or
        df.empty
    ):

        return []

    # ========================================================
    # COLUMN DETECTION
    # ========================================================

    college_col = find_column(

        df,

        [
            "College Name",
            "college name",
            "college",
            "institution",
            "institution name",
        ]
    )

    branch_col = find_column(

        df,

        [
            "Branch",
            "branch name",
            "course",
            "program",
            "programme",
        ]
    )

    # --------------------------------------------------------
    # THIS IS THE IMPORTANT FIX
    #
    # Look for the REAL DISTRICT COLUMN.
    # --------------------------------------------------------

    district_col = find_column(

        df,

        [
            "District",
            "district",
            "College District",
            "college district",
        ]
    )

    if not college_col:

        print(
            "College Name column not found."
        )

        print(
            "Available columns:",
            df.columns.tolist()
        )

        return []

    if not branch_col:

        print(
            "Branch column not found."
        )

        return []

    # ========================================================
    # CATEGORY
    # ========================================================

    category_was_provided = bool(
        category
    )

    normalized_category = (
        normalize_category(
            category
        )
        if category
        else None
    )

    # Internal fallback only.
    internal_category = (
        normalized_category
        or
        "OC"
    )

    category_col = find_column(

        df,

        [
            internal_category
        ]
    )

    if not category_col:

        print(
            f"Category column "
            f"{internal_category} not found."
        )

        return []

    # ========================================================
    # COPY DATA
    # ========================================================

    work = df.copy()

    work["__college"] = (

        work[college_col]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    work["__branch"] = (

        work[branch_col]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # ========================================================
    # STRICT DISTRICT FILTER
    # ========================================================
    #
    # BEFORE:
    #
    # if location_mask.any():
    #     work = work[location_mask]
    #
    # That was WRONG because if the mask failed, the complete
    # dataset could remain.
    #
    # NOW:
    #
    # If a district is requested, every row MUST belong to
    # that district.
    # ========================================================

    if location:

        requested_district = normalize_district(
            location
        )

        print(
            "REQUESTED DISTRICT:",
            requested_district
        )

        if district_col:

            # ----------------------------------------------
            # Use actual District column.
            # ----------------------------------------------

            work["__district"] = (

                work[district_col]
                .fillna("")
                .astype(str)
                .str.strip()
            )

            district_mask = (

                work["__district"]
                .map(

                    lambda value:
                    district_matches(
                        value,
                        requested_district
                    )
                )
            )

            # STRICT FILTER.
            work = work[
                district_mask
            ].copy()

        else:

            # ----------------------------------------------
            # Dataset has no District column.
            #
            # Use college name as fallback.
            # ----------------------------------------------

            district_mask = (

                work["__college"]
                .map(

                    lambda value:
                    any(

                        phrase_matches(
                            value,
                            alias
                        )

                        for alias in
                        DISTRICT_ALIASES.get(
                            requested_district,
                            [
                                requested_district
                            ]
                        )
                    )
                )
            )

            # STRICT FILTER.
            work = work[
                district_mask
            ].copy()

    # ========================================================
    # BRANCH FILTER
    # ========================================================

    if branch:

        requested_branch = normalize_branch(
            branch
        )

        if requested_branch:

            branch_mask = (

                work["__branch"]
                .map(

                    lambda value:
                    branch_matches(
                        value,
                        requested_branch
                    )
                )
            )

            work = work[
                branch_mask
            ].copy()

    # ========================================================
    # NOTHING LEFT
    # ========================================================

    if work.empty:

        return []

    # ========================================================
    # CUTOFF
    # ========================================================

    work["__cutoff"] = pd.to_numeric(

        work[category_col]
        .astype(str)
        .str.replace(
            "*",
            "",
            regex=False
        )
        .str.strip(),

        errors="coerce"
    )

    work = work.dropna(
        subset=[
            "__cutoff"
        ]
    ).copy()

    if work.empty:

        return []

    # ========================================================
    # DIFFERENCE
    # ========================================================

    work["__difference"] = (

        float(cutoff)
        -
        work["__cutoff"]
    )

    # ========================================================
    # CHANCE
    # ========================================================

    def calculate_chance(
        difference
    ):

        if difference >= 5:

            return "Very High"

        elif difference >= 0:

            return "High"

        elif difference >= -10:

            return "Moderate"

        else:

            return "Low"

    work["__chance"] = (

        work["__difference"]
        .map(
            calculate_chance
        )
    )

    # ========================================================
    # CHANCE ORDER
    # ========================================================

    chance_order = {

        "Very High": 0,

        "High": 1,

        "Moderate": 2,

        "Low": 3,
    }

    work["__chance_order"] = (

        work["__chance"]
        .map(
            chance_order
        )
    )

    # ========================================================
    # SORT
    # ========================================================

    work = work.sort_values(

        [
            "__chance_order",
            "__cutoff",
            "__college",
        ],

        ascending=[
            True,
            False,
            True,
        ]
    )

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    work = work.drop_duplicates(

        subset=[
            "__college",
            "__branch",
        ],

        keep="first"
    )

    # ========================================================
    # RESULTS
    # ========================================================

    results = []

    for rank, (_, row) in enumerate(

        work.iterrows(),

        start=1
    ):

        college_name = clean_text(
            row["__college"]
        )

        actual_branch = clean_text(
            row["__branch"]
        )

        # ----------------------------------------------------
        # Location shown on card.
        #
        # Prefer the actual District column.
        # ----------------------------------------------------

        if district_col:

            result_location = clean_text(
                row["__district"]
            )

        else:

            result_location = (
                extract_location_from_college_name(
                    college_name
                )
            )

        results.append({

            "rank":
                rank,

            "college_name":
                college_name,

            "location":
                result_location,

            "branch":
                actual_branch,

            "cutoff":
                float(
                    row["__cutoff"]
                ),

            "chance":
                row["__chance"],

            "cutoff_difference":
                round(
                    float(
                        row[
                            "__difference"
                        ]
                    ),
                    2
                ),
        })

    return results


# ============================================================
# GENERAL KNOWLEDGE
# ============================================================

KNOWLEDGE = {

    "tnea":
        (
            "TNEA stands for Tamil Nadu Engineering "
            "Admissions. It is the admission process "
            "used for B.E./B.Tech admissions in Tamil Nadu."
        ),

    "counselling":
        (
            "TNEA counselling is the process through "
            "which students participate in college and "
            "branch allotment based on rank, category, "
            "choices and available seats."
        ),

    "cutoff":
        (
            "A TNEA cutoff is a historical admission "
            "mark for a particular college, branch and "
            "category. Previous-year cutoffs are only "
            "references and do not guarantee admission."
        ),
}


def knowledge_reply(
    text: str
) -> str:

    lower = text.lower()

    if "tnea" in lower:

        return KNOWLEDGE[
            "tnea"
        ]

    if "counselling" in lower:

        return KNOWLEDGE[
            "counselling"
        ]

    if (
        "cutoff" in lower
        or
        "cut off" in lower
    ):

        return KNOWLEDGE[
            "cutoff"
        ]

    if (
        (
            "cse" in lower
            or
            "computer science" in lower
        )
        and
        (
            "ai" in lower
            or
            "data science" in lower
        )
    ):

        return (

            "CSE provides a broader computer-science "
            "foundation, while AI & DS focuses more on "
            "data science, machine learning and AI. "
            "The better choice depends on your career "
            "interest and the college available."
        )

    return (

        "I can help with TNEA, colleges, cutoffs, "
        "engineering branches and counselling. "
        "Tell me your cutoff, community, preferred "
        "district and branch if you have one."
    )


# ============================================================
# NVIDIA RESPONSE
# ============================================================

def try_nvidia_response(
    text: str,
    history: List[Dict],
    recommendations: List[Dict],
    category_was_provided: bool = False
) -> Optional[str]:

    api_key = (

        os.getenv(
            "NVIDIA_API_KEY"
        )

        or

        os.getenv(
            "NIM_API_KEY"
        )
    )

    if not api_key:

        return None

    try:

        from openai import OpenAI

    except Exception:

        return None

    try:

        client = OpenAI(

            base_url=os.getenv(
                "NVIDIA_BASE_URL",
                "https://integrate.api.nvidia.com/v1"
            ),

            api_key=api_key
        )

        model = os.getenv(

            "NVIDIA_MODEL",

            "meta/llama-3.1-8b-instruct"
        )

        context = ""

        if recommendations:

            context = (

                "\n\nCOLLEGE DATA FROM "
                "PROJECT DATASET:\n"
            )

            for row in recommendations[:100]:

                context += (

                    f"{row['rank']}. "
                    f"{row['college_name']} | "
                    f"{row['location']} | "
                    f"{row['branch']} | "
                    f"Cutoff: {row['cutoff']} | "
                    f"Chance: {row['chance']}\n"
                )

        if category_was_provided:

            community_rule = (

                "The student explicitly provided a "
                "community. You may mention it when "
                "relevant."
            )

        else:

            community_rule = (

                "The student did not explicitly provide "
                "a community. Do not claim that the "
                "student selected OC."
            )

        system_prompt = (

            "You are College Assistant for TNEA "
            "students in Tamil Nadu. "

            "Answer clearly and briefly. "

            "When college records are supplied, use "
            "ONLY those records. "

            "Never invent college names, cutoff values, "
            "branches or locations. "

            "Previous-year cutoffs are historical "
            "references and do not guarantee admission. "

            + community_rule

            +

            "\nThe displayed recommendations are already "
            "filtered by the requested district and branch. "
            "Do not introduce colleges from another district."

            + context
        )

        messages = [

            {
                "role":
                    "system",

                "content":
                    system_prompt,
            }
        ]

        if is_followup(text):

            for message in history[-6:]:

                role = message.get(
                    "role"
                )

                content = (

                    message.get(
                        "content",
                        ""
                    )
                    or
                    ""
                )

                if (
                    role
                    in {
                        "user",
                        "assistant"
                    }
                    and
                    content
                ):

                    messages.append({

                        "role":
                            role,

                        "content":
                            content,
                    })

        messages.append({

            "role":
                "user",

            "content":
                text,
        })

        response = (

            client
            .chat
            .completions
            .create(

                model=model,

                messages=messages,

                temperature=0.2,

                max_tokens=700
            )
        )

        answer = (

            response
            .choices[0]
            .message
            .content
        )

        if answer:

            return answer.strip()

    except Exception as error:

        print(
            "NVIDIA RESPONSE ERROR:",
            repr(error)
        )

    return None


# ============================================================
# MAIN CHATBOT
# ============================================================

def answer_question(
    user_input: str,
    history=None
) -> Tuple[str, List[Dict]]:

    history = history or []

    text = (
        user_input
        or
        ""
    ).strip()

    if not text:

        return (
            "Please enter your question.",
            []
        )

    # ========================================================
    # EXTRACT DETAILS
    # ========================================================

    details = extract_details(
        text,
        history
    )

    print(
        "===================================="
    )

    print(
        "USER QUERY:",
        text
    )

    print(
        "EXTRACTED DETAILS:",
        details
    )

    print(
        "===================================="
    )

    # ========================================================
    # INTENT
    # ========================================================

    is_recommendation = (

        recommendation_requested(
            text,
            details
        )
    )

    # ========================================================
    # RECOMMENDATION
    # ========================================================

    if is_recommendation:

        cutoff = details.get(
            "cutoff"
        )

        category = details.get(
            "category"
        )

        branch = details.get(
            "branch"
        )

        location = details.get(
            "location"
        )

        category_was_provided = (
            category is not None
        )

        # ----------------------------------------------------
        # CUTOFF REQUIRED
        # ----------------------------------------------------

        if cutoff is None:

            return (

                "Sure! I can find suitable colleges "
                "for you. Please tell me your TNEA "
                "cutoff or marks."

            ), []

        # ----------------------------------------------------
        # GET RESULTS
        # ----------------------------------------------------

        recommendations = (

            get_recommendations(

                cutoff=float(
                    cutoff
                ),

                category=category,

                location=location,

                branch=branch
            )
        )

        # ====================================================
        # RESULTS
        # ====================================================

        if recommendations:

            location_text = ""

            if location:

                location_text = (
                    f" in {location}"
                )

            if branch:

                branch_text = (
                    f" for {branch}"
                )

            else:

                branch_text = (
                    " across available branches"
                )

            if category_was_provided:

                reply = (

                    f"I found "
                    f"{len(recommendations)} "
                    f"matching college options"
                    f"{branch_text} "
                    f"with a cutoff of "
                    f"{cutoff} under the "
                    f"{category} category"
                    f"{location_text}. "

                    "The results are based on "
                    "the TNEA cutoff data in "
                    "your project dataset. "
                    "Previous-year cutoffs are "
                    "references only and do not "
                    "guarantee admission."
                )

            else:

                reply = (

                    f"I found "
                    f"{len(recommendations)} "
                    f"matching college options"
                    f"{branch_text} "
                    f"with a cutoff of "
                    f"{cutoff}"
                    f"{location_text}. "

                    "The results are based on "
                    "the TNEA cutoff data in "
                    "your project dataset. "
                    "Previous-year cutoffs are "
                    "references only and do not "
                    "guarantee admission."
                )

            # ------------------------------------------------
            # AI wording is optional.
            # ------------------------------------------------

            ai_reply = try_nvidia_response(

                text,

                history,

                recommendations,

                category_was_provided
            )

            if ai_reply:

                reply = ai_reply

            return (

                reply,

                recommendations
            )

        # ====================================================
        # NO RESULTS
        # ====================================================

        branch_text = (

            branch
            if branch
            else
            "the requested branches"
        )

        location_text = (

            f" in {location}"
            if location
            else
            ""
        )

        if category_was_provided:

            return (

                f"I couldn't find matching colleges "
                f"for {branch_text} with a cutoff of "
                f"{cutoff} under the {category} "
                f"category{location_text}. "

                "I did not include colleges from "
                "other districts. Try another "
                "cutoff, branch or district."

            ), []

        return (

            f"I couldn't find matching colleges "
            f"for {branch_text} with a cutoff of "
            f"{cutoff}{location_text}. "

            "I did not include colleges from "
            "other districts. Try another "
            "cutoff, branch or district."

        ), []

    # ========================================================
    # GENERAL QUESTION
    # ========================================================

    ai_reply = try_nvidia_response(

        text,

        history if is_followup(text)
        else [],

        [],

        False
    )

    if ai_reply:

        return (
            ai_reply,
            []
        )

    return (

        knowledge_reply(
            text
        ),

        []
    )