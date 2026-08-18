import re
from collections import Counter, defaultdict
from typing import Optional, List, Dict, Tuple

import pandas as pd

from data_loader import load_college_data

try:
    from llm import ask_llm
except Exception:
    ask_llm = None


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
# DISTRICT ALIASES
# ============================================================

DISTRICTS = {

    "Ariyalur": [
        "ariyalur",
    ],

    "Chengalpattu": [
        "chengalpattu",
        "chenglepet",
        "chengalpet",
    ],

    "Chennai": [
        "chennai",
        "madras",
    ],

    "Coimbatore": [
        "coimbatore",
        "kovai",
    ],

    "Cuddalore": [
        "cuddalore",
    ],

    "Dharmapuri": [
        "dharmapuri",
    ],

    "Dindigul": [
        "dindigul",
    ],

    "Erode": [
        "erode",
    ],

    "Kallakurichi": [
        "kallakurichi",
        "chinnasalem",
    ],

    "Kanchipuram": [
        "kancheepuram",
        "kanchipuram",
    ],

    "Kanyakumari": [
        "kanyakumari",
        "kanyakumarai",
    ],

    "Karur": [
        "karur",
    ],

    "Krishnagiri": [
        "krishnagiri",
    ],

    "Madurai": [
        "madurai",
    ],

    "Mayiladuthurai": [
        "mayiladuthurai",
        "mayavaram",
    ],

    "Nagapattinam": [
        "nagapattinam",
        "nagappattinam",
    ],

    "Namakkal": [
        "namakkal",
    ],

    "The Nilgiris": [
        "the nilgiris",
        "nilgiris",
        "ooty",
    ],

    "Perambalur": [
        "perambalur",
        "elambalur",
    ],

    "Pudukkottai": [
        "pudukkottai",
    ],

    "Ramanathapuram": [
        "ramanathapuram",
        "ramnad",
    ],

    "Salem": [
        "salem",
    ],

    "Sivaganga": [
        "sivaganga",
        "sivagangai",
        "sivaganagi",
    ],

    "Tenkasi": [
        "tenkasi",
        "ayikudy",
    ],

    "Thanjavur": [
        "thanjavur",
        "tanjore",
    ],

    "Theni": [
        "theni",
    ],

    "Thoothukudi": [
        "thoothukudi",
        "tuticorin",
    ],

    "Tiruchirappalli": [
        "tiruchirappalli",
        "tiruchirapalli",
        "trichy",
        "tiruchi",
    ],

    "Tirunelveli": [
        "tirunelveli",
        "tirunelvei",
        "nellai",
    ],

    "Tirupattur": [
        "tirupattur",
        "tirupathur",
    ],

    "Tiruppur": [
        "tiruppur",
        "tirupur",
    ],

    "Tiruvallur": [
        "tiruvallur",
        "thiruvallur",
    ],

    "Tiruvannamalai": [
        "tiruvannamalai",
        "thiruvannamalai",
    ],

    "Tiruvarur": [
        "tiruvarur",
        "thiruvarur",
    ],

    "Vellore": [
        "vellore",
    ],

    "Villupuram": [
        "villupuram",
        "viluppuram",
    ],

    "Virudhunagar": [
        "virudhunagar",
    ],
}


# ============================================================
# CHENGALPATTU SPECIAL LOCALITIES
# ============================================================

CHENGALPATTU_HINTS = [

    "siruseri",
    "egattur",
    "kattankulathur",
    "chengalpattu",
    "chenglepet",
    "mamallapuram",
    "mahabalipuram",
    "poonjeri",
    "maraimalai nagar",
    "maraimalainagar",
    "vandalur",
    "madurantakam",
    "thiruporur",
    "kelambakkam",
    "kazhipattur",
    "singaperumal koil",
    "singaperumalkoil",

]


# ============================================================
# PINCODE FALLBACK
# ============================================================

PIN_PREFIX = {

    "603": "Chengalpattu",

    "621": "Tiruchirappalli",

    "622": "Pudukkottai",

    "623": "Ramanathapuram",

    "624": "Dindigul",

    "625": "Madurai",

    "626": "Virudhunagar",

    "627": "Tirunelveli",

    "628": "Thoothukudi",

    "629": "Kanyakumari",

    "630": "Sivaganga",

    "631": "Kanchipuram",

    "632": "Vellore",

    "635": "Krishnagiri",

    "636": "Salem",

    "637": "Namakkal",

    "638": "Erode",

    "639": "Karur",

    "641": "Coimbatore",

    "642": "Coimbatore",

    "643": "The Nilgiris",

}


