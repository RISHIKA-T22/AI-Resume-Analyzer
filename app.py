import streamlit as st
import pandas as pd
import io
import html

from utils.pdf_parser import extract_text_from_pdf
from utils.skill_matcher import extract_skills
from utils.experience_checker import extract_experience
from utils.education_checker import extract_education
from utils.ai_suggestions import get_ai_suggestions

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Resume Intelligence | AI Analyzer",
    page_icon="📄",
    layout="wide"
)

# --------------------------------------------------
# PREMIUM UI
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    font-family: 'Inter', sans-serif;
    background: #f5f7ff;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.4rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: #eef0ff;
}

h1, h2, h3 {
    color: #25245e;
    font-weight: 750 !important;
    letter-spacing: -0.5px;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e1e5ff;
    border-radius: 15px;
    padding: 16px;
    box-shadow: 0 4px 14px #28286b0a;
}

[data-testid="stMetricValue"] {
    color: #5145cd;
    font-weight: 800;
}

[data-testid="stFileUploader"] {
    background: white;
    border: 1px dashed #8b83ed;
    border-radius: 15px;
    padding: 12px;
}

[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input {
    border-radius: 10px;
    background: white;
    border: 1px solid #d9ddf8;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 10px;
    font-weight: 700;
    border: 0;
    transition: 0.2s ease;
}

.stButton > button {
    background: linear-gradient(100deg, #5145cd, #7b42d8);
    color: white;
}

.stButton > button:hover {
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 5px 14px #5145cd30;
}

.stDownloadButton > button {
    background: #e9e7ff;
    color: #3730a3;
}

[data-testid="stExpander"] {
    background: white;
    border: 1px solid #e2e5fa;
    border-radius: 12px;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: #e0e4fb;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #e0e4fb;
    border-radius: 12px;
}

footer, #MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div style="
    background:linear-gradient(115deg,#24215e,#5145cd,#8147dc);
    padding:30px;
    border-radius:20px;
    margin-bottom:22px;
    box-shadow:0 12px 28px #39318b25;
">
    <div style="
        font-size:11px;
        font-weight:700;
        letter-spacing:2px;
        color:#d5d1ff;
    ">AI-POWERED RECRUITMENT PLATFORM</div>
    <div style="
        color:white;
        font-size:32px;
        font-weight:800;
        margin:8px 0;
    ">Resume Intelligence</div>
    <div style="
        color:#e7e5ff;
        font-size:14px;
    ">
        Screen resumes. Discover skill gaps. Compare candidates.
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# INPUT WORKSPACE
# --------------------------------------------------

left, right = st.columns([0.92, 1.08], gap="medium")

with left:
    with st.container(border=True):
        st.markdown("### 📂 Candidate Resumes")
        st.caption("STEP 01  /  Upload candidate profiles")

        uploaded_files = st.file_uploader(
            "Choose PDF resumes",
            type=["pdf"],
            accept_multiple_files=True,
            help="Upload multiple resumes for batch screening."
        )

        if uploaded_files:
            st.markdown(
                f"""
                <div style="
                    padding:11px 13px;
                    background:#eefbf4;
                    border:1px solid #c9f0d9;
                    border-radius:10px;
                    color:#18794e;
                    font-size:13px;
                    font-weight:600;
                ">
                    ✓ {len(uploaded_files)} candidate file(s) ready
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.caption("PDF format · Multiple files supported")

with right:
    with st.container(border=True):
        st.markdown("### 🎯 Job Requirements")
        st.caption("STEP 02  /  Define your hiring criteria")

        job_description = st.text_area(
            "Job Description",
            height=190,
            placeholder=(
                "Describe the role, required skills, education "
                "and experience..."
            ),
            label_visibility="collapsed"
        )

        st.caption("Tip: Include technical skills and required experience.")

st.markdown("")

_, action_col, _ = st.columns([1, 2, 1])

with action_col:
    analyze = st.button(
        "✦  Analyze Candidates",
        use_container_width=True
    )

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

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

        progress = st.progress(0, text="Preparing candidate analysis...")

        for index, uploaded_file in enumerate(uploaded_files):

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

            if len(jd_skills) > 0:
                match_percentage = round(
                    len(matching_skills) / len(jd_skills) * 100,
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

            progress.progress(
                (index + 1) / len(uploaded_files),
                text=f"Analyzing resume {index + 1} of {len(uploaded_files)}..."
            )

        progress.empty()

        results = sorted(
            results,
            key=lambda x: x["match_percentage"],
            reverse=True
        )

        st.session_state["resume_results"] = results
        st.session_state["jd_skills"] = jd_skills
        st.session_state["required_experience"] = required_experience
        st.session_state["required_education"] = required_education

# --------------------------------------------------
# RESULTS DASHBOARD
# --------------------------------------------------

if "resume_results" in st.session_state:

    results = st.session_state["resume_results"]
    jd_skills = st.session_state["jd_skills"]
    required_experience = st.session_state["required_experience"]
    required_education = st.session_state["required_education"]

    st.markdown("---")
    st.markdown("## 📊 Recruitment Overview")
    st.caption("A quick overview of the current analysis.")

    total = len(results)
    average_score = round(
        sum(r["match_percentage"] for r in results) / total, 2
    )
    top_score = results[0]["match_percentage"] if results else 0
    strong_matches = sum(
        1 for r in results if r["match_percentage"] >= 80
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📄 Resumes Analyzed", total)
    c2.metric("🎯 Average Match", f"{average_score}%")
    c3.metric("🏆 Highest Match", f"{top_score}%")
    c4.metric("⭐ Strong Matches", strong_matches)

    # --------------------------------------------------
    # SCORE CHART
    # --------------------------------------------------

    st.markdown("### 📈 Candidate Match Scores")

    chart_data = pd.DataFrame({
        "Candidate": [
            r["file_name"] for r in results
        ],
        "Match Score (%)": [
            r["match_percentage"] for r in results
        ]
    }).set_index("Candidate")

    st.bar_chart(chart_data, height=250)

    # --------------------------------------------------
    # CANDIDATE COMPARISON
    # --------------------------------------------------

    st.markdown("---")
    st.markdown("## ⚖️ Candidate Comparison")
    st.caption(
        "Select candidates to compare their match scores, "
        "skills, experience and education side by side."
    )

    candidate_names = [r["file_name"] for r in results]

    selected_names = st.multiselect(
        "Choose candidates to compare",
        options=candidate_names,
        default=candidate_names[:min(2, len(candidate_names))],
        max_selections=5
    )

    if selected_names:

        selected_results = [
            r for r in results if r["file_name"] in selected_names
        ]

        comparison_data = []

        for r in selected_results:
            comparison_data.append({
                "Candidate": r["file_name"],
                "Match (%)": r["match_percentage"],
                "Matching Skills": ", ".join(
                    sorted(r["matching_skills"])
                ) or "None",
                "Missing Skills": ", ".join(
                    sorted(r["missing_skills"])
                ) or "None",
                "Experience (Years)": r["experience"],
                "Education": ", ".join(
                    str(e) for e in r["education"]
                ) or "Not detected"
            })

        st.dataframe(
            pd.DataFrame(comparison_data),
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------
    # FILTER AND SEARCH
    # --------------------------------------------------

    st.markdown("---")
    st.markdown("## 🏅 Candidate Rankings")

    filter_col, search_col = st.columns([1, 1.4])

    with filter_col:
        recommendation_filter = st.selectbox(
            "Filter by recommendation",
            [
                "All Candidates",
                "Highly Recommended",
                "Recommended",
                "Consider for Review",
                "Not Recommended"
            ]
        )

    with search_col:
        search_text = st.text_input(
            "🔍 Search candidate",
            placeholder="Enter resume filename..."
        )

    def get_recommendation(score):
        if score >= 80:
            return "Highly Recommended"
        elif score >= 60:
            return "Recommended"
        elif score >= 40:
            return "Consider for Review"
        return "Not Recommended"

    filtered_results = []

    for r in results:
        recommendation = get_recommendation(r["match_percentage"])

        matches_filter = (
            recommendation_filter == "All Candidates"
            or recommendation == recommendation_filter
        )

        matches_search = (
            search_text.strip().lower() in r["file_name"].lower()
        )

        if matches_filter and matches_search:
            filtered_results.append(r)

    if not filtered_results:
        st.info("No candidates match the selected filters.")

    else:
        ranking_data = []

        for rank, r in enumerate(filtered_results, start=1):
            ranking_data.append({
                "Rank": rank,
                "Candidate": r["file_name"],
                "Match (%)": r["match_percentage"],
                "Experience": f"{r['experience']} Years",
                "Recommendation": get_recommendation(
                    r["match_percentage"]
                )
            })

        ranking_df = pd.DataFrame(ranking_data)

        st.dataframe(
            ranking_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Match (%)": st.column_config.ProgressColumn(
                    "Match Score",
                    format="%.2f%%",
                    min_value=0,
                    max_value=100
                )
            }
        )

        # --------------------------------------------------
        # CSV EXPORT
        # --------------------------------------------------

        csv_data = ranking_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Export Ranking as CSV",
            data=csv_data,
            file_name="candidate_ranking.csv",
            mime="text/csv",
            use_container_width=True
        )

    # --------------------------------------------------
    # DETAILED CANDIDATE REPORTS
    # --------------------------------------------------

    st.markdown("---")
    st.markdown("## 🔎 Detailed Candidate Reports")

    for rank, result in enumerate(results, start=1):

        score = result["match_percentage"]
        recommendation = get_recommendation(score)

        safe_name = html.escape(result["file_name"])

        with st.expander(
            f"#{rank} · {result['file_name']} · {score}% match",
            expanded=(rank == 1)
        ):

            score_col, recommendation_col = st.columns([1, 2])

            with score_col:
                st.metric("Skill Match", f"{score}%")

            with recommendation_col:
                st.markdown(f"### {recommendation}")
                st.progress(min(max(score / 100, 0.0), 1.0))

            skill_col1, skill_col2 = st.columns(2)

            with skill_col1:
                st.markdown("#### ✅ Matching Skills")

                if result["matching_skills"]:
                    for skill in sorted(result["matching_skills"]):
                        st.markdown(
                            f"""
                            <span style="
                                display:inline-block;
                                background:#dcfce7;
                                color:#166534;
                                padding:6px 10px;
                                border-radius:18px;
                                margin:3px;
                                font-size:13px;
                                font-weight:600;
                            ">{html.escape(str(skill))}</span>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.write("No matching skills found.")

            with skill_col2:
                st.markdown("#### ❌ Missing Skills")

                if result["missing_skills"]:
                    for skill in sorted(result["missing_skills"]):
                        st.markdown(
                            f"""
                            <span style="
                                display:inline-block;
                                background:#fee2e2;
                                color:#991b1b;
                                padding:6px 10px;
                                border-radius:18px;
                                margin:3px;
                                font-size:13px;
                                font-weight:600;
                            ">{html.escape(str(skill))}</span>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.write("No missing skills detected.")

            st.markdown("#### 💼 Experience & Education")

            info1, info2 = st.columns(2)

            with info1:
                st.write(
                    f"**Candidate experience:** "
                    f"{result['experience']} years"
                )
                st.write(
                    f"**Required experience:** "
                    f"{required_experience} years"
                )

            with info2:
                education = result["education"]

                st.write(
                    "**Detected education:** "
                    + (
                        ", ".join(str(e) for e in education)
                        if education else "Not detected"
                    )
                )

                if required_education:
                    st.write(
                        "**Education keywords in job description:** "
                        + ", ".join(str(e) for e in required_education)
                    )

            st.markdown("#### 🤖 AI-Powered Insights")

            with st.spinner("Generating candidate insights..."):

                ai_response = get_ai_suggestions(
                    result["matching_skills"],
                    result["missing_skills"],
                    result["match_percentage"],
                    result["experience"],
                    result["education"]
                )

            st.write(ai_response)

    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------

    st.markdown("""
    <div style="
        text-align:center;
        padding:22px 10px;
        color:#77799b;
        font-size:12px;
    ">
        Resume Intelligence · AI-assisted candidate screening
        <br>
        Use these results as decision support alongside human review.
    </div>
    """, unsafe_allow_html=True)
