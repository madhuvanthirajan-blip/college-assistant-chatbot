import re
from typing import Optional, List, Dict

import pandas as pd

from data_loader import load_college_data


# ============================================================
# DISTRICT ALIASES
# ============================================================
# IMPORTANT:
# The District column in the source dataset is NOT trusted.
# District is calculated from the actual college address.
# ============================================================

DISTRICT_ALIASES = {

    "Ariyalur": [
        "ariyalur"
    ],

    "Chengalpattu": [
        "chengalpattu",
        "chengalpet",
        "chengalpat"
    ],

    "Chennai": [
        "chennai",
        "madras"
    ],

    "Coimbatore": [
        "coimbatore",
        "kovai"
    ],

    "Cuddalore": [
        "cuddalore"
    ],

    "Dharmapuri": [
        "dharmapuri"
    ],

    "Dindigul": [
        "dindigul"
    ],

    "Erode": [
        "erode"
    ],

    "Kallakurichi": [
        "kallakurichi"
    ],

    "Kancheepuram": [
        "kancheepuram",
        "kanchipuram"
    ],

    "Karur": [
        "karur"
    ],

    "Krishnagiri": [
        "krishnagiri"
    ],

    "Madurai": [
        "madurai"
    ],

    "Mayiladuthurai": [
        "mayiladuthurai",
        "mayavaram"
    ],

    "Nagapattinam": [
        "nagapattinam"
    ],

    "Namakkal": [
        "namakkal"
    ],

    "Perambalur": [
        "perambalur"
    ],

    "Pudukkottai": [
        "pudukkottai",
        "pudukottai"
    ],

    "Ramanathapuram": [
        "ramanathapuram",
        "ramnad"
    ],

    "Ranipet": [
        "ranipet"
    ],

    "Salem": [
        "salem"
    ],

    "Sivaganga": [
        "sivaganga",
        "sivagangai"
    ],

    "Tenkasi": [
        "tenkasi"
    ],

    "Thanjavur": [
        "thanjavur",
        "tanjore"
    ],

    "The Nilgiris": [
        "nilgiris",
        "the nilgiris",
        "ooty",
        "udhagamandalam"
    ],

    "Theni": [
        "theni"
    ],

    "Thoothukudi": [
        "thoothukudi",
        "tuticorin"
    ],

    "Tiruchirappalli": [
        "tiruchirappalli",
        "tiruchirapalli",
        "trichy",
        "tiruchi"
    ],

    "Tirunelveli": [
        "tirunelveli",
        "nellai"
    ],

    "Tirupattur": [
        "tirupattur",
        "tirupathur"
    ],

    "Tiruppur": [
        "tiruppur",
        "tirupur"
    ],

    "Tiruvallur": [
        "tiruvallur",
        "thiruvallur"
    ],

    "Tiruvannamalai": [
        "tiruvannamalai",
        "thiruvannamalai"
    ],

    "Tiruvarur": [
        "tiruvarur",
        "thiruvarur"
    ],

    "Vellore": [
        "vellore"
    ],

    "Viluppuram": [
        "viluppuram",
        "villupuram",
        "vizhuppuram"
    ],

    "Virudhunagar": [
        "virudhunagar"
    ],

    "Kanyakumari": [
        "kanyakumari",
        "nagercoil"
    ]
}


# ============================================================
# PIN CODE DISTRICT RULES
# ============================================================
# These are used only where the broad PIN prefix is reliable.
#
# VERY IMPORTANT:
#
# 603xxx -> Chengalpattu
# 600xxx -> Chennai
#
# Therefore:
#
# Chennai-603103
#
# will NOT be classified as Chennai.
# It will be classified as Chengalpattu.
# ============================================================

PIN_PREFIX_DISTRICTS = {

    "603": "Chengalpattu",

    "600": "Chennai",

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

    "635": "Tirupattur",

    "636": "Salem",

    "637": "Namakkal",

    "638": "Erode",

    "639": "Karur",

    "641": "Coimbatore",

    "642": "Coimbatore",

    "643": "The Nilgiris"
}


# ============================================================
# CATEGORY COLUMNS
# ============================================================

CATEGORY_COLUMNS = [
    "OC",
    "BC",
    "BCM",
    "MBC",
    "SC",
    "SCA",
    "ST"
]


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(value) -> str:

    if value is None:
        return ""

    try:

        if pd.isna(value):
            return ""

    except Exception:
        pass

    return str(value).strip()


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(value) -> str:

    text = clean_text(value)

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

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# NORMALIZE DISTRICT
# ============================================================

