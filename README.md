# College Assistant Chatbot

A new Streamlit project for a ChatGPT-style college assistant with a separate TNEA recommendation page.

## Features
- Main chatbot page
- Quick questions above the chat input
- Conversation history
- NVIDIA/OpenAI-compatible LLM integration
- Natural-language extraction of cutoff/category/district/branch
- College recommendation cards
- Separate recommendation-system page
- All matching recommendation rows shown once in a clean table

## Setup

### 1. Create environment
Windows:
```bash
python -m venv venv
venv\\Scripts\\activate
```

### 2. Install
```bash
pip install -r requirements.txt
```

### 3. NVIDIA key
Copy `.env.example` to `.env` and set `NVIDIA_API_KEY`.

The default base URL is `https://integrate.api.nvidia.com/v1` and the code uses the OpenAI-compatible `/v1/chat/completions` endpoint. Change `NVIDIA_MODEL` if your account uses a different available model.

### 4. Run
```bash
streamlit run app.py
```

## Dataset

The included CSV is only sample data so the project can run immediately. Replace it with your real cleaned TNEA data.

Expected columns:
```text
college_name,district,branch,OC,BC,BCM,MBC,SC,SCA,ST
```

You may instead place `college_cutoffs.xlsx` in `data/`.

Each category column should contain the previous-year cutoff for that college and branch.

## Example chatbot message
```text
My cutoff is 180, OC category, Chennai district and CSE.
```

The chatbot extracts the four details, runs the recommendation engine, and displays matching college details in cards.

Historical cutoffs are references only and do not guarantee admission.

Never commit `.env` or an API key to GitHub.
