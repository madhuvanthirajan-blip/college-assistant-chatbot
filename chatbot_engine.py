import os
import re
import json
from typing import Optional, Tuple, List, Dict

import pandas as pd

from data_loader import load_college_data


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
    "ST",
]


# ============================================================
# COLLEGE TYPE / OWNERSHIP FILTERS
# ============================================================

COLLEGE_TYPE_ALIASES = {
    "AUTONOMOUS": [
        "autonomous",
        "autonomous college",
        "autonomous colleges",
        "autonomous institution",
        "autonomous institutions",
    ],
    "GOVERNMENT": [
        "government",
        "government college",
        "government colleges",
        "govt",
        "govt college",
        "govt colleges",
        "govt.",
        "government engineering college",
        "government engineering colleges",
        "government college of engineering",
        "university college of engineering",
        "university departments of anna university",
    ],
    "GOVERNMENT_AIDED": [
        "government aided",
        "government-aided",
        "govt aided",
        "govt-aided",
    ],
}



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
        "computer science & engineering",
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
        "artificial intelligence data science",
        "aids",
    ],

    "AI_ML": [
        "ai ml",
        "ai&ml",
        "ai and ml",
        "ai machine learning",
        "artificial intelligence and machine learning",
        "artificial intelligence & machine learning",
        "artificial intelligence machine learning",
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
        "mechanical",
        "mechanical engineering",
    ],

    "CIVIL": [
        "civil",
        "civil engineering",
    ],

    "AERONAUTICAL": [
        "aeronautical",
        "aeronautical engineering",
    ],

    "AEROSPACE": [
        "aerospace",
        "aerospace engineering",
    ],

    "BIOTECHNOLOGY": [
        "biotechnology",
        "bio technology",
        "biotech",
    ],

    "CHEMICAL": [
        "chemical",
        "chemical engineering",
    ],

    "AGRICULTURAL": [
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
    ],

    "BC": [
        "bc",
        "backward class",
        "backward classes",
        "bc category",
    ],

    "BCM": [
        "bcm",
        "bc muslim",
        "backward class muslim",
        "backward classes muslim",
    ],

    "MBC": [
        "mbc",
        "most backward class",
        "most backward classes",
        "mbc category",
    ],

    "SC": [
        "sc",
        "scheduled caste",
        "sc category",
    ],

    "SCA": [
        "sca",
        "scheduled caste arunthathiyar",
        "arunthathiyar",
    ],

    "ST": [
        "st",
        "scheduled tribe",
        "st category",
    ],
}


# ============================================================
# LOCATION ALIASES
# ============================================================

LOCATION_ALIASES = {

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
        "kanchipuram district",
    ],

    "Erode": [
        "erode",
    ],

    "Thanjavur": [
        "thanjavur",
        "tanjore",
    ],

    "Tiruvallur": [
        "tiruvallur",
        "thiruvallur",
    ],

    "Chengalpattu": [
        "chengalpattu",
    ],

    "Namakkal": [
        "namakkal",
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

    "Karur": [
        "karur",
    ],

    "Cuddalore": [
        "cuddalore",
    ],

    "Villupuram": [
        "villupuram",
        "viluppuram",
    ],

    "Tiruppur": [
        "tiruppur",
    ],

    "Dharmapuri": [
        "dharmapuri",
    ],

    "Krishnagiri": [
        "krishnagiri",
    ],

    "Ramanathapuram": [
        "ramanathapuram",
        "ramnad",
    ],

    "Sivaganga": [
        "sivaganga",
    ],

    "Pudukkottai": [
        "pudukkottai",
    ],

    "Nagapattinam": [
        "nagapattinam",
    ],

    "Mayiladuthurai": [
        "mayiladuthurai",
    ],

    "Tenkasi": [
        "tenkasi",
    ],

    "Kallakurichi": [
        "kallakurichi",
    ],
}


# ============================================================
# TEXT HELPERS
# ============================================================

def clean_text(value) -> str:

    if pd.isna(value):
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(value)
    ).strip()


def normalize_text(value) -> str:

    text = clean_text(value).lower()

    text = text.replace("&", " and ")

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

    phrase = normalize_text(phrase)

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
# BRANCH NORMALIZATION
# ============================================================

def normalize_branch(
    value: str
) -> Optional[str]:

    text = normalize_text(value)

    if not text:
        return None

    for canonical, aliases in BRANCH_ALIASES.items():

        for alias in aliases:

            if text == normalize_text(alias):

                return canonical

    return None