def normalize_district(value) -> str:

    text = normalize_text(value)

    text = re.sub(
        r"\b(district|dist|dt)\b",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    for district, aliases in DISTRICT_ALIASES.items():

        if text == normalize_text(district):

            return district

        for alias in aliases:

            if text == normalize_text(alias):

                return district

    if text:

        return text.title()

    return ""


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

        normalized_name = normalize_text(
            name
        )

        if normalized_name in normalized_columns:

            return normalized_columns[
                normalized_name
            ]

    return None


# ============================================================
# EXTRACT PIN CODE
# ============================================================

def extract_pincode(
    text: str
) -> Optional[str]:

    matches = re.findall(
        r"\b\d{6}\b",
        clean_text(text)
    )

    if not matches:

        return None

    return matches[-1]


# ============================================================
# DISTRICT FROM PIN CODE
# ============================================================

def district_from_pincode(
    pincode: Optional[str]
) -> Optional[str]:

    if not pincode:

        return None

    for prefix, district in PIN_PREFIX_DISTRICTS.items():

        if pincode.startswith(prefix):

            return district

    return None


# ============================================================
# EXTRACT DISTRICT FROM ADDRESS
# ============================================================

def extract_district_from_address(
    address: str
) -> str:

    original = clean_text(
        address
    )

    if not original:

        return "Not specified"


    normalized = normalize_text(
        original
    )


    # ========================================================
    # RULE 1
    #
    # EXPLICIT DISTRICT NAME
    #
    # Example:
    #
    # Chengalpattu District
    # Kancheepuram District
    # Cuddalore District
    #
    # This has the highest priority.
    # ========================================================

    explicit_matches = []


    for district, aliases in DISTRICT_ALIASES.items():

        for alias in aliases:

            alias_normalized = normalize_text(
                alias
            )

            pattern = (

                r"(?<![a-z0-9])"

                +

                re.escape(
                    alias_normalized
                )

                +

                r"\s+"

                r"(?:district|dist|dt)"

                r"\b"

            )


            for match in re.finditer(
                pattern,
                normalized,
                flags=re.IGNORECASE
            ):

                explicit_matches.append(
                    (
                        match.start(),
                        district
                    )
                )


    if explicit_matches:

        explicit_matches.sort(
            key=lambda item: item[0]
        )

        return explicit_matches[-1][1]


    # ========================================================
    # RULE 2
    #
    # PIN CODE
    #
    # Example:
    #
    # Chennai-603103
    #
    # 603103 -> Chengalpattu
    #
    # This is the important correction.
    # ========================================================

    pincode = extract_pincode(
        original
    )


    pin_district = district_from_pincode(
        pincode
    )


    if pin_district:

        return pin_district


    # ========================================================
    # RULE 3
    #
    # DISTRICT/CITY NAME IN ADDRESS
    # ========================================================

    location_matches = []


    for district, aliases in DISTRICT_ALIASES.items():

        for alias in aliases:

            alias_normalized = normalize_text(
                alias
            )


            pattern = (

                r"(?<![a-z0-9])"

                +

                re.escape(
                    alias_normalized
                )

                +

                r"(?![a-z0-9])"

            )


            for match in re.finditer(
                pattern,
                normalized,
                flags=re.IGNORECASE
            ):

                location_matches.append(
                    (
                        match.start(),
                        len(alias_normalized),
                        district
                    )
                )


    if location_matches:

        location_matches.sort(
            key=lambda item: (
                item[0],
                item[1]
            )
        )

        return location_matches[-1][2]


    return "Not specified"


# ============================================================
# CLEAN COLLEGE NAME
# ============================================================

def extract_clean_college_name(
    college_name: str
) -> str:

    text = clean_text(
        college_name
    )

    if not text:

        return "Unknown College"


    # Keep only the college name.
    #
    # The address remains available separately.
    # ========================================================

    name = text.split(
        ",",
        1
    )[0].strip()


    name = re.sub(
        r"\s+",
        " ",
        name
    )


    name = name.strip(
        " .,-"
    )


    return name or text


# ============================================================
# EXTRACT ADDRESS
# ============================================================

def extract_address(
    college_name: str
) -> str:

    return clean_text(
        college_name
    )


# ============================================================
# BRANCH NORMALIZATION
# ============================================================

def normalize_branch(
    value
) -> str:

    text = normalize_text(
        value
    )


    mapping = {

        # ----------------------------------------------------
        # CSE
        # ----------------------------------------------------

        "cse":
            "computer science and engineering",

        "cs":
            "computer science and engineering",

        "computer science":
            "computer science and engineering",

        "computer science engineering":
            "computer science and engineering",

        "computer science and engineering":
            "computer science and engineering",


        # ----------------------------------------------------
        # IT
        # ----------------------------------------------------

        "it":
            "information technology",

        "information tech":
            "information technology",

        "information technology":
            "information technology",


        # ----------------------------------------------------
        # AI & DS
        # ----------------------------------------------------

        "ai ds":
            "artificial intelligence and data science",

        "ai and ds":
            "artificial intelligence and data science",

        "aids":
            "artificial intelligence and data science",

        "artificial intelligence data science":
            "artificial intelligence and data science",

        "artificial intelligence and data science":
            "artificial intelligence and data science",


        # ----------------------------------------------------
        # AI & ML
        # ----------------------------------------------------

        "ai ml":
            "artificial intelligence and machine learning",

        "ai and ml":
            "artificial intelligence and machine learning",

        "aiml":
            "artificial intelligence and machine learning",

        "artificial intelligence machine learning":
            "artificial intelligence and machine learning",

        "artificial intelligence and machine learning":
            "artificial intelligence and machine learning",


        # ----------------------------------------------------
        # ECE
        # ----------------------------------------------------

        "ece":
            "electronics and communication engineering",

        "electronics communication engineering":
            "electronics and communication engineering",

        "electronics and communication engineering":
            "electronics and communication engineering",


        # ----------------------------------------------------
        # EEE
        # ----------------------------------------------------

        "eee":
            "electrical and electronics engineering",

        "electrical electronics engineering":
            "electrical and electronics engineering",

        "electrical and electronics engineering":
            "electrical and electronics engineering",


        # ----------------------------------------------------
        # MECHANICAL
        # ----------------------------------------------------

        "mechanical":
            "mechanical engineering",

        "mechanical engineering":
            "mechanical engineering",


        # ----------------------------------------------------
        # CIVIL
        # ----------------------------------------------------

        "civil":
            "civil engineering",

        "civil engineering":
            "civil engineering",


        # ----------------------------------------------------
        # AERONAUTICAL
        # ----------------------------------------------------

        "aeronautical":
            "aeronautical engineering",

        "aeronautical engineering":
            "aeronautical engineering",


        # ----------------------------------------------------
        # AEROSPACE
        # ----------------------------------------------------

        "aerospace":
            "aerospace engineering",

        "aerospace engineering":
            "aerospace engineering",


        # ----------------------------------------------------
        # BIOTECHNOLOGY
        # ----------------------------------------------------

        "biotech":
            "biotechnology",

        "bio technology":
            "biotechnology",

        "biotechnology":
            "biotechnology",


        # ----------------------------------------------------
        # CHEMICAL
        # ----------------------------------------------------

        "chemical":
            "chemical engineering",

        "chemical engineering":
            "chemical engineering",


        # ----------------------------------------------------
        # AGRICULTURAL
        # ----------------------------------------------------

        "agricultural":
            "agricultural engineering",

        "agricultural engineering":
            "agricultural engineering"
    }


    return mapping.get(
        text,
        text
    )


# ============================================================
# BRANCH MATCH
# ============================================================

def branch_matches(
    dataset_branch: str,
    requested_branch: str
) -> bool:

    dataset_normalized = normalize_branch(
        dataset_branch
    )

    requested_normalized = normalize_branch(
        requested_branch
    )


    if not dataset_normalized:

        return False


    if not requested_normalized:

        return False


    return (

        dataset_normalized
        ==
        requested_normalized

        or

        requested_normalized
        in
        dataset_normalized

    )


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data() -> pd.DataFrame:

    df = load_college_data().copy()


    # ========================================================
    # CLEAN COLUMN NAMES
    # ========================================================

    df.columns = [

        str(column).strip()

        for column in df.columns

    ]


    # ========================================================
    # FIND COLLEGE COLUMN
    # ========================================================

    college_column = find_column(

        df,

        [
            "College Name",
            "college_name",
            "College",
            "CollegeName"
        ]

    )


    if not college_column:

        raise ValueError(
            "The dataset must contain a College Name column."
        )


    # ========================================================
    # FIND BRANCH COLUMN
    # ========================================================

    branch_column = find_column(

        df,

        [
            "Branch",
            "branch",
            "Branch Name",
            "Course",
            "Program"
        ]

    )


    if not branch_column:

        raise ValueError(
            "The dataset must contain a Branch column."
        )


    if college_column != "College Name":

        df.rename(

            columns={
                college_column:
                    "College Name"
            },

            inplace=True

        )


    if branch_column != "Branch":

        df.rename(

            columns={
                branch_column:
                    "Branch"
            },

            inplace=True

        )


    # ========================================================
    # CLEAN VALUES
    # ========================================================

    df["College Name"] = (

        df["College Name"]

        .fillna("")

        .astype(str)

        .str.strip()

    )


    df["Branch"] = (

        df["Branch"]

        .fillna("")

        .astype(str)

        .str.strip()

    )


    # ========================================================
    # CRITICAL DISTRICT FIX
    # ========================================================
    #
    # DO NOT USE:
    #
    # df["District"]
    #
    # Instead, calculate District from the actual address.
    #
    # ========================================================

    df["Address"] = (

        df["College Name"]

        .apply(
            extract_address
        )

    )


    df["District"] = (

        df["Address"]

        .apply(
            extract_district_from_address
        )

    )


    df["District"] = (

        df["District"]

        .apply(
            normalize_district
        )

    )


    # ========================================================
    # CLEAN DISPLAY NAME
    # ========================================================

    df["Display College Name"] = (

        df["College Name"]

        .apply(
            extract_clean_college_name
        )

    )


    return df.reset_index(
        drop=True
    )


# ============================================================
# CORRECTED DISTRICT LIST
# ============================================================

def get_corrected_districts() -> List[str]:

    df = prepare_data()


    districts = sorted({

        district

        for district in df["District"].tolist()

        if district
        and
        district != "Not Specified"

    })


    return districts


# ============================================================
# CORRECTED DATA
# ============================================================

def get_corrected_data() -> pd.DataFrame:

    return prepare_data()


# ============================================================
# CHANCE CALCULATION
# ============================================================

def calculate_chance(
    difference: float
) -> str:

    if difference >= 5:

        return "Very High"


    elif difference >= 0:

        return "High"


    elif difference >= -10:

        return "Moderate"


    else:

        return "Low"


# ============================================================
# RECOMMENDATION
# ============================================================

def recommend(
    cutoff: float,
    category: str,
    district: str,
    branch: str,
    limit=None
) -> List[Dict]:

    # ========================================================
    # LOAD CORRECTED DATA
    # ========================================================

    df = prepare_data()


    # ========================================================
    # CUTOFF
    # ========================================================

    try:

        student_cutoff = float(
            cutoff
        )

    except (
        ValueError,
        TypeError
    ):

        return []


    if not (
        0 <= student_cutoff <= 200
    ):

        return []


    # ========================================================
    # CATEGORY
    # ========================================================

    category = str(
        category or "OC"
    ).strip().upper()


    if category not in CATEGORY_COLUMNS:

        return []


    # ========================================================
    # DISTRICT
    # ========================================================

    requested_district = normalize_district(
        district
    )


    # ========================================================
    # STRICT DISTRICT FILTER
    #
    # The corrected District column is used here.
    #
    # If user selects:
    #
    # Chengalpattu
    #
    # only address-derived Chengalpattu records are returned.
    #
    # Chennai records are NOT returned.
    # ========================================================

    if requested_district:

        df = df[

            df["District"]

            .apply(
                normalize_district
            )

            ==

            requested_district

        ].copy()


    # ========================================================
    # BRANCH FILTER
    # ========================================================

    df = df[

        df["Branch"]

        .apply(

            lambda value:

            branch_matches(
                value,
                branch
            )

        )

    ].copy()


    # ========================================================
    # NO RESULTS
    # ========================================================

    if df.empty:

        return []


    # ========================================================
    # CATEGORY COLUMN
    # ========================================================

    if category not in df.columns:

        return []


    # ========================================================
    # PREVIOUS CUTOFF
    # ========================================================

    df["__cutoff"] = pd.to_numeric(

        df[category]

        .astype(str)

        .str.replace(
            "*",
            "",
            regex=False
        )

        .str.replace(
            ",",
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

        student_cutoff
        -
        df["__cutoff"]

    )


    # ========================================================
    # CHANCE
    # ========================================================

    df["__chance"] = (

        df["__difference"]

        .apply(
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

        "Low": 3

    }


    df["__chance_order"] = (

        df["__chance"]

        .map(
            chance_order
        )

    )


    # ========================================================
    # SORT
    # ========================================================

    df = df.sort_values(

        [

            "__chance_order",

            "__cutoff",

            "Display College Name"

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

            "Display College Name",

            "Branch"

        ],

        keep="first"

    )


    # ========================================================
    # LIMIT
    # ========================================================

    if limit is not None:

        try:

            df = df.head(
                int(limit)
            )

        except (
            ValueError,
            TypeError
        ):

            pass


    # ========================================================
    # RESULT LIST
    # ========================================================

    results = []


    for _, row in df.iterrows():

        previous_cutoff = float(
            row["__cutoff"]
        )


        difference = float(
            row["__difference"]
        )


        result_district = normalize_district(
            row["District"]
        )


        # ====================================================
        # FINAL SAFETY CHECK
        # ====================================================

        if requested_district:

            if (
                result_district
                !=
                requested_district
            ):

                continue


        results.append({

            "rank":
                len(results) + 1,

            "college_name":
                clean_text(
                    row[
                        "Display College Name"
                    ]
                ),

            "address":
                clean_text(
                    row[
                        "Address"
                    ]
                ),

            "district":
                result_district,

            "location":
                result_district,

            "branch":
                clean_text(
                    row[
                        "Branch"
                    ]
                ),

            "cutoff":
                previous_cutoff,

            "chance":
                calculate_chance(
                    difference
                ),

            "cutoff_difference":
                round(
                    difference,
                    2
                )

        })


    return results