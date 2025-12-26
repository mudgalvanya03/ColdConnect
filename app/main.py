import streamlit as st
import tempfile
import matplotlib.pyplot as plt
from chains import Chain
from resume import Resume


# Initialize Chain
chain = Chain()

st.set_page_config(
    page_title="ColdConnect - AI Cold Email Generator",
    page_icon="📧",
    layout="wide"
)

st.title("ColdConnect – AI-Powered Job Application Assistant")
st.markdown("Upload your resume + paste a job link → get a personalized **Cold Email + Cover Letter**, plus skill match analysis.")

# -------- Inputs --------
col1, col2 = st.columns(2)

with col1:
    uploaded_resume = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

with col2:
    job_url = st.text_input("Job Posting URL", placeholder="https://...")

tone = st.selectbox("Choose Output Tone", ["formal", "casual", "enthusiastic"])

generate_btn = st.button("Generate Email + Cover Letter")

# -------- Workflow --------
if generate_btn:
    if not uploaded_resume or not job_url:
        st.error("Please upload a resume and provide a job URL.")
    else:
        try:
            # Save uploaded resume temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_resume.read())
                resume_path = tmp.name

            # Process resume
            resume = Resume(dataset_folder=None)
            resume.file_path = resume_path
            resume.load_resume()

            # Extract job details
            with st.spinner("🔍 Scraping job details..."):
                jobs = chain.extract_from_url(job_url)

            st.subheader("📊 Extracted Job Details (JSON)")
            st.json(jobs)

            if jobs and "skills" in jobs[0]:
                # Match resume chunks with job skills
                resume_chunks = resume.match_with_job(jobs[0]["skills"], n_results=3)
                resume_summary = " ".join([" ".join(r) for r in resume_chunks])

                # -------- Skill Match & Resume Gap --------
                job_skills = [s.lower() for s in jobs[0].get("skills", [])]
                resume_text = resume_summary.lower()

                matched = [skill for skill in job_skills if skill in resume_text]
                missing = [skill for skill in job_skills if skill not in resume_text]

                # Skill match %
                if job_skills:
                    match_percent = int((len(matched) / len(job_skills)) * 100)
                else:
                    match_percent = 0

                st.subheader("Skill Match Analysis")
                st.progress(match_percent / 100)
                st.write(f"Match Score: **{match_percent}%**")

                if matched:
                    st.success("Matched Skills: " + ", ".join(matched))
                if missing:
                    st.error("Missing Skills: " + ", ".join(missing))

            else:
                resume_summary = "N/A"

            # -------- Generate Both Email + Cover Letter --------
            with st.spinner("Generating personalized cold email..."):
                email = chain.generate_email(jobs[0], resume_summary=resume_summary, tone=tone)

            with st.spinner("Generating personalized cover letter..."):
                cover_letter = chain.generate_cover_letter(jobs[0], resume_summary=resume_summary, tone=tone)

            # -------- Display Results --------
            st.subheader("Generated Cold Email")
            st.code(email, language="markdown")

            st.download_button(
                label="Download Email as TXT",
                data=email,
                file_name="cold_email.txt",
                mime="text/plain"
            )

            st.subheader("Generated Cover Letter")
            st.code(cover_letter, language="markdown")

            st.download_button(
                label="Download Cover Letter as TXT",
                data=cover_letter,
                file_name="cover_letter.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error: {e}")