# ============================================================
# BRANCH MATCHING
# ============================================================

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

    # --------------------------------------------------------
    # CSE
    # --------------------------------------------------------

    if requested == "CSE":

        allowed = [

            "computer science and engineering",

            "computer science and engineering ss",

            "computer science engineering",

            "computer science engineering ss",
        ]

        return actual in allowed

    # --------------------------------------------------------
    # IT
    # --------------------------------------------------------

    if requested == "IT":

        return actual in [

            "information technology",

            "information tech",
        ]

    # --------------------------------------------------------
    # AI & DS
    # --------------------------------------------------------

    if requested == "AI_DS":

        return actual in [

            "artificial intelligence and data science",

            "artificial intelligence and data science ss",

            "ai and data science",

            "ai and data science ss",
        ]

    # --------------------------------------------------------
    # AI & ML
    # --------------------------------------------------------

    if requested == "AI_ML":

        return actual in [

            "artificial intelligence and machine learning",

            "artificial intelligence and machine learning ss",

            "ai and machine learning",

            "ai and machine learning ss",
        ]

    # --------------------------------------------------------
    # ECE
    # --------------------------------------------------------

    if requested == "ECE":

        return actual in [

            "electronics and communication engineering",

            "electronics and communication engineering ss",
        ]

    # --------------------------------------------------------
    # EEE
    # --------------------------------------------------------

    if requested == "EEE":

        return actual in [

            "electrical and electronics engineering",

            "electrical and electronics engineering ss",
        ]

    # --------------------------------------------------------
    # Other branches
    # --------------------------------------------------------

    exact_mapping = {

        "MECHANICAL": [
            "mechanical engineering",
            "mechanical engineering ss",
        ],

        "CIVIL": [
            "civil engineering",
            "civil engineering ss",
        ],

        "AERONAUTICAL": [
            "aeronautical engineering",
        ],

        "AEROSPACE": [
            "aerospace engineering",
        ],

        "BIOTECHNOLOGY": [
            "biotechnology",
        ],

        "CHEMICAL": [
            "chemical engineering",
        ],

        "AGRICULTURAL": [
            "agricultural engineering",
        ],
    }

    if requested in exact_mapping:

        return actual in exact_mapping[
            requested
        ]

    return False


# ============================================================
# LOCAL CUTOFF EXTRACTION
# ============================================================

def extract_cutoff_locally(
    text: str
) -> Optional[float]:

    lower = text.lower()

    patterns = [

        r"(?:cut[\s-]?off|cutoff)"
        r"\s*(?:is|was|=|:)?\s*"
        r"(\d{2,3}(?:\.\d+)?)",

        r"(?:score|scored|mark|marks)"
        r"\s*(?:is|was|of|=|:)?\s*"
        r"(\d{2,3}(?:\.\d+)?)",

        r"\b(\d{2,3}(?:\.\d+)?)\s*"
        r"(?:cut[\s-]?off|cutoff|marks?|score)\b",
    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            lower
        )

        for match in matches:

            try:

                value = float(match)

                if 0 <= value <= 200:

                    return value

            except ValueError:

                pass

    # --------------------------------------------------------
    # Fallback number detection
    # --------------------------------------------------------

    numbers = re.findall(
        r"\b\d{2,3}(?:\.\d+)?\b",
        lower
    )

    for number in numbers:

        try:

            value = float(number)

            if 50 <= value <= 200:

                return value

        except ValueError:

            pass

    return None


# ============================================================
# LOCAL CATEGORY EXTRACTION
# ============================================================

def extract_category_locally(
    text: str
) -> Optional[str]:

    lower = normalize_text(
        text
    )

    ordered = sorted(

        CATEGORY_ALIASES.items(),

        key=lambda item: max(
            len(
                normalize_text(alias)
            )
            for alias in item[1]
        ),

        reverse=True
    )

    for category, aliases in ordered:

        for alias in aliases:

            if phrase_matches(
                lower,
                alias
            ):

                return category

    return None


# ============================================================
# LOCAL BRANCH EXTRACTION
# ============================================================

def extract_branch_locally(
    text: str
) -> Optional[str]:

    lower = normalize_text(
        text
    )

    ordered = sorted(

        BRANCH_ALIASES.items(),

        key=lambda item: max(
            len(
                normalize_text(alias)
            )
            for alias in item[1]
        ),

        reverse=True
    )

    for canonical, aliases in ordered:

        for alias in aliases:

            if phrase_matches(
                lower,
                alias
            ):

                return canonical

    return None


# ============================================================
# LOCAL LOCATION EXTRACTION FROM USER PROMPT
# ============================================================

def extract_location_locally(
    text: str
) -> Optional[str]:

    lower = normalize_text(
        text
    )

    ordered = sorted(

        LOCATION_ALIASES.items(),

        key=lambda item: max(
            len(
                normalize_text(alias)
            )
            for alias in item[1]
        ),

        reverse=True
    )

    for location, aliases in ordered:

        for alias in aliases:

            if phrase_matches(
                lower,
                alias
            ):

                return location

    return None


# ============================================================
# LOCAL COLLEGE TYPE EXTRACTION
# ============================================================