# ============================================================
# BRANCHES
# ============================================================

BRANCHES = {

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
        "aids",
    ],

    "AI_ML": [
        "ai ml",
        "ai&ml",
        "ai and ml",
        "ai machine learning",
        "artificial intelligence and machine learning",
        "aiml",
    ],

    "ECE": [
        "ece",
        "electronics communication",
        "electronics and communication",
        "electronics and communication engineering",
    ],

    "EEE": [
        "eee",
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

CATEGORIES_ALIASES = {

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
# COLLEGE TYPE
# ============================================================

TYPE_ALIASES = {

    "AUTONOMOUS": [
        "autonomous",
        "autonomous college",
        "autonomous institution",
    ],

    "GOVERNMENT": [
        "government",
        "government college",
        "govt",
        "govt college",
        "government engineering college",
        "government college of engineering",
        "university college of engineering",
        "university departments of anna university",
        "anna university regional campus",
    ],

    "AIDED": [
        "government aided",
        "government-aided",
        "govt aided",
        "govt-aided",
    ],

}


# ============================================================
# BASIC TEXT FUNCTIONS
# ============================================================

def clean(value):

    if value is None or pd.isna(value):
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(value)
    ).strip()


def norm(value):

    text = clean(value)

    text = text.lower()

    text = text.replace(
        "&",
        " and "
    )

    text = re.sub(
        r"[^a-z0-9\s-]",
        " ",
        text
    )

    return re.sub(
        r"\s+",
        " ",
        text
    ).strip()


def has_phrase(
    text,
    phrase
):

    text = norm(text)

    phrase = norm(phrase)

    if not text or not phrase:
        return False

    return (
        re.search(
            r"(?<![a-z0-9])"
            + re.escape(phrase)
            + r"(?![a-z0-9])",
            text
        )
        is not None
    )


# ============================================================
# FIND DATASET COLUMN
# ============================================================

def find_col(
    df,
    names
):

    columns = {
        norm(column): column
        for column in df.columns
    }

    for name in names:

        key = norm(name)

        if key in columns:

            return columns[key]

    return None


# ============================================================
# EXTRACT CUTOFF
# ============================================================

def extract_cutoff(
    text
):

    text = text.lower()

    patterns = [

        r"(?:cut[\s-]?off|cutoff)"
        r"\s*(?:is|was|=|:)?\s*"
        r"(\d{2,3}(?:\.\d+)?)",

        r"(?:score|scored|mark|marks)"
        r"\s*(?:is|was|of|=|:)?\s*"
        r"(\d{2,3}(?:\.\d+)?)",

        r"\b(\d{2,3}(?:\.\d+)?)"
        r"\s*(?:cut[\s-]?off|cutoff|marks?|score)\b",
    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text
        )

        for value in matches:

            try:

                value = float(value)

                if 0 <= value <= 200:

                    return value

            except ValueError:

                pass

    # Fallback for:
    # "I got 189"
    for value in re.findall(
        r"\b\d{2,3}(?:\.\d+)?\b",
        text
    ):

        try:

            value = float(value)

            if 50 <= value <= 200:

                return value

        except ValueError:

            pass

    return None


# ============================================================
# GENERIC ALIAS EXTRACTION
# ============================================================

def extract_from_aliases(
    text,
    aliases
):

    text = norm(text)

    ordered = sorted(
        aliases.items(),
        key=lambda item:
            max(
                len(norm(x))
                for x in item[1]
            ),
        reverse=True
    )

    for key, values in ordered:

        for value in values:

            if has_phrase(
                text,
                value
            ):

                return key

    return None


def extract_category(
    text
):

    return extract_from_aliases(
        text,
        CATEGORIES_ALIASES
    )


def extract_branch(
    text
):

    return extract_from_aliases(
        text,
        BRANCHES
    )


def extract_location(
    text
):

    return extract_from_aliases(
        text,
        DISTRICTS
    )


# ============================================================
# EXTRACT COLLEGE TYPE
# ============================================================

def extract_type(
    text
):

    text = norm(text)

    aided = any(
        has_phrase(
            text,
            value
        )
        for value in TYPE_ALIASES["AIDED"]
    )

    autonomous = any(
        has_phrase(
            text,
            value
        )
        for value in TYPE_ALIASES["AUTONOMOUS"]
    )

    government = any(
        has_phrase(
            text,
            value
        )
        for value in TYPE_ALIASES["GOVERNMENT"]
    )

    if aided:

        return "GOVERNMENT_AIDED"

    if autonomous and government:

        return "AUTONOMOUS_GOVERNMENT"

    if autonomous:

        return "AUTONOMOUS"

    if government:

        return "GOVERNMENT"

    return None


# ============================================================
# EXPLICIT DISTRICT FROM ADDRESS
# ============================================================

def explicit_district(
    address
):

    text = norm(address)

    found = []

    for district, aliases in DISTRICTS.items():

        for alias in aliases:

            alias = norm(alias)

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(alias)
                + r"\s+"
                r"(?:district|dist|dt)\b"
            )

            for match in re.finditer(
                pattern,
                text
            ):

                found.append(
                    (
                        match.start(),
                        district
                    )
                )

    if not found:

        return None

    found.sort(
        key=lambda item:
        item[0]
    )

    return found[-1][1]


