ColdConnect

AI-Powered Cold Email & Cover Letter Generator

ColdConnect is a Streamlit-based GenAI application that generates personalized cold emails and cover letters from a job posting URL and a candidate’s resume.
It also performs resume–job skill matching using semantic search.

This project focuses on practical, production-oriented GenAI usage rather than demo workflows.

## Features

- **Job Description Extraction**
  - Scrapes job postings from a given URL
  - Extracts role, experience, skills, and description into structured JSON

- **Resume Understanding**
  - Parses PDF resumes
  - Stores semantic embeddings using ChromaDB
  - Retrieves the most relevant resume sections for a job

- **AI Content Generation**
  - Personalized cold email
  - Tailored cover letter
  - Multiple tone options (formal, casual, enthusiastic)

- **Skill Match Analysis**
  - Resume vs job skill comparison
  - Match percentage
  - Highlighted missing skills

- **Downloadable Outputs**
  - Email and cover letter as text files

## Tech Stack

### Frontend
Streamlit is used to build the interactive web interface for uploading resumes, entering job URLs, and displaying generated outputs.

### Large Language Model Performance (Groq)

Initially, LLM inference was tested using local CPU-based inference, which resulted in significantly high latency. End-to-end generation of cold emails and cover letters took more than 5 minutes due to limited compute and sequential processing.

To address this performance bottleneck, Groq was integrated as the LLM provider via LangChain. With Groq’s optimized inference infrastructure, the same end-to-end workflow execution time was reduced to approximately 1–2 minutes.

This change resulted in:
- Drastically reduced response latency
- Improved user experience in the Streamlit application
- Faster iteration during development and testing

The decision to use Groq was driven by practical performance considerations rather than model capability alone, making the application more responsive and usable in real-world scenarios.

### Prompt Orchestration
LangChain is used to manage prompts, chain LLM calls, and structure AI outputs.

### Embeddings
HuggingFace Sentence Transformers (all-MiniLM-L6-v2) are used to generate semantic embeddings for resume content.

### Vector Database
ChromaDB is used as a local vector store to persist and query resume embeddings for semantic matching.

### PDF Processing
PyPDF2 is used to extract text from uploaded PDF resumes.

### Environment Management
python-dotenv is used to manage API keys and environment variables securely.

## Project Structure

The project is organized to separate application logic, AI orchestration, and data processing concerns for better readability and maintainability.

### Application Layer
The Streamlit application is located inside the `app` directory and serves as the main entry point for user interaction.

### AI Orchestration
The core AI logic is implemented using LangChain and Groq. This layer is responsible for job extraction, prompt orchestration, and content generation.

### Resume Processing
Resume parsing, embedding generation, and semantic search logic are handled separately to enable efficient resume–job matching.

### Vector Storage
ChromaDB is used as a local vector store to persist resume embeddings which also helps in semantic search. The generated vector data is excluded from version control since it is created dynamically at runtime.

### Configuration and Dependencies
Environment variables, Streamlit configuration, and dependency management are handled separately to keep the codebase clean and secure.

## Setup Instructions

Follow the steps below to set up and run the project locally.

### Clone the Repository
Clone the repository from GitHub and navigate into the project directory.

git clone https://github.com/<your-username>/ColdConnect.git  
cd ColdConnect

### Install Dependencies
Install all required Python dependencies using the provided requirements file.

pip install -r requirements.txt

### Configure Environment Variables
Create a `.env` file inside the `app` directory and add your Groq API key.

GROQ_API_KEY=your_groq_api_key_here

The `.env` file is excluded from version control to protect sensitive credentials.

## Run Application

After completing the setup steps, the application can be started locally using Streamlit.

### Start the Streamlit App
Run the following command from the project root directory.

streamlit run app/main.py

### Application Access
Once the command is executed, Streamlit will start a local server and automatically open the application in the browser. If it does not open automatically, the local URL will be displayed in the terminal.

### Usage Flow
Upload a resume in PDF format, provide a job posting URL, select the desired tone, and generate a personalized cold email and cover letter along with skill match analysis.

## Use Cases

This application is designed to support real-world job application and outreach workflows.

### Job Applications at Scale
Helps candidates generate personalized cold emails and cover letters for multiple job applications without writing each one manually.

### Personalized Outreach
Enables tailored communication with hiring managers instead of sending generic application emails.

### Resume and Job Matching
Assists candidates in understanding how well their resume aligns with a job description and identifies missing skills.

### GenAI Demonstration Project
Serves as a practical example of applying GenAI, semantic search, and vector databases in a production-style application.

## Future Enhancements

The following improvements are planned to further enhance the functionality and scalability of the application.

### Resume Gap Analysis
Provide detailed feedback on missing skills along with suggested learning resources and improvement areas.

### Multiple Resume Support
Allow users to upload and manage multiple resumes for different job roles.

### Advanced Job Scraping
Improve job description extraction accuracy across different job portals and layouts.

### Email Export and Integration
Enable exporting generated emails and cover letters to PDF and integrate with email platforms such as Gmail.

### Deployment and Scalability
Containerize the application using Docker and explore cloud deployment options for broader accessibility.

## Author

Vanya Mudgal  
QA Engineer | Aspiring SDET