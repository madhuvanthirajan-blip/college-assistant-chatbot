import os
import re
from pathlib import Path
from typing import Optional, Tuple, List, Dict

import pandas as pd

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


# ============================================================
# DATA LOADING
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_CANDIDATES = [
    BASE_DIR / "data" / "tnea_cutoff_data.csv",
    BASE_DIR / "data" / "college_cutoffs.csv",
    BASE_DIR / "data" / "cutoff_data.csv",
    BASE_DIR / "tnea_cutoff_data.csv",
    BASE_DIR / "college_cutoffs.csv",
    BASE_DIR / "cutoff_data.csv",
]


def _find_data_file() -> Optional[Path]:
    for path in DATA_CANDIDATES:
        if path.exists():
            return path

    # Last-resort search: only CSV files inside the project.
    for path in BASE_DIR.rglob("*.csv"):
        if path.name.lower() not in {"requirements.csv"}:
            return path
    return None


def _clean_name(value) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def _norm(value) -> str:
    value = _clean_name(value).lower()
    value = value.replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def _find_col(df: pd.DataFrame, aliases: List[str]) -> Optional[str]:
    normalized = {_norm(c): c for c in df.columns}
    for alias in aliases:
        if _norm(alias) in normalized:
            return normalized[_norm(alias)]
    for c in df.columns:
        nc = _norm(c)
        for alias in aliases:
            na = _norm(alias)
            if na and (na in nc or nc in na):
                return c
    return None


def load_data() -> pd.DataFrame:
    path = _find_data_file()
    if path is None:
        return pd.DataFrame()

    df = pd.read_csv(path)
    df.columns = [_clean_name(c) for c in df.columns]
    return df


# ============================================================
# BRANCH / CATEGORY HELPERS
# ============================================================

BRANCH_ALIASES = {
    "cse": [
        "computer science and engineering",
        "computer science & engineering",
        "computer science engineering",
        "cse",
    ],
    "it": ["information technology", "it"],
    "ai ds": [
        "artificial intelligence and data science",
        "artificial intelligence & data science",
        "ai and data science",
        "ai&ds",
        "ai ds",
    ],
    "ai ml": [
        "artificial intelligence and machine learning",
        "computer science and engineering (ai and machine learning)",
        "ai and machine learning",
        "ai ml",
    ],
    "ece": ["electronics and communication engineering", "ece"],
    "eee": ["electrical and electronics engineering", "eee"],
    "mechanical": ["mechanical engineering", "mechanical"],
    "civil": ["civil engineering", "civil"],
    "aeronautical": ["aeronautical engineering", "aeronautical"],
    "aerospace": ["aerospace engineering", "aerospace"],
    "biotech": ["biotechnology", "bio technology", "biotech"],
    "chemical": ["chemical engineering", "chemical"],
}

CATEGORIES = ["OC", "BC", "BCM", "MBC", "SC", "SCA", "ST"]


def normalize_branch(value: str) -> str:
    text = _norm(value)
    for canonical, aliases in BRANCH_ALIASES.items():
        if text == _norm(canonical):
            return canonical
        if any(_norm(a) == text for a in aliases):
            return canonical
    return text


def branch_matches(value: str, requested: str) -> bool:
    row = _norm(value)
    req = normalize_branch(requested)
    aliases = BRANCH_ALIASES.get(req, [requested])
    return any(_norm(alias) == row or _norm(alias) in row or row in _norm(alias) for alias in aliases)


def _category_cutoff_column(df: pd.DataFrame, category: str) -> Optional[str]:
    aliases = [category, f"{category} cutoff", f"cutoff {category}", f"{category}_cutoff"]
    return _find_col(df, aliases)


def _long_format_columns(df: pd.DataFrame):
    category_col = _find_col(df, ["category", "community", "caste", "quota"])
    cutoff_col = _find_col(df, ["cutoff", "previous cutoff", "cutoff mark", "closing cutoff"])
    return category_col, cutoff_col


# ============================================================
# RECOMMENDATION ENGINE
# IMPORTANT: THERE IS NO TOP-3 LIMIT HERE.
# ============================================================