# ============================================================
# PINCODES
# ============================================================

def pins(
    address
):

    return re.findall(
        r"\b\d{6}\b",
        clean(address)
    )


# ============================================================
# BUILD EXACT PIN -> DISTRICT MAP
# ============================================================

def build_pin_map(
    df,
    college_col
):

    counts = defaultdict(
        Counter
    )

    for address in df[
        college_col
    ].fillna("").astype(str):

        district = explicit_district(
            address
        )

        if not district:

            continue

        for pin in pins(
            address
        ):

            counts[
                pin
            ][district] += 1

    result = {}

    for pin, counter in counts.items():

        # Only use an exact mapping when the
        # Excel itself gives one district for
        # that PIN.
        if len(counter) == 1:

            result[pin] = (
                counter
                .most_common(1)[0][0]
            )

    return result


# ============================================================
# FIND DISTRICT OF A COLLEGE
# ============================================================

def college_district(
    address,
    pin_map
):

    address = clean(
        address
    )

    if not address:

        return "Not specified"

    text = norm(
        address
    )

    # --------------------------------------------------------
    # CURRENT DISTRICT OVERRIDES
    # --------------------------------------------------------

    current_hints = {

        "Kallakurichi": [
            "kallakurichi",
            "chinnasalem",
        ],

        "Mayiladuthurai": [
            "mayiladuthurai",
            "mayavaram",
        ],

        "Tenkasi": [
            "tenkasi",
            "ayikudy",
        ],

        "Tirupattur": [
            "tirupattur",
            "tirupathur",
        ],

        "Perambalur": [
            "perambalur",
            "elambalur",
        ],
    }

    for district, hints in current_hints.items():

        if any(
            has_phrase(
                text,
                hint
            )
            for hint in hints
        ):

            return district

    # --------------------------------------------------------
    # EXPLICIT DISTRICT
    # --------------------------------------------------------

    district = explicit_district(
        address
    )

    if district:

        return district

    # --------------------------------------------------------
    # CHENGALPATTU SPECIAL CASE
    # --------------------------------------------------------
    # Example:
    # Siruseri, Egattur, Chennai-603103
    #
    # This must not become Chennai merely because
    # "Chennai" appears in the address.
    # --------------------------------------------------------

    if any(
        has_phrase(
            text,
            hint
        )
        for hint in CHENGALPATTU_HINTS
    ):

        return "Chengalpattu"

    # --------------------------------------------------------
    # EXACT PIN LEARNED FROM EXCEL
    # --------------------------------------------------------

    for pin in reversed(
        pins(address)
    ):

        if pin in pin_map:

            return pin_map[pin]

    # --------------------------------------------------------
    # BROAD PIN FALLBACK
    # --------------------------------------------------------

    for pin in reversed(
        pins(address)
    ):

        prefix = pin[:3]

        if prefix in PIN_PREFIX:

            return PIN_PREFIX[
                prefix
            ]

    # --------------------------------------------------------
    # LAST LOCATION MENTION
    # --------------------------------------------------------

    matches = []

    for district, aliases in DISTRICTS.items():

        for alias in aliases:

            alias = norm(alias)

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(alias)
                + r"(?![a-z0-9])"
            )

            for match in re.finditer(
                pattern,
                text
            ):

                matches.append(
                    (
                        match.start(),
                        len(alias),
                        district
                    )
                )

    if matches:

        matches.sort(
            key=lambda item:
            (
                item[0],
                item[1]
            )
        )

        return matches[-1][2]

    return "Not specified"


