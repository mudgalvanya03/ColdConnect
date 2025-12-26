import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            #model_name="llama-3.1-70b-versatile"
            model_name="groq/compound-mini"
        )

    def extract_from_text(self, cleaned_text):
        """Extract job details from scraped text into JSON format."""
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            The scraped text is from a career page.
            Extract the job postings and return JSON with keys:
            `role`, `experience`, `skills`, and `description`.

            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke({"page_data": cleaned_text})

        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Unable to parse jobs into JSON.")

        return res if isinstance(res, list) else [res]

    def extract_from_url(self, url):
        """Scrape and extract job details from a URL using WebBaseLoader."""
        from langchain_community.document_loaders import WebBaseLoader
        from utils import clean_text

        loader = WebBaseLoader([url])
        data = clean_text(loader.load().pop().page_content)
        return self.extract_from_text(data)

    def generate_email(self, job, resume_summary=None, tone="formal"):
        """Generate personalized cold email."""
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### CANDIDATE HIGHLIGHTS:
            {resume_summary}

            ### INSTRUCTION:
            Write a {tone} cold email to the hiring manager based on the job description.
            - Highlight relevant skills/achievements from candidate highlights.
            - Keep it concise and professional (150–200 words).
            - Do NOT include a preamble, only the email body.
            - Address as "Dear Hiring Manager".
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job),
            "resume_summary": resume_summary or "Candidate resume not available",
            "tone": tone
        })
        return res.content

    def generate_cover_letter(self, job, resume_summary=None, tone="formal"):
        """Generate personalized cover letter."""
        prompt_cover = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### CANDIDATE HIGHLIGHTS:
            {resume_summary}

            ### INSTRUCTION:
            Write a {tone} cover letter for this job.
            - Structure into paragraphs (Intro, Skills/Experience, Conclusion).
            - Highlight skills from candidate highlights that align with job description.
            - Be professional but approachable.
            - Address as "Dear Hiring Manager".
            - Keep length around 250–350 words.
            - Do NOT include a preamble, only the letter.
            """
        )
        chain_cover = prompt_cover | self.llm
        res = chain_cover.invoke({
            "job_description": str(job),
            "resume_summary": resume_summary or "Candidate resume not available",
            "tone": tone
        })
        return res.content


if __name__ == "__main__":
    url = "https://www.whitecarrot.io/resources/templates/job-descriptions/python-django-developer"
    chain = Chain()
    jobs = chain.extract_from_url(url)
    print("✅ Extracted Jobs JSON:\n", jobs)
    email = chain.generate_email(jobs[0], resume_summary="Skilled in Django, Python, REST APIs", tone="formal")
    print("\n📧 Email:\n", email)
    cover = chain.generate_cover_letter(jobs[0], resume_summary="Skilled in Django, Python, REST APIs", tone="formal")
    print("\n📄 Cover Letter:\n", cover)


