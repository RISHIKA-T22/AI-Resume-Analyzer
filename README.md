
# AI Resume Analyzer & Candidate Ranking System

## Overview

The AI Resume Analyzer is a Python-based application designed to simplify resume screening and help evaluate candidates based on their resume information. It uses Natural Language Processing (NLP) techniques and Google Gemini AI to analyze resume content and generate useful insights.

The application provides a simple Streamlit interface through which users can upload a resume and obtain AI-assisted analysis.

## Features

- **Resume Upload:** Upload a resume in PDF format.
- **Text Extraction:** Extract resume content using PyPDF2.
- **AI-Powered Analysis:** Use Google Gemini AI to interpret resume information and generate relevant insights.
- **Candidate Evaluation:** Support resume screening and candidate assessment.
- **Interactive Interface:** Use a Streamlit-based interface to interact with the application.
- **Automated Processing:** Reduce the effort involved in manually reviewing resume content.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| PyPDF2 | Extract text from PDF resumes |
| NLP | Process and analyze textual information |
| Google Gemini AI | AI-powered resume analysis |

## How It Works

1. The user uploads a PDF resume through the application.
2. PyPDF2 extracts the text from the uploaded document.
3. The extracted resume content is prepared for analysis.
4. Google Gemini AI processes the content and generates analysis based on the instructions provided.
5. The application displays the resulting insights through the Streamlit interface.

## Project Structure

```text
AI-Resume-Analyzer/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.9 or a compatible version
- pip
- Google Gemini API key

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/RISHIKA-T22/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure the API key**

Create a `.streamlit/secrets.toml` file and add your Gemini API key:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

Make sure the application reads the key using the same configuration name. Never commit your API key to GitHub.

**4. Run the application**

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the application.

## Future Enhancements

- Support additional resume formats such as DOCX.
- Compare resumes against specific job descriptions.
- Improve candidate ranking using clearly defined evaluation criteria.
- Provide skill-gap identification and personalized improvement suggestions.
- Enable batch processing of multiple resumes.

## Learning Outcomes

Through this project, I gained practical experience in:

- Python application development.
- PDF text extraction and text processing.
- Integrating generative AI into an application.
- Working with API-based AI services.
- Building interactive applications using Streamlit.

## Author

**T Rishika**

GitHub: [RISHIKA-T22](https://github.com/RISHIKA-T22)