def extract_college_type_locally(
    text: str
) -> Optional[str]:

    normalized = normalize_text(text)

    # Government-aided is checked first so it is never
    # accidentally treated as a plain government college.
    is_aided = any(
        phrase_matches(normalized, alias)
        for alias in COLLEGE_TYPE_ALIASES["GOVERNMENT_AIDED"]
    )

    is_autonomous = any(
        phrase_matches(normalized, alias)
        for alias in COLLEGE_TYPE_ALIASES["AUTONOMOUS"]
    )

    is_government = any(
        phrase_matches(normalized, alias)
        for alias in COLLEGE_TYPE_ALIASES["GOVERNMENT"]
    )

    if is_aided:
        return "GOVERNMENT_AIDED"

    if is_autonomous and is_government:
        return "AUTONOMOUS_GOVERNMENT"

    if is_autonomous:
        return "AUTONOMOUS"

    if is_government:
        return "GOVERNMENT"

    return None


# ============================================================
# LOCAL DETAILS
# ============================================================

def extract_details_locally(
    text: str
) -> Dict:

    details = {}

    cutoff = extract_cutoff_locally(
        text
    )

    if cutoff is not None:

        details["cutoff"] = cutoff

    category = extract_category_locally(
        text
    )

    if category:

        details["category"] = category

    branch = extract_branch_locally(
        text
    )

    if branch:

        details["branch"] = branch

    location = extract_location_locally(
        text
    )

    if location:

        details["location"] = location

    college_type = extract_college_type_locally(
        text
    )

    if college_type:

        details["college_type"] = college_type

    return details


# ============================================================
# AI NATURAL LANGUAGE UNDERSTANDING
# ============================================================

def extract_details_with_ai(
    text: str
) -> Optional[Dict]:

    api_key = (
        os.getenv("NVIDIA_API_KEY")
        or os.getenv("NIM_API_KEY")
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

        system_prompt = """

You are the natural-language understanding component
of a Tamil Nadu TNEA college recommendation chatbot.

Understand the student's request regardless of how it
is written.

The student may use:

- formal English
- informal English
- short phrases
- incomplete sentences
- conversational language
- different word orders
- spelling variations

Determine whether the student wants:

RECOMMEND_COLLEGES

or

GENERAL_QUESTION

RECOMMEND_COLLEGES means the student wants:

- college recommendations
- college options
- colleges they can get
- admission chances
- possible colleges
- suitable colleges
- colleges based on marks
- where they can study
- similar requests

Extract:

cutoff:
The student's TNEA cutoff/mark.
Number from 0 to 200.
Use null if missing.

category:
One of:
OC, BC, BCM, MBC, SC, SCA, ST

Use null if the student did not mention a community/category.
Do NOT default missing category to OC.

college_type:
One of:
AUTONOMOUS, GOVERNMENT, GOVERNMENT_AIDED
Use null if the student did not mention a college type.
If the student says autonomous, return AUTONOMOUS.
If the student says government college/govt college, return GOVERNMENT.
If the student says government-aided, return GOVERNMENT_AIDED.

location:
A Tamil Nadu city/district if mentioned.

Examples:
Chennai
Coimbatore
Madurai
Salem
Cuddalore
Trichy
Tiruvallur
etc.

Use null if missing.

branch:
Use exactly one of:

CSE
IT
AI_DS
AI_ML
ECE
EEE
MECHANICAL
CIVIL
AERONAUTICAL
AEROSPACE
BIOTECHNOLOGY
CHEMICAL
AGRICULTURAL

Examples:

computer science -> CSE
computer science engineering -> CSE
CS -> CSE
CSE -> CSE

AI and data science -> AI_DS
AI & DS -> AI_DS
AIDS -> AI_DS

AI and machine learning -> AI_ML
AI & ML -> AI_ML
AIML -> AI_ML

electronics and communication -> ECE
ECE -> ECE

information technology -> IT
IT -> IT

Do not invent missing information.

Example:

"I got 180 and want computer science colleges in Chennai"

means:

{
    "intent": "RECOMMEND_COLLEGES",
    "cutoff": 180,
    "category": null,
    "location": "Chennai",
    "branch": "CSE"
}

Example:

"I'm BC, scored 175 and want AI data science near Coimbatore"

means:

{
    "intent": "RECOMMEND_COLLEGES",
    "cutoff": 175,
    "category": "BC",
    "location": "Coimbatore",
    "branch": "AI_DS"
}

Example:

"180 BC CSE"

means:

{
    "intent": "RECOMMEND_COLLEGES",
    "cutoff": 180,
    "category": "BC",
    "location": null,
    "branch": "CSE"
}

Example:

"Tell me about TNEA counselling"

means:

{
    "intent": "GENERAL_QUESTION",
    "cutoff": null,
    "category": null,
    "location": null,
    "branch": null
}

Return ONLY valid JSON.

"""

        response = client.chat.completions.create(

            model=os.getenv(
                "NVIDIA_MODEL",
                "meta/llama-3.1-8b-instruct"
            ),

            messages=[

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": text
                }

            ],

            temperature=0,

            max_tokens=300
        )

        raw = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        # ----------------------------------------------------
        # Remove markdown code fences if the model returns them
        # ----------------------------------------------------

        raw = re.sub(

            r"^```(?:json)?\s*",

            "",

            raw,

            flags=re.IGNORECASE
        )

        raw = re.sub(

            r"\s*```$",

            "",

            raw
        ).strip()

        data = json.loads(
            raw
        )

        if not isinstance(
            data,
            dict
        ):

            return None

        return data

    except Exception as error:

        print(
            "AI EXTRACTION ERROR:",
            repr(error)
        )

        return None