# ============================================================
# BRANCH MATCHING
# ============================================================

def branch_matches(
    actual,
    requested
):

    actual = norm(
        actual
    )

    exact = {

        "CSE": [
            "computer science and engineering",
            "computer science and engineering ss",
        ],

        "IT": [
            "information technology",
            "information technology ss",
        ],

        "AI_DS": [
            "artificial intelligence and data science",
            "artificial intelligence and data science ss",
        ],

        "AI_ML": [
            "artificial intelligence and machine learning",
            "artificial intelligence and machine learning ss",
        ],

        "ECE": [
            "electronics and communication engineering",
            "electronics and communication engineering ss",
        ],

        "EEE": [
            "electrical and electronics engineering",
            "electrical and electronics engineering ss",
        ],

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
            "biotechnology ss",
        ],

        "CHEMICAL": [
            "chemical engineering",
        ],

        "AGRICULTURAL": [
            "agricultural engineering",
        ],
    }

    return (
        actual
        in
        exact.get(
            requested,
            []
        )
    )


# ============================================================
# COLLEGE TYPE DETECTION
# ============================================================

def college_flags(
    row
):

    text_parts = []

    for value in row.tolist():

        if isinstance(
            value,
            str
        ):

            text_parts.append(
                value
            )

    text = norm(
        " ".join(
            text_parts
        )
    )

    aided = any(
        has_phrase(
            text,
            alias
        )
        for alias
        in TYPE_ALIASES[
            "AIDED"
        ]
    )

    autonomous = any(
        has_phrase(
            text,
            alias
        )
        for alias
        in TYPE_ALIASES[
            "AUTONOMOUS"
        ]
    )

    government = any(
        has_phrase(
            text,
            alias
        )
        for alias
        in TYPE_ALIASES[
            "GOVERNMENT"
        ]
    )

    # Government-aided is NOT treated
    # as plain government.
    if aided:

        government = False

    return (
        government,
        autonomous,
        aided
    )


# ============================================================
# MAIN RECOMMENDATION ENGINE
# ============================================================

