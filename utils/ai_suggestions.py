import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-flash-latest")


def get_ai_suggestions(
    matching_skills,
    missing_skills,
    match_percentage,
    experience,
    education
):

    prompt = f"""
    You are an expert HR recruiter.

    Resume Analysis:

    Matching Skills:
    {matching_skills}

    Missing Skills:
    {missing_skills}

    Match Percentage:
    {match_percentage}%

    Experience:
    {experience} years

    Education:
    {education}

    Give:

    1. Candidate Strengths
    2. Areas for Improvement
    3. Final Hiring Recommendation

    Keep response professional and concise.
    """

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception:
        return """
Candidate Strengths:
- Relevant skills match the job description.

Areas for Improvement:
- Improve missing technical skills.
- Gain more practical experience.

Final Hiring Recommendation:
- Consider for further evaluation.
"""