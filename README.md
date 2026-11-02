
# AI Resume Analyzer & Candidate Ranking System

## Overview

AI Resume Analyzer is a Python and Streamlit application for screening multiple PDF resumes against a job description. It extracts text from each resume, matches skills against the job description using a keyword database, detects experience and education, ranks candidates by skill-match percentage, and generates a short HR-style summary for each candidate using Google Gemini.

> **Note:** Scoring and ranking are rule-based (keyword and regex matching). Gemini is used only to write the final text insights; it does not calculate the score.

## Features

- **Batch resume upload:** Upload one or more PDF resumes at once.
- **Job description input:** Paste the job description into a text box.
- **PDF text extraction:** Uses PyMuPDF (`fitz`) to read the text of every page.
- **Skill extraction:** Matches resume and job description text against a built-in list of 28 skills (whole-word, case-insensitive).
- **Match score:** `(matching skills ÷ skills found in the job description) × 100`.
- **Missing skills:** Shows the skills the job description asks for that the resume lacks.
- **Experience detection:** Finds patterns such as "3 years", "5+ yrs" and takes the largest number in the text.
- **Education detection:** Finds degree keywords (B.Tech, B.E, Bachelor, B.Sc, M.Tech, M.E, Master, M.Sc, PhD, Doctorate).
- **Recommendation levels:** Highly Recommended (≥ 80%), Recommended (≥ 60%), Consider for Review (≥ 40%), Not Recommended (< 40%).
- **Dashboard:**
  - Summary metrics: resumes analyzed, average match, highest match, strong matches (≥ 80%).
  - Bar chart of match scores.
  - Side-by-side comparison of up to 5 selected candidates.
  - Ranking table with progress bars.
  - Filter by recommendation level and search by file name.
  - CSV export of the ranking table (exports only the rows currently shown after filtering and search).
  - Expandable detailed report per candidate, with skill chips, experience and education.
- **AI-powered insights (Gemini):** Candidate strengths, areas for improvement and a final hiring recommendation. If the Gemini call fails, a generic fallback message is shown.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web interface |
| PyMuPDF (`fitz`) | PDF text extraction |
| Regex / keyword matching | Skill, experience and education detection |
| pandas | Tables, charts and CSV export |
| Google Gemini (`google-generativeai`, model `gemini-flash-latest`) | AI-generated insights |
| python-dotenv | Loading the API key from `.env` |

## How It Works

1. The user uploads one or more PDF resumes and pastes a job description.
2. On **Analyze Candidates**, skills, required experience and education keywords are extracted from the job description.
3. For each resume, text is extracted with PyMuPDF, then skills, experience and education are detected.
4. Matching and missing skills are computed against the job description, and the match percentage is calculated.
5. Candidates are sorted by match percentage (highest first) and stored in Streamlit session state.
6. The dashboard shows metrics, chart, comparison, ranking table, filters, CSV export and detailed reports.
7. For each candidate's report, the matching skills, missing skills, score, experience and education are sent to Gemini, which returns the strengths, improvements and recommendation text.

## Project Structure

```text
AI-Resume-Analyzer/
├── app.py                        # Streamlit UI, analysis flow, dashboard
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── skills_db.py              # List of recognised skills
└── utils/
    ├── pdf_parser.py             # PDF text extraction (PyMuPDF)
    ├── skill_matcher.py          # Skill detection
    ├── experience_checker.py     # Years-of-experience detection
    ├── education_checker.py      # Degree keyword detection
    └── ai_suggestions.py         # Gemini prompt and fallback text
```

## Recognised Skills

python, java, c++, sql, mysql, postgresql, mongodb, html, css, javascript, react, nodejs, django, flask, machine learning, deep learning, tensorflow, pytorch, data analysis, aws, azure, docker, kubernetes, git, github, power bi, tableau, excel

Skills outside this list are not detected. Add new ones in `data/skills_db.py`.

## Getting Started

### Prerequisites

- Python 3.9 or later (carried over from the original README; not enforced anywhere in the code)
- pip
- A Google Gemini API key

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/RISHIKA-T22/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
pip install google-generativeai
```

> `google-generativeai` is imported by `utils/ai_suggestions.py` but is missing from `requirements.txt`. Add it to that file (see "Known Issues").

**3. Configure the API key**

Create a `.env` file in the project root.


The app reads the key with `python-dotenv`. It does **not** use `.streamlit/secrets.toml`. `.env` is already listed in `.gitignore`; never commit your key.

**4. Run the application**

```bash
streamlit run app.py
```

Open the local URL shown in the terminal.

## Known Limitations

- Skills are matched from a fixed list of 28 keywords; there is no semantic or NLP understanding.
- The score is based on skills only. Experience and education are detected and displayed but do not affect the score or ranking.
- Experience detection takes the largest "N years" figure found anywhere in the text, which may include unrelated numbers.
- Education matching is simple substring matching, so `master` also matches words like "mastery" or "mastered", and short keywords like `b.e` or `m.e` can match unrelated text.
- Gemini receives only the extracted summary (skills, score, experience, education), not the full resume text.
- Gemini is called again for every candidate each time the page reruns (for example when a filter changes), because results are not cached.
- If the job description contains no recognised skills, every candidate scores 0%.
- The app was reviewed by reading the code, not by running it.
- If `GEMINI_API_KEY` is missing, the Gemini call fails and the generic fallback text is shown for every candidate.
- Only PDF files are supported. Scanned (image-only) PDFs will return no text.

## Future Enhancements

- Support DOCX resumes.
- Include experience and education in the ranking score.
- Use NLP or embeddings for semantic skill matching.
- Expand the skills database.
- Cache Gemini responses to avoid repeated API calls.

## Learning Outcomes

- Building a multi-file Python application with Streamlit.
- PDF text extraction and rule-based text processing.
- Integrating a generative AI API (Gemini).
- Data presentation with pandas, charts and CSV export.

## Author

**T Rishika**

GitHub: [RISHIKA-T22](https://github.com/RISHIKA-T22)
