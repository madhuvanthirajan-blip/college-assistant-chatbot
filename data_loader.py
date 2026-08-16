from pathlib import Path
import pandas as pd


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


# ============================================================
# LOAD TNEA EXCEL / CSV DATA
# ============================================================

def load_college_data():

    excel_file = DATA_DIR / "college_cutoffs.xlsx"
    csv_file = DATA_DIR / "college_cutoffs.csv"

    # --------------------------------------------------------
    # Excel file
    # --------------------------------------------------------

    if excel_file.exists():

        # The TNEA Excel file has:
        # Row 1 -> title
        # Row 2 -> actual column headers
        # Row 3 onwards -> college data

        df = pd.read_excel(
            excel_file,
            sheet_name=0,
            header=1
        )

    # --------------------------------------------------------
    # CSV fallback
    # --------------------------------------------------------

    elif csv_file.exists():

        df = pd.read_csv(csv_file)

    else:

        raise FileNotFoundError(
            "No college dataset found. "
            "Put college_cutoffs.xlsx inside the data folder."
        )

    # ========================================================
    # CLEAN COLUMN NAMES
    # ========================================================

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    # ========================================================
    # REMOVE COMPLETELY EMPTY COLUMNS
    # ========================================================

    df = df.dropna(
        axis=1,
        how="all"
    )

    # ========================================================
    # REMOVE COMPLETELY EMPTY ROWS
    # ========================================================

    df = df.dropna(
        axis=0,
        how="all"
    )

    # ========================================================
    # CLEAN TEXT COLUMNS
    # ========================================================

    for column in ["College Name", "Branch"]:

        if column in df.columns:

            df[column] = (
                df[column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    # ========================================================
    # CLEAN CUTOFF COLUMNS
    # ========================================================

    cutoff_columns = [
        "OC",
        "BC",
        "BCM",
        "MBC",
        "SC",
        "SCA",
        "ST"
    ]

    for column in cutoff_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # ========================================================
    # RESET INDEX
    # ========================================================

    df = df.reset_index(
        drop=True
    )

    return df