def get_recommendations(
    cutoff: float,
    category: str,
    district: str,
    branch: str,
) -> List[Dict]:
    df = load_data()
    if df.empty:
        return []

    category = category.upper().replace("-", "").replace(" ", "")
    if category not in CATEGORIES:
        category = "OC"

    district_col = _find_col(df, ["district", "district name"])
    branch_col = _find_col(df, ["branch", "course", "branch name", "programme", "program"])
    college_col = _find_col(df, ["college name", "college", "institution name", "institution"])

    if not college_col or not branch_col:
        return []

    work = df.copy()
    work["__college"] = work[college_col].map(_clean_name)
    work["__branch"] = work[branch_col].map(_clean_name)

    # --------------------------------------------------------
    # District filtering
    # --------------------------------------------------------
    if district_col and district and district.strip():
        requested_district = _norm(district)
        district_values = work[district_col].map(_norm)

        # Exact district first. If the dataset uses an address instead of a
        # district column, allow the district text to occur in the address.
        exact = district_values == requested_district
        contains = district_values.str.contains(re.escape(requested_district), na=False)
        district_mask = exact | contains

        if district_mask.any():
            work = work[district_mask].copy()

    # --------------------------------------------------------
    # Branch filtering
    # --------------------------------------------------------
    branch_mask = work["__branch"].map(lambda x: branch_matches(x, branch))
    work = work[branch_mask].copy()

    if work.empty:
        return []

    # --------------------------------------------------------
    # Category-specific cutoff
    # Supports both wide data (OC/BC/...) and long data
    # (Category + Cutoff columns).
    # --------------------------------------------------------
    category_col, long_cutoff_col = _long_format_columns(work)
    category_cutoff_col = _category_cutoff_column(work, category)

    if category_cutoff_col:
        work["__cutoff"] = pd.to_numeric(
            work[category_cutoff_col].astype(str).str.replace("*", "", regex=False),
            errors="coerce",
        )
    elif category_col and long_cutoff_col:
        work["__category"] = work[category_col].map(_norm)
        requested_category = _norm(category)
        cat_mask = work["__category"].eq(requested_category)
        # Some datasets spell BCM/MBC etc. differently; exact normalized match
        # is preferred, with a fallback to all rows if no category rows exist.
        if cat_mask.any():
            work = work[cat_mask].copy()
        work["__cutoff"] = pd.to_numeric(
            work[long_cutoff_col].astype(str).str.replace("*", "", regex=False),
            errors="coerce",
        )
    else:
        # Fallback for a dataset that has only one cutoff column.
        generic_cutoff = _find_col(
            work,
            ["previous cutoff", "cutoff", "cutoff mark", "closing cutoff", "previous_cutoff"],
        )
        if not generic_cutoff:
            return []
        work["__cutoff"] = pd.to_numeric(
            work[generic_cutoff].astype(str).str.replace("*", "", regex=False),
            errors="coerce",
        )

    work = work.dropna(subset=["__cutoff"]).copy()
    if work.empty:
        return []

    # --------------------------------------------------------
    # DO NOT filter with cutoff <= student cutoff.
    # We need all matching colleges, including higher-cutoff colleges,
    # so the user can see Very High / High / Moderate / Low chances.
    # --------------------------------------------------------
    work["__difference"] = cutoff - work["__cutoff"]

    def chance(diff: float) -> str:
        if diff >= 5:
            return "Very High"
        if diff >= 0:
            return "High"
        if diff >= -10:
            return "Moderate"
        return "Low"

    work["__chance"] = work["__difference"].map(chance)

    # Best chance first, then closest cutoff to the student's cutoff.
    chance_order = {"Very High": 0, "High": 1, "Moderate": 2, "Low": 3}
    work["__chance_order"] = work["__chance"].map(chance_order)
    work = work.sort_values(
        ["__chance_order", "__cutoff", "__college"],
        ascending=[True, True, True],
    )

    # Remove duplicate college + branch rows while preserving the best match.
    work = work.drop_duplicates(subset=["__college", "__branch"], keep="first")

    profile = {
        "cutoff": cutoff,
        "category": category,
        "district": district,
        "branch": branch,
    }

    results: List[Dict] = []
    for rank, (_, row) in enumerate(work.iterrows(), start=1):
        results.append(
            {
                "rank": rank,
                "college_name": row["__college"],
                "district": _clean_name(row[district_col]) if district_col else district,
                "branch": row["__branch"],
                "cutoff": float(row["__cutoff"]),
                "chance": row["__chance"],
                "cutoff_difference": round(float(row["__difference"]), 2),
                "_profile": profile if rank == 1 else None,
            }
        )

    return results