def get_recommendations(
    cutoff,
    category,
    location,
    branch,
    college_type=None
):

    try:

        df = load_college_data().copy()

    except Exception as error:

        print(
            "DATA LOAD ERROR:",
            repr(error)
        )

        return []

    college_col = find_col(
        df,
        [
            "College Name",
            "college_name",
            "College",
        ]
    )

    branch_col = find_col(
        df,
        [
            "Branch",
            "branch",
            "Course",
            "Program",
        ]
    )

    if not college_col:

        print(
            "College Name column missing:",
            df.columns.tolist()
        )

        return []

    if not branch_col:

        print(
            "Branch column missing:",
            df.columns.tolist()
        )

        return []

    # ========================================================
    # CATEGORY
    # ========================================================

    category = (
        category.upper().strip()
        if category
        else "OC"
    )

    if category not in CATEGORIES:

        category = "OC"

    category_col = find_col(
        df,
        [category]
    )

    if not category_col:

        return []

    # ========================================================
    # BUILD DISTRICT MAP
    # ========================================================

    pin_map = build_pin_map(
        df,
        college_col
    )

    # ========================================================
    # COLLEGE TYPE FILTER
    # ========================================================

    requested_type = (
        college_type.upper().strip()
        if college_type
        else None
    )

    def type_matches(
        row
    ):

        government, autonomous, aided = (
            college_flags(row)
        )

        # User explicitly asked autonomous.
        if requested_type == "AUTONOMOUS":

            return autonomous

        # User explicitly asked government.
        if requested_type == "GOVERNMENT":

            return government

        # User explicitly asked government aided.
        if requested_type == "GOVERNMENT_AIDED":

            return aided

        # User explicitly asked both.
        if requested_type == "AUTONOMOUS_GOVERNMENT":

            return (
                autonomous
                and
                government
            )

        # IMPORTANT:
        # If user did NOT mention type,
        # show government + autonomous only.
        return (
            government
            or
            autonomous
        )

    df = df[
        df.apply(
            type_matches,
            axis=1
        )
    ].copy()

    if df.empty:

        return []

    # ========================================================
    # BRANCH FILTER
    # ========================================================

    df = df[
        df[
            branch_col
        ]
        .fillna("")
        .map(
            lambda value:
            branch_matches(
                value,
                branch
            )
        )
    ].copy()

    if df.empty:

        return []

    # ========================================================
    # DISTRICT FILTER
    # ========================================================
    # STRICT:
    # A row must belong to the requested district.
    # It is NOT allowed to match another district.
    # ========================================================

    df["__district"] = (
        df[
            college_col
        ]
        .fillna("")
        .map(
            lambda value:
            college_district(
                value,
                pin_map
            )
        )
    )

    if location:

        requested_location = (
            extract_location(
                location
            )
            or
            location
        )

        df = df[
            df[
                "__district"
            ]
            .map(norm)
            ==
            norm(
                requested_location
            )
        ].copy()

        if df.empty:

            return []

    # ========================================================
    # CUTOFF
    # ========================================================

    df["__cutoff"] = pd.to_numeric(

        df[
            category_col
        ]
        .astype(str)
        .str.replace(
            "*",
            "",
            regex=False
        )
        .str.replace(
            "—",
            "",
            regex=False
        )
        .str.strip(),

        errors="coerce"

    )

    df = df.dropna(
        subset=[
            "__cutoff"
        ]
    ).copy()

    if df.empty:

        return []

    # ========================================================
    # DIFFERENCE
    # ========================================================

    df["__difference"] = (
        float(cutoff)
        -
        df["__cutoff"]
    )

    # ========================================================
    # CHANCE
    # ========================================================

    def chance(
        difference
    ):

        if difference >= 5:

            return "Very High"

        if difference >= 0:

            return "High"

        if difference >= -10:

            return "Moderate"

        return "Low"

    df["__chance"] = (
        df[
            "__difference"
        ]
        .map(chance)
    )

    # ========================================================
    # SORT
    # ========================================================

    chance_order = {

        "Very High": 0,
        "High": 1,
        "Moderate": 2,
        "Low": 3,
    }

    df["__order"] = (
        df[
            "__chance"
        ]
        .map(
            chance_order
        )
    )

    df = df.sort_values(

        [
            "__order",
            "__cutoff",
            college_col
        ],

        ascending=[
            True,
            False,
            True
        ]

    )

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    df = df.drop_duplicates(

        subset=[
            college_col,
            branch_col
        ],

        keep="first"

    )

    # ========================================================
    # RESULT LIST
    # ========================================================

    results = []

    for rank, (_, row) in enumerate(
        df.iterrows(),
        start=1
    ):

        government, autonomous, aided = (
            college_flags(row)
        )

        if government and autonomous:

            type_name = (
                "GOVERNMENT AUTONOMOUS"
            )

        elif government:

            type_name = "GOVERNMENT"

        elif autonomous:

            type_name = "AUTONOMOUS"

        elif aided:

            type_name = "GOVERNMENT_AIDED"

        else:

            type_name = "OTHER"

        results.append({

            "rank":
                rank,

            "college_name":
                clean(
                    row[
                        college_col
                    ]
                ),

            "location":
                row[
                    "__district"
                ],

            "district":
                row[
                    "__district"
                ],

            "college_type":
                type_name,

            "branch":
                clean(
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
                ),
        })

    return results


# ============================================================
# EXTRACT ALL USER DETAILS
# ============================================================

def extract_details(
    text
):

    details = {}

    cutoff = extract_cutoff(
        text
    )

    category = extract_category(
        text
    )

    branch = extract_branch(
        text
    )

    location = extract_location(
        text
    )

    college_type = extract_type(
        text
    )

    if cutoff is not None:

        details[
            "cutoff"
        ] = cutoff

    if category:

        details[
            "category"
        ] = category

    if branch:

        details[
            "branch"
        ] = branch

    if location:

        details[
            "location"
        ] = location

    if college_type:

        details[
            "college_type"
        ] = college_type

    return details


# ============================================================
# RECOMMENDATION INTENT
# ============================================================