# ============================================================
# COMBINE AI + LOCAL EXTRACTION
# ============================================================

def extract_details(
    text: str
) -> Dict:

    local = extract_details_locally(
        text
    )

    ai = extract_details_with_ai(
        text
    )

    details = {}

    # --------------------------------------------------------
    # AI results
    # --------------------------------------------------------

    if ai:

        intent = ai.get(
            "intent"
        )

        if intent:

            details["intent"] = (

                str(intent)
                .upper()
                .strip()
            )

        cutoff = ai.get(
            "cutoff"
        )

        if cutoff is not None:

            try:

                cutoff = float(
                    cutoff
                )

                if 0 <= cutoff <= 200:

                    details["cutoff"] = cutoff

            except (
                ValueError,
                TypeError
            ):

                pass

        category = ai.get(
            "category"
        )

        if category:

            category = (

                str(category)
                .upper()
                .strip()
            )

            if category in CATEGORIES:

                details["category"] = category

        college_type = ai.get(
            "college_type"
        )

        if college_type:

            college_type = (
                str(college_type)
                .upper()
                .strip()
            )

            if college_type in {
                "AUTONOMOUS",
                "GOVERNMENT",
                "GOVERNMENT_AIDED",
                "AUTONOMOUS_GOVERNMENT"
            }:

                details["college_type"] = college_type

        branch = ai.get(
            "branch"
        )

        if branch:

            branch_key = (

                str(branch)
                .strip()
                .lower()
            )

            branch_map = {

                "cse": "CSE",
                "cs": "CSE",

                "it": "IT",

                "ai_ds": "AI_DS",
                "ai ds": "AI_DS",
                "ai and ds": "AI_DS",
                "aids": "AI_DS",

                "ai_ml": "AI_ML",
                "ai ml": "AI_ML",
                "ai and ml": "AI_ML",
                "aiml": "AI_ML",

                "ece": "ECE",

                "eee": "EEE",

                "mechanical": "MECHANICAL",

                "civil": "CIVIL",

                "aeronautical": "AERONAUTICAL",

                "aerospace": "AEROSPACE",

                "biotechnology": "BIOTECHNOLOGY",

                "chemical": "CHEMICAL",

                "agricultural": "AGRICULTURAL",
            }

            if branch_key in branch_map:

                details["branch"] = (
                    branch_map[
                        branch_key
                    ]
                )

            else:

                normalized_branch = (
                    normalize_branch(
                        branch
                    )
                )

                if normalized_branch:

                    details["branch"] = (
                        normalized_branch
                    )

        location = ai.get(
            "location"
        )

        if location:

            details["location"] = (
                str(location).strip()
            )

    # --------------------------------------------------------
    # USER TEXT IS AUTHORITATIVE
    # --------------------------------------------------------
    # The deterministic local parser reads the exact words typed
    # by the user. Therefore it must override AI output whenever
    # it found a value. This prevents the LLM from replacing
    # Chennai with another district or changing CSE/category.
    # --------------------------------------------------------

    for key, value in local.items():

        details[key] = value

    # --------------------------------------------------------
    # USER TEXT IS AUTHORITATIVE FOR COMMUNITY + COLLEGE TYPE
    # --------------------------------------------------------
    # The AI extractor must never invent a community/category
    # that the student did not mention. The same applies to
    # autonomous/government status.
    # --------------------------------------------------------

    if "category" not in local:
        details.pop("category", None)

    if "college_type" not in local:
        details.pop("college_type", None)

    return details


# ============================================================
# RECOMMENDATION INTENT
# ============================================================

def recommendation_requested(
    text: str,
    details: Dict
) -> bool:

    if (
        details.get("intent")
        == "RECOMMEND_COLLEGES"
    ):

        return True

    lower = normalize_text(
        text
    )

    recommendation_phrases = [

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
        "autonomous colleges",
        "government colleges",
        "government-aided colleges",
        "autonomous college options",
        "government college options",
    ]

    if any(

        phrase in lower

        for phrase in recommendation_phrases

    ):

        return True

    # If cutoff and branch are both present,
    # assume recommendation intent.

    if (

        details.get("cutoff") is not None

        and

        details.get("branch")

    ):

        return True

    return False


# ============================================================
# FIND EXCEL COLUMN
# ============================================================

def find_column(
    df: pd.DataFrame,
    names: List[str]
) -> Optional[str]:

    normalized_columns = {

        normalize_text(column): column

        for column in df.columns

    }

    for name in names:

        normalized_name = normalize_text(
            name
        )

        if normalized_name in normalized_columns:

            return normalized_columns[
                normalized_name
            ]

    return None


# ============================================================
# EXTRACT LOCATION FROM COLLEGE NAME
# ============================================================