# ============================================================
# CHATBOT
# ============================================================

KNOWLEDGE = {
    "tnea": "TNEA (Tamil Nadu Engineering Admissions) is the admission process used for B.E./B.Tech admissions in Tamil Nadu. Students are allotted colleges and branches based on eligibility, rank, choices, reservation and seat availability.",
    "counselling": "TNEA counselling is the process through which eligible students enter their choices and receive college/branch allotments based on rank, reservation, choices and available seats.",
    "cutoff": "A TNEA cutoff is a historical admission mark for a particular college, branch and category. A previous-year cutoff is only an estimate and does not guarantee admission.",
    "branches": "Popular engineering branches include CSE, IT, AI & DS, AI & ML, ECE, EEE, Mechanical, Civil, Aeronautical, Aerospace, Biotechnology and Chemical Engineering.",
    "documents": "Common counselling documents can include marksheets, community certificate where applicable, transfer certificate, nativity-related documents where applicable, ID proof and photographs. Always verify the current TNEA requirements before counselling.",
}


def _extract_details(text: str) -> Dict:
    lower = text.lower()
    details: Dict = {}

    cutoff_match = re.search(r"(?:cutoff|cut off|mark|score)?\s*(?:is|:|=)?\s*(\d{2,3}(?:\.\d+)?)", lower)
    if cutoff_match:
        try:
            details["cutoff"] = float(cutoff_match.group(1))
        except ValueError:
            pass

    for category in CATEGORIES:
        patterns = [
            rf"\b{re.escape(category.lower())}\b",
            rf"\b{re.escape(category.lower().replace('c', 'c-'))}\b",
        ]
        if any(re.search(p, lower) for p in patterns):
            details["category"] = category
            break

    districts = [
        "chennai", "coimbatore", "madurai", "tiruchirappalli", "trichy",
        "salem", "tirunelveli", "vellore", "kanchipuram", "erode",
        "thanjavur", "tiruvallur", "chengalpattu", "kancheepuram",
    ]
    for district in districts:
        if district in lower:
            details["district"] = "Chennai" if district == "chennai" else district.title()
            break

    branch_patterns = [
        ("ai ds", "Artificial Intelligence and Data Science"),
        ("ai&ds", "Artificial Intelligence and Data Science"),
        ("artificial intelligence and data science", "Artificial Intelligence and Data Science"),
        ("ai ml", "Artificial Intelligence and Machine Learning"),
        ("artificial intelligence and machine learning", "Artificial Intelligence and Machine Learning"),
        ("computer science", "Computer Science and Engineering"),
        ("cse", "Computer Science and Engineering"),
        ("information technology", "Information Technology"),
        ("\bit\b", "Information Technology"),
        ("electronics and communication", "Electronics and Communication Engineering"),
        ("\bece\b", "Electronics and Communication Engineering"),
        ("electrical and electronics", "Electrical and Electronics Engineering"),
        ("\beee\b", "Electrical and Electronics Engineering"),
        ("mechanical", "Mechanical Engineering"),
        ("civil", "Civil Engineering"),
        ("aeronautical", "Aeronautical Engineering"),
        ("aerospace", "Aerospace Engineering"),
        ("biotechnology", "Biotechnology"),
        ("biotech", "Biotechnology"),
    ]
    for pattern, branch in branch_patterns:
        if re.search(pattern, lower):
            details["branch"] = branch
            break

    return details


