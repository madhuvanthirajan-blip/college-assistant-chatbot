from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


REQUIRED_COLUMNS = {
    "College Name",
    "Branch",
    "OC",
    "BC",
    "BCM",
    "MBC",
    "SC",
    "SCA",
    "ST",
}


def clean_excel_headers(df):
    """
    Fix the TNEA 2025 Excel structure.

    The workbook has:
        Row 1 -> title
        Row 2 -> actual column headers
        Row 3 onward -> data
    """

    # Already correctly loaded
    current_columns = {
        str(column).strip()
        for column in df.columns
    }

    if REQUIRED_COLUMNS.issubset(current_columns):
        df.columns = [
            str(column).strip()
            for column in df.columns
        ]
        return df

    # Search first few rows for the actual header
    for row_index in range(min(10, len(df))):

        row_values = {
            str(value).strip()
            for value in df.iloc[row_index].tolist()
        }

        if REQUIRED_COLUMNS.issubset(row_values):

            header = [
                str(value).strip()
                for value in df.iloc[row_index].tolist()
            ]

            cleaned = df.iloc[row_index + 1:].copy()

            cleaned.columns = header

            cleaned = cleaned.reset_index(drop=True)

            return cleaned

    raise ValueError(
        "Could not find the real TNEA column header row."
    )


def load_college_data():
    """
    Load the TNEA college cutoff dataset.
    """

    DATA_DIR.mkdir(
        exist_ok=True
    )

    files = [
        DATA_DIR / "college_cutoffs.xlsx",
        DATA_DIR / "college_cutoffs.xls",
        DATA_DIR / "college_cutoffs.csv",
    ]

    for path in files:

        if not path.exists():
            continue

        print(
            f"Loading college data from: {path}"
        )

        if path.suffix.lower() == ".csv":

            df = pd.read_csv(path)

        else:

            # IMPORTANT:
            # Read without assuming the first row is the header.
            df = pd.read_excel(
                path,
                header=None
            )

        df = clean_excel_headers(
            df
        )

        # Remove completely empty rows
        df = df.dropna(
            how="all"
        )

        # Clean column names
        df.columns = [
            str(column).strip()
            for column in df.columns
        ]

        print(
            "Loaded columns:",
            df.columns.tolist()
        )

        print(
            "Loaded rows:",
            len(df)
        )

        return df

    raise FileNotFoundError(
        "Put your TNEA Excel file inside the data folder "
        "and name it college_cutoffs.xlsx"
    )