import math
import pandas as pd
from data_loader import load_college_data
CATEGORY_COLUMNS=['OC','BC','BCM','MBC','SC','SCA','ST']

def clean(v): return '' if pd.isna(v) else str(v).strip()
def norm_branch(v):
    t=clean(v).lower()
    m={'computer science & engineering':'computer science and engineering','computer science engineering':'computer science and engineering','ai & ds':'artificial intelligence and data science','ai and ds':'artificial intelligence and data science','aeronautical':'aeronautical engineering','agricultural':'agricultural engineering','cse':'computer science and engineering','ece':'electronics and communication engineering','eee':'electrical and electronics engineering','it':'information technology'}
    return m.get(t,t)

def find_col(df,names):
    mp={str(c).strip().lower():c for c in df.columns}
    for n in names:
        if n.lower() in mp:return mp[n.lower()]
    return None

def prepare(df):
    df=df.copy(); df.columns=[str(c).strip() for c in df.columns]
    cc=find_col(df,['college_name','college name','college','name']); dc=find_col(df,['district','college district']); bc=find_col(df,['branch','branch name','course','program'])
    if not cc or not bc: raise ValueError('Dataset needs college_name and branch columns.')
    rename={cc:'college_name',bc:'branch'}
    if dc: rename[dc]='district'
    df=df.rename(columns=rename)
    if 'district' not in df.columns: df['district']='Not specified'
    for cat in CATEGORY_COLUMNS:
        c=find_col(df,[cat])
        if c and c!=cat: df=df.rename(columns={c:cat})
    for c in ['college_name','district','branch']: df[c]=df[c].apply(clean)
    return df

def chance(student,previous):
    if previous is None or math.isnan(previous): return 'Data unavailable'
    gap=student-previous
    if gap>=0:return 'Very High'
    if gap>=-5:return 'High'
    if gap>=-10:return 'Moderate'
    return 'Low'

def recommend(cutoff,category,district,branch,limit=None):
    df=prepare(load_college_data()); category=str(category).upper().strip(); district=str(district).lower().strip(); requested=norm_branch(branch)
    if category not in CATEGORY_COLUMNS: raise ValueError(f'Unsupported category: {category}')
    b=df['branch'].map(norm_branch)
    mask=(b==requested)
    if not mask.any(): mask=b.apply(lambda x: requested in x or x in requested)
    filtered=df[mask].copy()
    if district:
        dm=filtered['district'].str.lower().str.contains(district,na=False,regex=False)
        if dm.any(): filtered=filtered[dm]
    if filtered.empty:return []
    filtered['_previous_cutoff']=pd.to_numeric(filtered[category],errors='coerce'); filtered=filtered.dropna(subset=['_previous_cutoff'])
    if filtered.empty:return []
    filtered['_gap']=cutoff-filtered['_previous_cutoff']; filtered=filtered.sort_values(['_gap','_previous_cutoff'],ascending=[False,False])
    if limit is not None: filtered=filtered.head(limit)
    out=[]
    for i,(_,row) in enumerate(filtered.iterrows(),1):
        prev=float(row['_previous_cutoff'])
        out.append({'rank':i,'college_name':clean(row['college_name']),'district':clean(row['district']),'branch':clean(row['branch']),'cutoff':prev,'chance':chance(float(cutoff),prev)})
    return out

def recommend_from_text(details):
    return recommend(float(details['cutoff']),details['category'],details['district'],details['branch'],limit=None)
