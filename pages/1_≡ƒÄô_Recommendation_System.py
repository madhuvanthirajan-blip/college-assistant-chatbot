import streamlit as st
from recommendation_engine import recommend

st.set_page_config(page_title='College Recommendation System',page_icon='🎓',layout='wide')
st.markdown('''<style>.stApp{background:#F6F3FB}.block-container{max-width:1200px;padding-top:2rem}.title{text-align:center;font-size:38px;font-weight:750;color:#171717}.subtitle{text-align:center;color:#777;font-size:16px;margin-bottom:25px}.profile-card{background:#fff;border:1px solid #E2DAEF;border-radius:14px;padding:16px;min-height:112px}.profile-label{color:#777;font-size:12px;font-weight:700;margin-bottom:10px}.profile-value{color:#4F2FA8;font-size:18px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.result-card{background:#fff;border:1px solid #E2DAEF;border-radius:14px;padding:18px;margin-top:15px}</style>''',unsafe_allow_html=True)
st.markdown('<div class="title">🎓 Find Your Best-Fit College</div>',unsafe_allow_html=True)
st.markdown('<div class="subtitle">Get personalized college recommendations using your TNEA cutoff, category, district and preferred engineering branch.</div>',unsafe_allow_html=True)

c1,c2,c3=st.columns(3)
with c1: name=st.text_input('Name',placeholder='Enter your name')
with c2: district=st.selectbox('District',['Ariyalur','Chengalpattu','Chennai','Coimbatore','Cuddalore','Dharmapuri','Dindigul','Erode','Kanchipuram','Karur','Krishnagiri','Madurai','Namakkal','Salem','Thanjavur','Tiruchirappalli','Tirunelveli','Tiruppur','Tiruvallur','Tiruvannamalai','Vellore','Virudhunagar'])
with c3: category=st.selectbox('Category',['OC','BC','BCM','MBC','SC','SCA','ST'])
cutoff=st.number_input('TNEA Cutoff',min_value=0.0,max_value=200.0,value=150.0,step=.5)
branch=st.selectbox('Preferred Branch',['Computer Science and Engineering','Artificial Intelligence and Data Science','Information Technology','Electronics and Communication Engineering','Electrical and Electronics Engineering','Mechanical Engineering','Civil Engineering','Aeronautical Engineering','Agricultural Engineering','Biotechnology'])
search=st.button('🔎 Find My Colleges',type='primary',use_container_width=True)

if search:
    try: results=recommend(cutoff,category,district,branch,limit=None)
    except Exception as e: st.error(str(e)); results=[]
    st.markdown('<h2>📋 Your Profile Summary</h2>',unsafe_allow_html=True)
    vals=[('👤 NAME',name or 'Student'),('📍 DISTRICT',district),('🏷️ CATEGORY',category),('📊 CUTOFF',f'{cutoff:.1f}'),('💻 BRANCH',branch)]
    cols=st.columns(5)
    for col,(label,value) in zip(cols,vals):
        with col: st.markdown(f'<div class="profile-card"><div class="profile-label">{label}</div><div class="profile-value" title="{value}">{value}</div></div>',unsafe_allow_html=True)
    st.divider()
    if not results: st.warning('No matching colleges were found in the current dataset.')
    else:
        st.success(f'Found {len(results)} college options.')
        st.markdown('<h2>🏆 Top Picks For You</h2>',unsafe_allow_html=True)
        for item in results[:3]: st.markdown(f'<div class="result-card"><div style="color:#5533A8;font-size:12px;font-weight:700">#{item["rank"]} · {item["chance"]}</div><div style="font-size:19px;font-weight:700;margin-top:6px">{item["college_name"]}</div><div style="color:#666;font-size:14px;margin-top:7px;line-height:1.6">📍 {item["district"]}<br>💻 {item["branch"]}<br>📊 Previous cutoff: {item["cutoff"]}</div></div>',unsafe_allow_html=True)
        st.markdown('<h2>🏫 All College Recommendations</h2>',unsafe_allow_html=True)
        table=[{'Rank':x['rank'],'College Name':x['college_name'],'District':x['district'],'Branch':x['branch'],'Previous Cutoff':x['cutoff'],'Chance':x['chance']} for x in results]
        st.dataframe(table,use_container_width=True,hide_index=True)
        st.caption('Recommendations use previous-year cutoff data and are not an admission guarantee.')
