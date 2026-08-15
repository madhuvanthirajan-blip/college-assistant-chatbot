from pathlib import Path
import pandas as pd
BASE_DIR=Path(__file__).resolve().parent
DATA_DIR=BASE_DIR/'data'

def load_college_data():
    csv=DATA_DIR/'college_cutoffs.csv'; xlsx=DATA_DIR/'college_cutoffs.xlsx'
    if csv.exists(): return pd.read_csv(csv)
    if xlsx.exists(): return pd.read_excel(xlsx)
    raise FileNotFoundError('Put college_cutoffs.csv or college_cutoffs.xlsx inside the data folder.')
