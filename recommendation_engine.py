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

    "ariyalur": "Ariyalur",

    "chengalpattu": "Chengalpattu",
    "chengalpet": "Chengalpattu",

    "chennai": "Chennai",

    "coimbatore": "Coimbatore",

    "cuddalore": "Cuddalore",

    "dharmapuri": "Dharmapuri",

    "dindigul": "Dindigul",

    "erode": "Erode",

    "kanchipuram": "Kanchipuram",
    "kancheepuram": "Kanchipuram",

    "karur": "Karur",

    "krishnagiri": "Krishnagiri",

    "madurai": "Madurai",

    "nagapattinam": "Nagapattinam",

    "namakkal": "Namakkal",

    "pudukkottai": "Pudukkottai",

    "ramanathapuram": "Ramanathapuram",

    "salem": "Salem",

    "sivaganga": "Sivaganga",
    "sivagangai": "Sivaganga",

    "thanjavur": "Thanjavur",
    "tanjore": "Thanjavur",

    "thoothukudi": "Thoothukudi",
    "tuticorin": "Thoothukudi",

    "tiruchirappalli": "Tiruchirappalli",
    "tiruchirapalli": "Tiruchirappalli",
    "trichy": "Tiruchirappalli",

    "tirunelveli": "Tirunelveli",

    "tiruppur": "Tiruppur",
    "tirupur": "Tiruppur",

    "tiruvallur": "Tiruvallur",
    "thiruvallur": "Tiruvallur",

    "vellore": "Vellore",

    "villupuram": "Villupuram",
    "viluppuram": "Villupuram",

    "virudhunagar": "Virudhunagar"
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

    return DISTRICT_ALIASES.get(
        text,
        text.title()
    )


# ============================================================
# EXTRACT DISTRICT FROM COLLEGE NAME
# ============================================================

def extract_location_from_college_name(
    college_name
):

    original_text = clean(
        college_name
    )

    if not original_text:

        return "Not specified"


    text = normalize_text(
        original_text
    )


    # ========================================================
    # RULE 1
    #
    # Look for explicit:
    #
    # "Salem District"
    # "Salem (Dt)"
    # "Salem Dt"
    # "Salem Dist"
    #
    # This is the strongest indication.
    # ========================================================

    explicit_matches = []

    for alias, district in DISTRICT_ALIASES.items():

        patterns = [

            r"\b"
            + re.escape(alias)
            + r"\s+district\b",

            r"\b"
            + re.escape(alias)
            + r"\s+dist\b",

            r"\b"
            + re.escape(alias)
            + r"\s+dt\b"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text
            )

            if match:

                explicit_matches.append(
                    (
                        match.start(),
                        district
                    )
                )


    if explicit_matches:

        explicit_matches.sort(
            key=lambda x: x[0]
        )

        return explicit_matches[-1][1]


    # ========================================================
    # RULE 2
    #
    # Look near the 6-digit PIN code.
    #
    # Example:
    #
    # Madurai-625104
    # -> Madurai
    #
    # Salem-636112
    # -> Salem
    #
    # Chennai-600097
    # -> Chennai
    # ========================================================

    pin_matches = list(
        re.finditer(
            r"\b\d{6}\b",
            original_text
        )
    )


    if pin_matches:

        # Use the last PIN in the address.
        pin_match = pin_matches[-1]

        pin_position = (
            pin_match.start()
        )


        # Look at the text before the PIN.
        #
        # We use a reasonably large window because
        # addresses can contain several words.

        start_position = max(
            0,
            pin_position - 100
        )


        nearby_text = normalize_text(
            original_text[
                start_position:
                pin_position
            ]
        )


        candidates = []


        for alias, district in DISTRICT_ALIASES.items():

            pattern = (
                r"\b"
                + re.escape(alias)
                + r"\b"
            )


            for match in re.finditer(
                pattern,
                nearby_text
            ):

                candidates.append(
                    (
                        match.start(),
                        district
                    )
                )


        if candidates:

            # The district closest to the PIN
            # is normally the actual location.

            candidates.sort(
                key=lambda x: x[0]
            )

            return candidates[-1][1]


    # ========================================================
    # RULE 3
    #
    # If there is no PIN or explicit district,
    # use the LAST district name in the college address.
    #
    # This is only a fallback.
    # ========================================================

    candidates = []


    for alias, district in DISTRICT_ALIASES.items():

        pattern = (
            r"\b"
            + re.escape(alias)
            + r"\b"
        )


        for match in re.finditer(
            pattern,
            text
        ):

            candidates.append(
                (
                    match.start(),
                    district
                )
            )


    if candidates:

        candidates.sort(
            key=lambda x: x[0]
        )

        return candidates[-1][1]


    # ========================================================
    # NOTHING FOUND
    # ========================================================

    return "Not specified"


