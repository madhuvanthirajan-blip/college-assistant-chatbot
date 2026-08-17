import re
import pandas as pd

from data_loader import load_college_data


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
# DISTRICT ALIASES
# ============================================================

DISTRICT_ALIASES = {

    "ariyalur":
        "Ariyalur",

    "chengalpattu":
        "Chengalpattu",

    "chengalpet":
        "Chengalpattu",

    "chennai":
        "Chennai",

    "coimbatore":
        "Coimbatore",

    "cuddalore":
        "Cuddalore",

    "dharmapuri":
        "Dharmapuri",

    "dindigul":
        "Dindigul",

    "erode":
        "Erode",

    "kanchipuram":
        "Kanchipuram",

    "kancheepuram":
        "Kanchipuram",

    "karur":
        "Karur",

    "krishnagiri":
        "Krishnagiri",

    "madurai":
        "Madurai",

    "nagapattinam":
        "Nagapattinam",

    "namakkal":
        "Namakkal",

    "pudukkottai":
        "Pudukkottai",

    "ramanathapuram":
        "Ramanathapuram",

    "salem":
        "Salem",

    "sivaganga":
        "Sivaganga",

    "sivagangai":
        "Sivaganga",

    "thanjavur":
        "Thanjavur",

    "tanjore":
        "Thanjavur",

    "thoothukudi":
        "Thoothukudi",

    "tuticorin":
        "Thoothukudi",

    "tiruchirappalli":
        "Tiruchirappalli",

    "tiruchirapalli":
        "Tiruchirappalli",

    "trichy":
        "Tiruchirappalli",

    "tiruchi":
        "Tiruchirappalli",

    "tirunelveli":
        "Tirunelveli",

    "tiruppur":
        "Tiruppur",

    "tirupur":
        "Tiruppur",

    "tiruvallur":
        "Tiruvallur",

    "thiruvallur":
        "Tiruvallur",

    "vellore":
        "Vellore",

    "villupuram":
        "Villupuram",

    "viluppuram":
        "Villupuram",

    "virudhunagar":
        "Virudhunagar",

    "mayiladuthurai":
        "Mayiladuthurai",

    "tenkasi":
        "Tenkasi",

    "kallakurichi":
        "Kallakurichi",

    "perambalur":
        "Perambalur",

    "ranipet":
        "Ranipet",

    "tirupattur":
        "Tirupattur"
}


# ============================================================
# CLEAN VALUE
# ============================================================