def recommendation_requested(
    text,
    details
):

    # Example:
    # "I need CSE in Chennai for 180 cutoff"
    if (
        details.get("cutoff")
        is not None
        and
        details.get("branch")
        is not None
    ):

        return True

    text = norm(
        text
    )

    phrases = [

        "college",
        "colleges",
        "recommend",
        "recommendation",
        "options",
        "which college",
        "which colleges",
        "show colleges",
        "find colleges",
        "admission chance",

    ]

    return any(
        phrase in text
        for phrase in phrases
    )


# ============================================================
# FALLBACK GENERAL ANSWER
# ============================================================

def fallback(
    text
):

    text = norm(
        text
    )

    if "tnea" in text:

        return (
            "TNEA stands for Tamil Nadu Engineering "
            "Admissions, the counselling process used "
            "for B.E./B.Tech admissions in Tamil Nadu."
        )

    if "counselling" in text:

        return (
            "TNEA counselling is the college and branch "
            "allotment process based on rank, choices, "
            "category and available seats."
        )

    if "branch" in text:

        return (
            "Popular branches include CSE, IT, AI & DS, "
            "ECE, EEE, Mechanical and Civil. The best "
            "branch depends on your interests and career goals."
        )

    return (
        "I'm your College Assistant. Ask me about TNEA, "
        "colleges, cutoffs, branches, counselling or admissions."
    )


# ============================================================
# MAIN CHATBOT FUNCTION
# ============================================================

def answer_question(
    user_input: str,
    history=None
) -> Tuple[str, List[Dict]]:

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

    details = extract_details(
        text
    )

    print(
        "EXTRACTED DETAILS:",
        details
    )

    # ========================================================
    # RECOMMENDATION REQUEST
    # ========================================================

    if recommendation_requested(
        text,
        details
    ):

        cutoff = details.get(
            "cutoff"
        )

        branch = details.get(
            "branch"
        )

        # IMPORTANT:
        # None means the user did NOT mention a community.
        # We never expose OC in the response in this case.
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
        # CUTOFF MISSING
        # ----------------------------------------------------

        if cutoff is None:

            return (
                "Please tell me your TNEA cutoff or marks "
                "so I can find matching colleges.",
                []
            )

        # ----------------------------------------------------
        # BRANCH MISSING
        # ----------------------------------------------------

        if branch is None:

            return (
                f"I understood your cutoff as {cutoff}. "
                "Which engineering branch do you want, "
                "such as CSE, IT, AI & DS, ECE or EEE?",
                []
            )

        # ----------------------------------------------------
        # FIND COLLEGES
        # ----------------------------------------------------

        results = get_recommendations(

            cutoff=float(
                cutoff
            ),

            category=category,

            location=location,

            branch=branch,

            college_type=college_type

        )

        # ----------------------------------------------------
        # RESPONSE TEXT
        # ----------------------------------------------------

        type_text = {

            "AUTONOMOUS":
                " autonomous",

            "GOVERNMENT":
                " government",

            "GOVERNMENT_AIDED":
                " government-aided",

            "AUTONOMOUS_GOVERNMENT":
                " autonomous government",

        }.get(
            college_type,
            ""
        )

        category_text = ""

        if category:

            category_text = (
                f" under the {category} category"
            )

        location_text = ""

        if location:

            location_text = (
                f" in {location}"
            )

        # ----------------------------------------------------
        # RESULTS FOUND
        # ----------------------------------------------------

        if results:

            reply = (

                f"I found {len(results)} matching"
                f"{type_text} college options for "
                f"{branch} with a cutoff of "
                f"{cutoff}{category_text}"
                f"{location_text}. "

                "The results are based on the "
                "TNEA cutoff data in your Excel file. "
                "Previous-year cutoffs are references "
                "only and do not guarantee admission."

            )

        # ----------------------------------------------------
        # NO RESULTS
        # ----------------------------------------------------

        else:

            reply = (

                f"I couldn't find matching"
                f"{type_text} colleges for "
                f"{branch} with a cutoff of "
                f"{cutoff}{category_text}"
                f"{location_text}. "

                "You can try another branch, "
                "location or cutoff."

            )

        return (
            reply,
            results
        )

    # ========================================================
    # GENERAL QUESTION
    # ========================================================

    if ask_llm:

        try:

            answer = ask_llm(
                text,
                history or []
            )

            if answer:

                return (
                    answer,
                    []
                )

        except Exception as error:

            print(
                "LLM ERROR:",
                repr(error)
            )

    return (
        fallback(text),
        []
    )