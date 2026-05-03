# AI Degree Advisor

AI Degree Advisor is a Flask web application that recommends degree paths based on a student profile and explains why a path was selected.

The project combines:

- rule-based eligibility checks
- weighted scoring
- A* style ranking across degree states
- mapped career outcomes
- optional Groq-powered follow-up guidance in chat

## What this project does

The app collects student inputs such as marks, interests, skills, work preference, math level, and career goal. It then:

1. ranks available degree options from `data/degree_rules.csv`
2. computes a best match and a score
3. maps that degree to careers from `data/career_map.csv`
4. stores recommendation history in `data/session_history.json`
5. allows Q&A on the result using Groq API

## Key features

- Student profile form with structured inputs
- Transparent recommendation output with best degree, match score, ranked alternatives, missing-cost signal, and rule trace (`rules_used`)
- Career suggestions linked to the selected degree
- Session history page for previous recommendations
- Chat assistant for next-step guidance after recommendation

## Tech stack

- Python
- Flask
- Pandas
- OpenAI Python SDK (used with Groq OpenAI-compatible endpoint)
- HTML/CSS/JavaScript (Jinja templates)

## Project structure

```text
.
├── app.py
├── requirements.txt
├── data/
│   ├── career_map.csv
│   ├── degree_rules.csv
│   └── session_history.json
├── recommender/
│   ├── groq_chat.py
│   ├── rule_engine.py
│   └── scorer.py
├── static/
│   ├── chat.js
│   └── style.css
└── templates/
    ├── base.html
    ├── history.html
    ├── index.html
    └── result.html
```

## Recommendation flow

1. `app.py` receives form data at `/recommend`.
2. `RecommendationEngine` loads rule and career datasets.
3. `rank_with_astar` scores and ranks each degree state.
4. Highest-ranked degree is selected as `best`.
5. Matching careers are attached to the response.
6. Rule explanation is generated and displayed.
7. Result and profile are stored in session and history.

## Scoring overview

The score combines multiple signals:

- marks vs required minimum
- overlap in interests
- overlap in skills
- preferred work alignment
- math level alignment
- career-goal keyword alignment

A missing-cost penalty is applied for profile mismatches (e.g., below required marks, work/maths mismatch). Final displayed score is bounded to 0-100.

## Setup

### 1. Clone repository

```bash
git clone https://github.com/HamzaaAkmal/AI_Degree_Advisor.git
cd AI_Degree_Advisor
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
FLASK_SECRET_KEY=your_secret_key_here
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

Notes:

- `GROQ_API_KEY` is required for chat.
- Recommendation flow works without Groq, but chat replies will show a key-missing message.

### 5. Run the app

```bash
python app.py
```

Open browser at:

```text
http://127.0.0.1:5000
```

## Routes

- `/` - student input form
- `/recommend` - recommendation result (POST)
- `/chat` - chat API for follow-up questions (POST)
- `/history` - previous recommendation sessions

## Data files

- `data/degree_rules.csv`: degree constraints and keywords used by ranking logic
- `data/career_map.csv`: degree-to-career mapping
- `data/session_history.json`: rolling recommendation history (latest 25 records)

## Notes for development

- The app currently runs in debug mode through `app.py`.
- `recommender/__pycache__/` files can be ignored in future commits with `.gitignore`.
- Rule and scoring behavior can be tuned in `recommender/scorer.py` and `recommender/rule_engine.py`.