def clean(value):

    if pd.isna(value):
        return ""

    return str(value).strip()


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(value):

    value = clean(value)

    value = value.lower()

    value = value.replace("&", " and ")

    value = re.sub(
        r"[^a-z0-9\s]",
        " ",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


# ============================================================
# NORMALIZE DISTRICT
# ============================================================

def normalize_district(value):

    text = normalize_text(value)

    if not text:
        return ""

    # Direct alias
    if text in DISTRICT_ALIASES:

        return DISTRICT_ALIASES[text]


    # Remove common words around district names

    text = re.sub(
        r"\bdistrict\b",
        "",
        text
    ).strip()


    text = re.sub(
        r"\bdist\b",
        "",
        text
    ).strip()


    text = re.sub(
        r"\bdt\b",
        "",
        text
    ).strip()


    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()


    if text in DISTRICT_ALIASES:

        return DISTRICT_ALIASES[text]


    return text.title()


# ============================================================
# FIND COLUMN
# ============================================================

def find_column(
    df,
    possible_names
):

    normalized_columns = {

        normalize_text(column):
            column

        for column in df.columns

    }


    for name in possible_names:

        normalized_name = normalize_text(
            name
        )


        if normalized_name in normalized_columns:

            return normalized_columns[
                normalized_name
            ]


    return None


# ============================================================
# NORMALIZE BRANCH
# ============================================================

def normalize_branch(value):

    text = normalize_text(
        value
    )


    mapping = {

        # ------------------------------
        # CSE
        # ------------------------------

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

        "computer science and engineering ss":
            "computer science and engineering",


        # ------------------------------
        # IT
        # ------------------------------

        "it":
            "information technology",

        "information technology":
            "information technology",

        "information tech":
            "information technology",


        # ------------------------------
        # AI & DS
        # ------------------------------

        "ai ds":
            "artificial intelligence and data science",

        "ai and ds":
            "artificial intelligence and data science",

        "ai data science":
            "artificial intelligence and data science",

        "ai and data science":
            "artificial intelligence and data science",

        "artificial intelligence data science":
            "artificial intelligence and data science",

        "artificial intelligence and data science":
            "artificial intelligence and data science",

        "aids":
            "artificial intelligence and data science",


        # ------------------------------
        # AI & ML
        # ------------------------------

        "ai ml":
            "artificial intelligence and machine learning",

        "ai and ml":
            "artificial intelligence and machine learning",

        "ai machine learning":
            "artificial intelligence and machine learning",

        "artificial intelligence machine learning":
            "artificial intelligence and machine learning",

        "artificial intelligence and machine learning":
            "artificial intelligence and machine learning",

        "aiml":
            "artificial intelligence and machine learning",


        # ------------------------------
        # ECE
        # ------------------------------

        "ece":
            "electronics and communication engineering",

        "electronics":
            "electronics and communication engineering",

        "electronics communication":
            "electronics and communication engineering",

        "electronics and communication":
            "electronics and communication engineering",

        "electronics communication engineering":
            "electronics and communication engineering",

        "electronics and communication engineering":
            "electronics and communication engineering",


        # ------------------------------
        # EEE
        # ------------------------------

        "eee":
            "electrical and electronics engineering",

        "electrical":
            "electrical and electronics engineering",

        "electrical electronics":
            "electrical and electronics engineering",

        "electrical and electronics":
            "electrical and electronics engineering",

        "electrical electronics engineering":
            "electrical and electronics engineering",

        "electrical and electronics engineering":
            "electrical and electronics engineering",


        # ------------------------------
        # MECHANICAL
        # ------------------------------

        "mechanical":
            "mechanical engineering",

        "mechanical engineering":
            "mechanical engineering",


        # ------------------------------
        # CIVIL
        # ------------------------------

        "civil":
            "civil engineering",

        "civil engineering":
            "civil engineering",


        # ------------------------------
        # AERONAUTICAL
        # ------------------------------

        "aeronautical":
            "aeronautical engineering",

        "aeronautical engineering":
            "aeronautical engineering",


        # ------------------------------
        # AEROSPACE
        # ------------------------------

        "aerospace":
            "aerospace engineering",

        "aerospace engineering":
            "aerospace engineering",


        # ------------------------------
        # BIOTECHNOLOGY
        # ------------------------------

        "biotech":
            "biotechnology",

        "bio technology":
            "biotechnology",

        "biotechnology":
            "biotechnology",


        # ------------------------------
        # CHEMICAL
        # ------------------------------

        "chemical":
            "chemical engineering",

        "chemical engineering":
            "chemical engineering",


        # ------------------------------
        # AGRICULTURAL
        # ------------------------------

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
# CHANCE CALCULATION
# ============================================================

def get_chance(
    student_cutoff,
    previous_cutoff
):

    if pd.isna(
        previous_cutoff
    ):

        return "Data unavailable"


    difference = (
        student_cutoff
        -
        previous_cutoff
    )


    if difference >= 0:

        return "Very High"

    elif difference >= -5:

        return "High"

    elif difference >= -10:

        return "Moderate"

    else:

        return "Low"


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data():

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    df = load_college_data().copy()


    # --------------------------------------------------------
    # CLEAN COLUMN NAMES
    # --------------------------------------------------------

    df.columns = [

        str(column).strip()

        for column in df.columns

    ]


    # --------------------------------------------------------
    # FIND IMPORTANT COLUMNS
    # --------------------------------------------------------

    college_col = find_column(
        df,
        [
            "College Name",
            "college_name",
            "College"
        ]
    )


    branch_col = find_column(
        df,
        [
            "Branch",
            "branch"
        ]
    )


    district_col = find_column(
        df,
        [
            "District",
            "district",
            "District Name",
            "district_name"
        ]
    )


    # --------------------------------------------------------
    # REQUIRED COLUMN CHECK
    # --------------------------------------------------------

    if not college_col:

        raise ValueError(
            "The dataset must contain a "
            "'College Name' column."
        )


    if not branch_col:

        raise ValueError(
            "The dataset must contain a "
            "'Branch' column."
        )


    if not district_col:

        raise ValueError(
            "The dataset must contain a "
            "'District' column. "
            "District must come from the "
            "dataset and must not be guessed "
            "from the college address."
        )


    # --------------------------------------------------------
    # STANDARDIZE COLUMN NAMES
    # --------------------------------------------------------

    if college_col != "College Name":

        df.rename(
            columns={
                college_col:
                    "College Name"
            },
            inplace=True
        )


    if branch_col != "Branch":

        df.rename(
            columns={
                branch_col:
                    "Branch"
            },
            inplace=True
        )


    if district_col != "District":

        df.rename(
            columns={
                district_col:
                    "District"
            },
            inplace=True
        )


    # --------------------------------------------------------
    # CLEAN COLLEGE NAME
    # --------------------------------------------------------

    df["College Name"] = (

        df["College Name"]
        .fillna("")
        .astype(str)
        .str.strip()

    )


    # --------------------------------------------------------
    # CLEAN BRANCH
    # --------------------------------------------------------

    df["Branch"] = (

        df["Branch"]
        .fillna("")
        .astype(str)
        .str.strip()

    )


    # ========================================================
    # IMPORTANT DISTRICT FIX
    #
    # USE THE ACTUAL DISTRICT COLUMN FROM EXCEL.
    #
    # DO NOT extract district from College Name.
    # ========================================================

    df["District"] = (

        df["District"]
        .fillna("")
        .astype(str)
        .str.strip()

    )


    # --------------------------------------------------------
    # NORMALIZE DISTRICT
    # --------------------------------------------------------

    df["District_Normalized"] = (

        df["District"]
        .apply(
            normalize_district
        )

    )


    # --------------------------------------------------------
    # REMOVE ROWS WITHOUT VALID DISTRICT
    # --------------------------------------------------------

    df = df[
        df["District_Normalized"]
        != ""
    ].copy()


    # --------------------------------------------------------
    # RESET INDEX
    # --------------------------------------------------------

    df.reset_index(
        drop=True,
        inplace=True
    )


    return df


# ============================================================
# MAIN RECOMMENDATION FUNCTION
# ============================================================

def recommend(
    cutoff,
    category,
    district,
    branch,
    limit=None
):

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    df = prepare_data()


    # --------------------------------------------------------
    # USER INPUT
    # --------------------------------------------------------

    try:

        student_cutoff = float(
            cutoff
        )

    except (
        ValueError,
        TypeError
    ):

        return []


    category = str(
        category
        or "OC"
    ).strip().upper()


    requested_district = normalize_district(
        district
    )


    requested_branch = normalize_branch(
        branch
    )


    # ========================================================
    # CATEGORY CHECK
    # ========================================================

    if category not in CATEGORY_COLUMNS:

        return []


    # ========================================================
    # DISTRICT FILTER
    # ========================================================

    if requested_district:

        district_mask = (

            df["District_Normalized"]
            ==
            requested_district

        )


        # ----------------------------------------------------
        # NEVER FALL BACK TO OTHER DISTRICTS
        # ----------------------------------------------------

        if not district_mask.any():

            return []


        df = df[
            district_mask
        ].copy()


    # ========================================================
    # BRANCH FILTER
    # ========================================================

    dataset_branches = (

        df["Branch"]
        .apply(
            normalize_branch
        )

    )


    branch_mask = (

        dataset_branches
        ==
        requested_branch

    )


    # --------------------------------------------------------
    # BRANCH FALLBACK
    # --------------------------------------------------------

    if not branch_mask.any():

        branch_mask = (

            dataset_branches
            .str.contains(
                re.escape(
                    requested_branch
                ),
                na=False,
                regex=True
            )

        )


    df = df[
        branch_mask
    ].copy()


    # --------------------------------------------------------
    # NO RESULTS
    # --------------------------------------------------------

    if df.empty:

        return []


    # ========================================================
    # CATEGORY CUTOFF
    # ========================================================

    if category not in df.columns:

        return []


    df["_cutoff"] = pd.to_numeric(

        df[category]
        .astype(str)
        .str.replace(
            "*",
            "",
            regex=False
        )
        .str.strip(),

        errors="coerce"

    )


    df = df.dropna(
        subset=[
            "_cutoff"
        ]
    ).copy()


    if df.empty:

        return []


    # ========================================================
    # CUTOFF DIFFERENCE
    # ========================================================

    df["_difference"] = (

        student_cutoff
        -
        df["_cutoff"]

    )


    # ========================================================
    # CHANCE ORDER
    # ========================================================

    def chance_order(
        difference
    ):

        if difference >= 0:

            return 0

        elif difference >= -5:

            return 1

        elif difference >= -10:

            return 2

        else:

            return 3


    df["_chance_order"] = (

        df["_difference"]
        .apply(
            chance_order
        )

    )


    # ========================================================
    # SORT RESULTS
    # ========================================================

    df = df.sort_values(

        by=[
            "_chance_order",
            "_cutoff",
            "College Name"
        ],

        ascending=[
            True,
            False,
            True
        ]

    )


    # ========================================================
    # REMOVE DUPLICATES
    #
    # One college + one branch = one result
    # ========================================================

    df = df.drop_duplicates(

        subset=[
            "College Name",
            "Branch"
        ],

        keep="first"

    )


    # ========================================================
    # LIMIT
    # ========================================================

    if limit is not None:

        df = df.head(
            int(limit)
        )


    # ========================================================
    # BUILD RESULTS
    # ========================================================

    results = []


    for rank, (
        index,
        row
    ) in enumerate(

        df.iterrows(),

        start=1

    ):

        previous_cutoff = float(
            row["_cutoff"]
        )


        difference = (

            student_cutoff
            -
            previous_cutoff

        )


        # ----------------------------------------------------
        # USE ACTUAL EXCEL DISTRICT
        # ----------------------------------------------------

        actual_district = (
            clean(
                row["District"]
            )
        )


        # ----------------------------------------------------
        # NORMALIZE ONLY FOR DISPLAY
        # ----------------------------------------------------

        display_district = (

            normalize_district(
                actual_district
            )

            or

            actual_district

        )


        results.append(

            {

                "rank":
                    rank,


                "college_name":
                    clean(
                        row["College Name"]
                    ),


                "district":
                    display_district,


                "location":
                    display_district,


                "branch":
                    clean(
                        row["Branch"]
                    ),


                "cutoff":
                    previous_cutoff,


                "chance":
                    get_chance(
                        student_cutoff,
                        previous_cutoff
                    ),


                "cutoff_difference":
                    round(
                        difference,
                        2
                    )

            }

        )


    return results