def extract_location_from_college_name(
    college_name: str
) -> str:

    text = clean_text(
        college_name
    )

    if not text:

        return "Not specified"

    normalized = normalize_text(
        text
    )

    # --------------------------------------------------------
    # 1. DISTRICT HAS HIGHEST PRIORITY
    #
    # Example:
    #
    # Panruti Cuddalore District 607106
    #
    # should return Cuddalore.
    # --------------------------------------------------------

    district_matches = []

    for location, aliases in LOCATION_ALIASES.items():

        for alias in aliases:

            alias_normalized = normalize_text(
                alias
            )

            pattern = (

                r"(?<![a-z0-9])"

                + re.escape(
                    alias_normalized
                )

                + r"\s+district\b"

            )

            for match in re.finditer(
                pattern,
                normalized,
                flags=re.IGNORECASE
            ):

                district_matches.append(
                    (
                        match.start(),
                        location
                    )
                )

    if district_matches:

        district_matches.sort(
            key=lambda item: item[0]
        )

        return district_matches[-1][1]

    # --------------------------------------------------------
    # 2. Remove highway / road / salai expressions
    #
    # This prevents:
    #
    # Chennai-Kumbakonam Highway
    #
    # from automatically making the college Chennai.
    # --------------------------------------------------------

    address_for_location = re.sub(

        r"\b[a-z0-9\s-]+"
        r"(?:highway|road|salai)\b",

        " ",

        normalized,

        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # 3. Find all remaining location mentions.
    #
    # Prefer the LAST occurrence because college addresses
    # often end with the actual city/district.
    # --------------------------------------------------------

    location_matches = []

    for location, aliases in LOCATION_ALIASES.items():

        for alias in aliases:

            alias_normalized = normalize_text(
                alias
            )

            pattern = (

                r"(?<![a-z0-9])"

                + re.escape(
                    alias_normalized
                )

                + r"(?![a-z0-9])"

            )

            for match in re.finditer(

                pattern,

                address_for_location,

                flags=re.IGNORECASE

            ):

                location_matches.append(

                    (
                        match.start(),
                        location
                    )

                )

    if location_matches:

        location_matches.sort(
            key=lambda item: item[0]
        )

        return location_matches[-1][1]

    return "Not specified"


# ============================================================
# DATASET DISTRICT NORMALIZATION
# ============================================================

def normalize_location_value(value: str) -> str:

    text = normalize_text(value)

    if not text:
        return ""

    # Remove common suffixes used in Excel district columns.
    text = re.sub(r"\b(district|dist|dt)\b", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    for location, aliases in LOCATION_ALIASES.items():

        if text == normalize_text(location):
            return normalize_text(location)

        for alias in aliases:
            if text == normalize_text(alias):
                return normalize_text(location)

    return text


# ============================================================
# LOCATION MATCHING
# ============================================================

def college_location_matches(
    college_name: str,
    requested_location: str
) -> bool:

    if not requested_location:

        return True

    actual_location = (

        extract_location_from_college_name(

            college_name

        )

    )

    return (

        normalize_text(
            actual_location
        )

        ==

        normalize_text(
            requested_location
        )

    )


# ============================================================
# COLLEGE TYPE DETECTION
# ============================================================

def detect_college_type_from_row(
    row: pd.Series,
    college_col: str
) -> str:
    """Detect institution type from the complete dataset row.

    The dataset may not have a dedicated type column, so the
    college name/address is the main source. If a dedicated
    type/status/management column exists, its value is also
    considered.
    """

    values = []

    for column in row.index:
        try:
            value = row[column]
        except Exception:
            continue

        if pd.isna(value):
            continue

        values.append(str(value))

    text = normalize_text(" ".join(values))

    is_aided = any(
        phrase_matches(text, alias)
        for alias in COLLEGE_TYPE_ALIASES["GOVERNMENT_AIDED"]
    )

    is_autonomous = any(
        phrase_matches(text, alias)
        for alias in COLLEGE_TYPE_ALIASES["AUTONOMOUS"]
    )

    is_government = any(
        phrase_matches(text, alias)
        for alias in COLLEGE_TYPE_ALIASES["GOVERNMENT"]
    )

    if is_aided:
        if is_autonomous:
            return "AUTONOMOUS GOVERNMENT_AIDED"
        return "GOVERNMENT_AIDED"

    if is_government and is_autonomous:
        return "AUTONOMOUS GOVERNMENT"

    if is_autonomous:
        return "AUTONOMOUS"

    if is_government:
        return "GOVERNMENT"

    return "OTHER"


# ============================================================
# GET RECOMMENDATIONS
# ============================================================

def get_recommendations(
    cutoff: float,
    category: Optional[str],
    location: Optional[str],
    branch: str,
    college_type: Optional[str] = None
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

    # --------------------------------------------------------
    # Find actual Excel columns
    # --------------------------------------------------------

    college_col = find_column(

        df,

        [
            "College Name",
            "college_name",
            "College",
            "Institution Name",
            "Institution",
            "institution_name"
        ]

    )

    branch_col = find_column(

        df,

        [
            "Branch",
            "branch",
            "Branch Name",
            "Course",
            "Course Name",
            "Programme",
            "Program",
            "Department"
        ]

    )

    district_col = find_column(

        df,

        [
            "District",
            "district",
            "District Name",
            "district name",
            "College District",
            "college district",
            "Location",
            "location"
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

        print(
            "Available columns:",
            df.columns.tolist()
        )

        return []

    # --------------------------------------------------------
    # Category
    # --------------------------------------------------------
    # IMPORTANT:
    # The user may omit community/category. In that case we use
    # OC internally only because the cutoff dataset requires a
    # specific cutoff column, but the chatbot must NEVER tell
    # the user that OC was selected or mention a community they
    # did not provide.
    # --------------------------------------------------------

    category_was_provided = bool(category)

    category = (
        str(category).upper().strip()
        if category
        else "OC"
    )

    if category not in CATEGORIES:
        category = "OC"
        category_was_provided = False

    category_col = find_column(
        df,
        [category]
    )

    if not category_col:
        print(
            f"Category column {category} not found."
        )
        return []

    # --------------------------------------------------------
    # COLLEGE TYPE FILTER
    # --------------------------------------------------------
    # This filter is applied BEFORE cutoff ranking.
    #
    # AUTONOMOUS -> only rows containing autonomous evidence.
    # GOVERNMENT -> only government colleges; government-aided
    #                rows are excluded.
    # GOVERNMENT_AIDED -> only government-aided colleges.
    # --------------------------------------------------------

    requested_type = (
        str(college_type).upper().strip()
        if college_type
        else None
    )

    if requested_type not in {
        None,
        "AUTONOMOUS",
        "GOVERNMENT",
        "GOVERNMENT_AIDED",
        "AUTONOMOUS_GOVERNMENT"
    }:
        requested_type = None

    def college_type_matches(
        college_name: str,
        row: pd.Series,
        requested: Optional[str]
    ) -> bool:

        if not requested:
            return True

        detected = detect_college_type_from_row(
            row,
            college_col
        )

        if requested == "AUTONOMOUS":
            return "AUTONOMOUS" in detected

        if requested == "GOVERNMENT":
            return (
                "GOVERNMENT" in detected
                and "GOVERNMENT_AIDED" not in detected
            )

        if requested == "GOVERNMENT_AIDED":
            return "GOVERNMENT_AIDED" in detected

        if requested == "AUTONOMOUS_GOVERNMENT":
            return (
                "AUTONOMOUS" in detected
                and "GOVERNMENT" in detected
                and "GOVERNMENT_AIDED" not in detected
            )

        return True

    if requested_type:

        type_mask = df.apply(
            lambda row: college_type_matches(
                clean_text(row[college_col]),
                row,
                requested_type
            ),
            axis=1
        )

        df = df[type_mask].copy()

        if df.empty:
            return []

    # --------------------------------------------------------
    # BRANCH FILTER
    # --------------------------------------------------------

    branch_mask = (

        df[branch_col]

        .fillna("")

        .map(

            lambda value:

            branch_matches(

                value,

                branch

            )

        )

    )

    filtered = df[
        branch_mask
    ].copy()

    # --------------------------------------------------------
    # LOCATION FILTER -- STRICT
    # --------------------------------------------------------
    # If the Excel file contains a District/Location column, use
    # it as the primary source. Only if that column does not exist
    # do we fall back to parsing the college name/address.
    # NEVER fall back to all districts when a requested district
    # has zero matches.
    # --------------------------------------------------------

    requested_location = normalize_location_value(location) if location else ""

    if requested_location and not filtered.empty:

        if district_col:

            district_values = (
                filtered[district_col]
                .fillna("")
                .map(normalize_location_value)
            )

            location_mask = district_values.eq(
                requested_location
            )

            filtered = filtered[
                location_mask
            ].copy()

        else:

            location_mask = (
                filtered[college_col]
                .fillna("")
                .map(
                    lambda value: college_location_matches(
                        value,
                        location
                    )
                )
            )

            filtered = filtered[
                location_mask
            ].copy()

    if filtered.empty:

        return []

    # --------------------------------------------------------
    # CONVERT CUTOFF COLUMN TO NUMERIC
    # --------------------------------------------------------

    filtered["__cutoff"] = pd.to_numeric(

        filtered[category_col]

        .astype(str)

        .str.replace(
            "*",
            "",
            regex=False
        )

        .str.strip(),

        errors="coerce"

    )

    filtered = filtered.dropna(

        subset=[
            "__cutoff"
        ]

    )

    if filtered.empty:

        return []

    # --------------------------------------------------------
    # CUTOFF DIFFERENCE
    # --------------------------------------------------------

    filtered["__difference"] = (

        float(cutoff)

        -

        filtered["__cutoff"]

    )

    # --------------------------------------------------------
    # CHANCE
    # --------------------------------------------------------

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

    filtered["__chance"] = (

        filtered[
            "__difference"
        ]

        .map(
            calculate_chance
        )

    )

    # --------------------------------------------------------
    # CHANCE ORDER
    # --------------------------------------------------------

    chance_order = {

        "Very High": 0,

        "High": 1,

        "Moderate": 2,

        "Low": 3,
    }

    filtered["__chance_order"] = (

        filtered[
            "__chance"
        ]

        .map(
            chance_order
        )

    )

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    filtered = filtered.sort_values(

        [

            "__chance_order",

            "__cutoff",

            college_col

        ],

        ascending=[

            True,

            False,

            True

        ]

    )

    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    filtered = filtered.drop_duplicates(

        subset=[

            college_col,

            branch_col

        ],

        keep="first"

    )

    # --------------------------------------------------------
    # CREATE RESULT LIST
    # --------------------------------------------------------

    results = []

    for rank, (_, row) in enumerate(

        filtered.iterrows(),

        start=1

    ):

        college_name = clean_text(

            row[
                college_col
            ]

        )

        results.append({

            "rank":
                rank,

            "college_name":
                college_name,

            "location":
                (
                    normalize_location_value(
                        row[district_col]
                    )
                    if district_col
                    and clean_text(row[district_col])
                    else extract_location_from_college_name(
                        college_name
                    )
                ),
            "district":
                (
                    normalize_location_value(
                        row[district_col]
                    )
                    if district_col
                    and clean_text(row[district_col])
                    else extract_location_from_college_name(
                        college_name
                    )
                ),

            "college_type":
                detect_college_type_from_row(
                    row,
                    college_col
                ),

            "branch":
                clean_text(
                    row[
                        branch_col
                    ]
                ),

            "cutoff":
                float(
                    row[
                        "__cutoff"
                    ]
                ),

            "chance":
                row[
                    "__chance"
                ],

            "cutoff_difference":
                round(

                    float(
                        row[
                            "__difference"
                        ]
                    ),

                    2

                )

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

    "branch":

        (
            "Popular engineering branches include CSE, "
            "IT, AI & DS, AI & ML, ECE, EEE, Mechanical, "
            "Civil and other engineering branches."
        ),
}


# ============================================================
# GENERAL KNOWLEDGE RESPONSE
# ============================================================

def knowledge_reply(
    text: str
) -> str:

    lower = normalize_text(
        text
    )

    if (

        "cse" in lower

        and

        (
            "ai" in lower
            or
            "data science" in lower
        )

    ):

        return (

            "CSE and AI & DS are both strong choices. "
            "CSE provides a broader computer-science "
            "foundation, while AI & DS focuses more on "
            "artificial intelligence, machine learning "
            "and data science."

        )

    if (

        "best branch" in lower

        or

        "which branch" in lower

    ):

        return (

            "There is no single best engineering branch "
            "for everyone. CSE, IT and AI & DS are popular "
            "for software and AI careers, while ECE, EEE, "
            "Mechanical, Civil and other branches suit "
            "different interests and career goals."

        )

    for key, answer in KNOWLEDGE.items():

        if key in lower:

            return answer

    return (

        "I can help you with TNEA, colleges, cutoffs, "
        "engineering branches, counselling and college "
        "recommendations."

    )


# ============================================================
# NVIDIA RESPONSE
# ============================================================

def try_nvidia_response(
    text: str,
    history: List[Dict],
    recommendations: List[Dict]
) -> Optional[str]:

    api_key = (

        os.getenv("NVIDIA_API_KEY")

        or

        os.getenv("NIM_API_KEY")

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

                "\n\nCOLLEGE DATA FROM THE PROJECT "
                "EXCEL FILE:\n"

            )

            for row in recommendations[:100]:

                context += (

                    f"{row['rank']}. "

                    f"{row['college_name']} | "

                    f"{row['location']} | "

                    f"{row['branch']} | "

                    f"Type: {row.get('college_type', '')} | "

                    f"Cutoff: {row['cutoff']} | "

                    f"Chance: {row['chance']}\n"

                )

        system_prompt = (

            "You are College Assistant, an AI assistant "
            "for students in Tamil Nadu. "

            "Answer clearly and in a student-friendly way. "

            "When college records are supplied, use ONLY "
            "those records. "

            "Never invent college names, cutoff values, "
            "branches, locations or admission chances. "

            "Previous-year cutoff data is historical and "
            "does not guarantee admission. "
            "Never mention OC, BC, BCM, MBC, SC, SCA or ST "
            "unless the student explicitly mentioned that "
            "community/category. Never invent a community. "
            "If the student asked for autonomous colleges, "
            "discuss only the supplied autonomous results. "
            "If the student asked for government colleges, "
            "discuss only the supplied government results. "
            "Do not claim a college is autonomous or government "
            "unless the supplied record supports it."

            + context

        )

        messages = [

            {

                "role":
                    "system",

                "content":
                    system_prompt

            }

        ]

        for message in history[-8:]:

            role = message.get(
                "role"
            )

            content = message.get(
                "content",
                ""
            )

            if (

                role in {
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
                        content

                })

        messages.append({

            "role":
                "user",

            "content":
                text

        })

        response = client.chat.completions.create(

            model=model,

            messages=messages,

            temperature=0.2,

            max_tokens=700

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
# CONVERSATION DETAIL MERGING
# ============================================================

def latest_previous_user_details(history) -> Dict:

    if not history:
        return {}

    for item in reversed(history):

        if item.get("role") != "user":
            continue

        content = clean_text(
            item.get("content", "")
        )

        if content:
            return extract_details_locally(content)

    return {}


def merge_with_history(
    current: Dict,
    history
) -> Dict:

    previous = latest_previous_user_details(
        history
    )

    merged = dict(previous)

    # Current message always wins.
    merged.update(current)

    return merged


# ============================================================
# MAIN CHATBOT FUNCTION
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

    # --------------------------------------------------------
    # UNDERSTAND NATURAL LANGUAGE
    # --------------------------------------------------------

    current_details = extract_details(
        text
    )

    # Support follow-up questions such as:
    # "What about Chennai?" after the user previously supplied
    # cutoff + branch. The newly mentioned district replaces the
    # previous district, while unspecified fields are retained.
    details = merge_with_history(
        current_details,
        history
    )

    print(
        "CURRENT DETAILS:",
        current_details
    )

    print(
        "FINAL DETAILS:",
        details
    )

    # --------------------------------------------------------
    # DETERMINE INTENT
    # --------------------------------------------------------

    is_recommendation = (

        recommendation_requested(

            text,

            details

        )

    )

    # ========================================================
    # COLLEGE RECOMMENDATION
    # ========================================================

    if is_recommendation:

        cutoff = details.get(
            "cutoff"
        )

        branch = details.get(
            "branch"
        )

        # IMPORTANT: keep category as None when the user did not
        # mention a community. Do not expose an OC default.
        category = details.get(
            "category"
        )

        location = details.get(
            "location"
        )

        college_type = details.get(
            "college_type"
        )

        # ----------------------------------------------------
        # Missing cutoff
        # ----------------------------------------------------

        if cutoff is None:

            return (

                "Sure, I can find suitable colleges "
                "for you. Please tell me your TNEA "
                "cutoff or marks."

            ), []

        # ----------------------------------------------------
        # Missing branch
        # ----------------------------------------------------

        if branch is None:

            return (

                f"I understood that your cutoff is "
                f"{cutoff}. Which engineering branch "
                f"are you interested in? For example, "
                f"CSE, IT, AI & DS, ECE or EEE."

            ), []

        # ----------------------------------------------------
        # SEARCH EXCEL
        # ----------------------------------------------------

        recommendations = get_recommendations(

            cutoff=float(
                cutoff
            ),

            category=category,

            location=location,

            branch=branch,

            college_type=college_type

        )

        # ----------------------------------------------------
        # RESULTS FOUND
        # ----------------------------------------------------

        if recommendations:

            location_text = ""

            if location:

                location_text = (

                    f" in {location}"

                )

            type_text = ""

            if college_type == "AUTONOMOUS":
                type_text = " autonomous"
            elif college_type == "GOVERNMENT":
                type_text = " government"
            elif college_type == "GOVERNMENT_AIDED":
                type_text = " government-aided"
            elif college_type == "AUTONOMOUS_GOVERNMENT":
                type_text = " autonomous government"

            category_text = ""

            if category:
                category_text = f" under the {category} category"

            reply = (
                f"I found {len(recommendations)} matching"
                f"{type_text} college options for {branch} "
                f"with a cutoff of {cutoff}{category_text}"
                f"{location_text}. "
                f"The results are based on the TNEA cutoff data "
                f"in your Excel file. Previous-year cutoffs are "
                f"references only and do not guarantee admission."
            )

        # ----------------------------------------------------
        # NO RESULTS
        # ----------------------------------------------------

        else:

            category_text = ""

            if category:
                category_text = f" under the {category} category"

            type_text = ""

            if college_type == "AUTONOMOUS":
                type_text = " autonomous"
            elif college_type == "GOVERNMENT":
                type_text = " government"
            elif college_type == "GOVERNMENT_AIDED":
                type_text = " government-aided"
            elif college_type == "AUTONOMOUS_GOVERNMENT":
                type_text = " autonomous government"

            reply = (
                f"I couldn't find matching{type_text} colleges "
                f"for {branch} with a cutoff of {cutoff}"
                f"{category_text}"
            )

            if location:
                reply += f" in {location}."
            else:
                reply += "."

            reply += (
                " You can try another branch, location or cutoff."
            )

        # ----------------------------------------------------
        # NVIDIA CAN IMPROVE RESPONSE WORDING
        #
        # BUT IT MUST USE ONLY THE EXCEL RESULTS.
        # ----------------------------------------------------

        ai_reply = try_nvidia_response(

            text,

            history,

            recommendations

        )

        if ai_reply:

            reply = ai_reply

        return (

            reply,

            recommendations

        )

    # ========================================================
    # GENERAL QUESTION
    # ========================================================

    ai_reply = try_nvidia_response(

        text,

        history,

        []

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