def _recommendation_requested(text: str, details: Dict) -> bool:
    lower = text.lower()
    recommendation_words = [
        "what colleges", "which colleges", "colleges can i get", "college can i get",
        "recommend", "recommendation", "eligible colleges", "matching colleges",
        "my cutoff", "my cut off", "find colleges", "suggest colleges",
    ]
    return any(word in lower for word in recommendation_words) or (
        "cutoff" in lower and bool(details.get("branch"))
    )


def _knowledge_reply(text: str) -> str:
    lower = text.lower()

    if "cse" in lower and ("ai" in lower or "data science" in lower):
        return (
            "CSE and AI & DS are both strong choices. CSE is broader and covers software, "
            "systems and core computer science, while AI & DS focuses more on data, machine "
            "learning and AI. Choose based on your interests and the college/branch combination available to you."
        )

    if "best branch" in lower or "which branch" in lower:
        return (
            "There is no single best engineering branch for everyone. CSE, IT and AI & DS are "
            "popular for software/AI careers, while ECE, EEE, Mechanical, Civil and other branches "
            "are better suited to different interests and career paths."
        )

    for key, value in KNOWLEDGE.items():
        if key in lower:
            return value

    return (
        "I can help with TNEA, colleges, cutoffs, engineering branches and counselling. "
        "For college recommendations, include your cutoff, category, district and preferred branch."
    )


def _try_nvidia_response(text: str, history: List[Dict], recommendations: List[Dict]) -> Optional[str]:
    """Use NVIDIA only when an API key is configured. Never invent recommendation data."""
    api_key = os.getenv("NVIDIA_API_KEY") or os.getenv("NIM_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI
    except Exception:
        return None

    model = os.getenv("NVIDIA_MODEL", "openai/gpt-oss-20b")

    try:
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key,
        )

        context = ""
        if recommendations:
            context = "\n\nAVAILABLE COLLEGE DATA:\n" + "\n".join(
                f"{r['rank']}. {r['college_name']} | {r['branch']} | {r['cutoff']} | {r['chance']}"
                for r in recommendations
            )

        system = (
            "You are a helpful TNEA college assistant. Answer the student's question clearly. "
            "For recommendation facts, use ONLY the supplied college data. Do not invent colleges, "
            "cutoffs, branches or admission chances. Previous-year cutoffs are historical and do not guarantee admission."
            + context
        )

        messages = [{"role": "system", "content": system}]
        for item in history[-8:]:
            role = item.get("role")
            content = item.get("content", "")
            if role in {"user", "assistant"} and content:
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": text})

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
            max_tokens=700,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        print("NVIDIA CHATBOT ERROR:", repr(exc))
        return None


def answer_question(user_input: str, history=None) -> Tuple[str, List[Dict]]:
    history = history or []
    text = user_input.strip()
    details = _extract_details(text)

    recommendations: List[Dict] = []

    if _recommendation_requested(text, details):
        missing = [
            name for name in ("cutoff", "category", "district", "branch")
            if name not in details
        ]

        if not missing:
            recommendations = get_recommendations(
                cutoff=details["cutoff"],
                category=details["category"],
                district=details["district"],
                branch=details["branch"],
            )

            if recommendations:
                reply = (
                    f"I found {len(recommendations)} college(s) matching your requirements "
                    f"for {details['branch']} in {details['district']} under the {details['category']} category. "
                    "The table below contains all matching colleges from the dataset, not just the top three."
                )
            else:
                reply = (
                    "I couldn't find matching colleges in the current dataset for all four requirements. "
                    "Try another branch, district or category."
                )

            # Let NVIDIA improve the wording when available, but keep the exact
            # recommendation list untouched.
            ai_reply = _try_nvidia_response(text, history, recommendations)
            if ai_reply:
                reply = ai_reply

            return reply, recommendations

        # If the user asked for recommendations but did not provide all details,
        # explain exactly what is missing instead of silently returning top colleges.
        pretty = ", ".join(missing)
        return (
            f"I can find all matching colleges for you. Please provide your {pretty}. "
            "Example: My cutoff is 189, I am OC, from Chennai and I want CSE."
        ), []

    ai_reply = _try_nvidia_response(text, history, [])
    return ai_reply or _knowledge_reply(text), []
