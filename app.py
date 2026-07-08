import streamlit as st
from utils.pdf_parser import extract_text_from_pdf
from utils.skill_matcher import extract_skills
from utils.experience_checker import extract_experience
from utils.education_checker import extract_education
from utils.ai_suggestions import get_ai_suggestions

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload multiple resumes and compare them with a job description.")

# --------------------------------------------------
# Upload Multiple Resumes
# --------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload Resume(s) (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

# --------------------------------------------------
# Job Description
# --------------------------------------------------

st.subheader("Job Description")

job_description = st.text_area(
    "Enter Job Description",
    height=250
)

# --------------------------------------------------
# Analyze Button
# --------------------------------------------------

analyze = st.button("Analyze Resumes")

if analyze:

    if not uploaded_files:
        st.error("Please upload at least one resume.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:

        jd_skills = extract_skills(job_description)
        required_experience = extract_experience(job_description)
        required_education = extract_education(job_description)

        results = []

        # ==========================================
        # Analyze Every Resume
        # ==========================================

        for uploaded_file in uploaded_files:

            resume_text = extract_text_from_pdf(uploaded_file)

            resume_skills = extract_skills(resume_text)
            resume_experience = extract_experience(resume_text)
            resume_education = extract_education(resume_text)

            matching_skills = list(
                set(resume_skills).intersection(set(jd_skills))
            )

            missing_skills = list(
                set(jd_skills).difference(set(resume_skills))
            )

            # Match Percentage

            if len(jd_skills) > 0:
                match_percentage = round(
                    (len(matching_skills) / len(jd_skills)) * 100,
                    2
                )
            else:
                match_percentage = 0

            results.append({
                "file_name": uploaded_file.name,
                "match_percentage": match_percentage,
                "matching_skills": matching_skills,
                "missing_skills": missing_skills,
                "experience": resume_experience,
                "education": resume_education
            })

        # ==========================================
        # Sort By Match %
        # ==========================================

        results = sorted(
            results,
            key=lambda x: x["match_percentage"],
            reverse=True
        )

        st.success("Analysis Completed")

        # ==========================================
        # Detailed Resume Analysis
        # ==========================================

        st.header("🏆 Resume Ranking")

        for rank, result in enumerate(results, start=1):

            st.markdown("---")

            st.subheader(
                f"#{rank} - {result['file_name']}"
            )

            st.metric(
                "Match Percentage",
                f"{result['match_percentage']}%"
            )

            # Matching Skills

            st.write("### ✅ Matching Skills")

            if result["matching_skills"]:
                for skill in result["matching_skills"]:
                    st.write(f"• {skill}")
            else:
                st.write("No matching skills found")

            # Missing Skills

            st.write("### ❌ Missing Skills")

            if result["missing_skills"]:
                for skill in result["missing_skills"]:
                    st.write(f"• {skill}")
            else:
                st.write("No missing skills")

            # Experience

            st.write("### 💼 Experience")

            st.write(
                f"Candidate Experience: {result['experience']} Years"
            )

            st.write(
                f"Required Experience: {required_experience} Years"
            )

            # Education

            st.write("### 🎓 Education")

            if result["education"]:
                st.write(result["education"])
            else:
                st.write("Not Detected")

            # AI Recommendation

            st.write("### 🤖 AI Recommendation")

            ai_response = get_ai_suggestions(
                result["matching_skills"],
                result["missing_skills"],
                result["match_percentage"],
                result["experience"],
                result["education"]
            )

            st.write(ai_response)

            # Final Recommendation

            st.write("### 📌 Final Recommendation")

            score = result["match_percentage"]

            if score >= 80:
                st.success("Highly Recommended")

            elif score >= 60:
                st.info("Recommended")

            elif score >= 40:
                st.warning("Consider for Review")

            else:
                st.error("Not Recommended")

        # ==========================================
        # Final Ranking Table
        # ==========================================

        st.markdown("---")
        st.header("🏆 Final Candidate Ranking")

        ranking_data = []

        for rank, result in enumerate(results, start=1):

            score = result["match_percentage"]

            if score >= 80:
                recommendation = "Highly Recommended"
            elif score >= 60:
                recommendation = "Recommended"
            elif score >= 40:
                recommendation = "Consider for Review"
            else:
                recommendation = "Not Recommended"

            ranking_data.append({
                "Rank": rank,
                "Candidate": result["file_name"],
                "Match %": score,
                "Experience": f"{result['experience']} Years",
                "Recommendation": recommendation
            })

        st.table(ranking_data)