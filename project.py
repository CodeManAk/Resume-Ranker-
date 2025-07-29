
import streamlit as st
from utils import extract_text_from_pdf, get_llm, score_resume

st.set_page_config(page_title="Resume Ranker", layout="centered")
st.title("📄 Resume Ranker using Azure OpenAI")

st.markdown("Upload a Job Description and multiple resumes to get ranked scores.")

jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
resume_files = st.file_uploader("Upload Resumes (PDFs)", type=["pdf"], accept_multiple_files=True)

if jd_file and resume_files:
    with st.spinner("Extracting and ranking..."):
        jd_text = extract_text_from_pdf(jd_file)
        llm = get_llm()

        scores = []
        for resume in resume_files:
            resume_text = extract_text_from_pdf(resume)
            score = score_resume(llm, jd_text, resume_text)
            scores.append((resume.name, score))

        scores.sort(key=lambda x: x[1], reverse=True)

    st.subheader("🏆 Ranked Resumes")
    for name, score in scores:
        st.write(f"**{name}** — Score: {score}/100")
