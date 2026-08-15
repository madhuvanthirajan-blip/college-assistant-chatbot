import os
from openai import OpenAI

SYSTEM_PROMPT='''You are College Assistant, an AI assistant for students in Tamil Nadu. Answer clearly and briefly about TNEA, engineering colleges, branches, cutoffs, counselling, admissions and career questions. You may also answer general questions because you are the main chatbot. Do not invent exact college cutoffs, fees, ranks, seats or admission guarantees. For exact college recommendations, ask the student to provide cutoff, category, district and preferred branch so the recommendation engine can check the project dataset. Keep answers student-friendly and concise.'''

def ask_llm(prompt,history=None):
    key=os.getenv('NVIDIA_API_KEY','').strip()
    if not key: return fallback_response(prompt)
    try:
        client=OpenAI(base_url=os.getenv('NVIDIA_BASE_URL','https://integrate.api.nvidia.com/v1'),api_key=key)
        messages=[{'role':'system','content':SYSTEM_PROMPT}]
        for m in (history or [])[-10:]:
            if m.get('role') in ('user','assistant') and m.get('content'):
                messages.append({'role':m['role'],'content':m['content']})
        messages.append({'role':'user','content':prompt})
        r=client.chat.completions.create(model=os.getenv('NVIDIA_MODEL','meta/llama-3.1-8b-instruct'),messages=messages,temperature=.3,max_tokens=350)
        return (r.choices[0].message.content or fallback_response(prompt)).strip()
    except Exception as e:
        return f'AI service is currently unavailable. Check your NVIDIA API key and model settings. ({type(e).__name__})'

def fallback_response(prompt):
    t=prompt.lower()
    if 'tnea' in t: return 'TNEA is Tamil Nadu Engineering Admissions, the counselling process used for admission to B.E./B.Tech courses in Tamil Nadu.'
    if 'counselling' in t: return 'TNEA counselling is the college and branch allotment process based on rank, choices, category and available seats.'
    if 'cse' in t and ('ai' in t or 'data science' in t): return 'CSE gives a broad computer-science foundation, while AI & DS focuses more on AI, machine learning and data. Choose based on the subjects and career direction you prefer.'
    if 'branch' in t: return 'Popular branches include CSE, IT, AI & DS, ECE, EEE, Mechanical and Civil. The best branch depends on your interests and career goals.'
    return "I'm your College Assistant. Ask me about TNEA, colleges, cutoffs, branches, counselling or admissions. For personalized recommendations, send your cutoff, category, district and preferred branch."