# ============================================================
# NORMALIZE BRANCH
# ============================================================

def normalize_branch(value):

    text = normalize_text(
        value
    )


    mapping = {

        "cse":
            "computer science and engineering",

        "computer science engineering":
            "computer science and engineering",

        "computer science and engineering":
            "computer science and engineering",

        "computer science and engineering ss":
            "computer science and engineering",


        "it":
            "information technology",

        "information technology":
            "information technology",


        "ai ds":
            "artificial intelligence and data science",

        "ai and ds":
            "artificial intelligence and data science",

        "ai data science":
            "artificial intelligence and data science",

        "artificial intelligence data science":
            "artificial intelligence and data science",

        "artificial intelligence and data science":
            "artificial intelligence and data science",


        "ai ml":
            "artificial intelligence and machine learning",

        "ai and ml":
            "artificial intelligence and machine learning",

        "artificial intelligence machine learning":
            "artificial intelligence and machine learning",

        "artificial intelligence and machine learning":
            "artificial intelligence and machine learning",


        "ece":
            "electronics and communication engineering",

        "electronics communication engineering":
            "electronics and communication engineering",

        "electronics and communication engineering":
            "electronics and communication engineering",


        "eee":
            "electrical and electronics engineering",

        "electrical electronics engineering":
            "electrical and electronics engineering",

        "electrical and electronics engineering":
            "electrical and electronics engineering",


        "mechanical":
            "mechanical engineering",

        "mechanical engineering":
            "mechanical engineering",


        "civil":
            "civil engineering",

        "civil engineering":
            "civil engineering",


        "aeronautical":
            "aeronautical engineering",

        "aeronautical engineering":
            "aeronautical engineering",


        "aerospace":
            "aerospace engineering",

        "aerospace engineering":
            "aerospace engineering",


        "biotech":
            "biotechnology",

        "biotechnology":
            "biotechnology",


        "chemical":
            "chemical engineering",

        "chemical engineering":
            "chemical engineering",


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
        - previous_cutoff
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

    df = load_college_data().copy()


    # --------------------------------------------------------
    # Clean column names
    # --------------------------------------------------------

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]


    # --------------------------------------------------------
    # Required columns
    # --------------------------------------------------------

    if "College Name" not in df.columns:

        raise ValueError(
            "The Excel file must contain a 'College Name' column."
        )


    if "Branch" not in df.columns:

        raise ValueError(
            "The Excel file must contain a 'Branch' column."
        )


    # --------------------------------------------------------
    # Clean college names
    # --------------------------------------------------------

    df["College Name"] = (
        df["College Name"]
        .fillna("")
        .astype(str)
        .str.strip()
    )


    # --------------------------------------------------------
    # Clean branches
    # --------------------------------------------------------

    df["Branch"] = (
        df["Branch"]
        .fillna("")
        .astype(str)
        .str.strip()
    )


    # --------------------------------------------------------
    # Extract district
    # --------------------------------------------------------

    df["District"] = (
        df["College Name"]
        .apply(
            extract_location_from_college_name
        )
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
    # Load data
    # --------------------------------------------------------

    df = prepare_data()


    # --------------------------------------------------------
    # User input
    # --------------------------------------------------------

    student_cutoff = float(
        cutoff
    )


    category = str(
        category
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

        raise ValueError(
            f"Invalid category: {category}"
        )


    # ========================================================
    # DISTRICT FILTER
    # ========================================================

    if requested_district:

        district_values = (
            df["District"]
            .apply(
                normalize_district
            )
        )


        district_mask = (
            district_values
            == requested_district
        )


        # IMPORTANT:
        # Never fall back to all districts.

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
        == requested_branch
    )


    # --------------------------------------------------------
    # Fallback for branches containing additional information
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
    # No branch results
    # --------------------------------------------------------

    if df.empty:

        return []


    # ========================================================
    # CATEGORY CUTOFF
    # ========================================================

    if category not in df.columns:

        return []


    df["_cutoff"] = pd.to_numeric(
        df[category],
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
        - df["_cutoff"]
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
            True,
            True
        ]
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
            - previous_cutoff
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
                    clean(
                        row["District"]
                    ),

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