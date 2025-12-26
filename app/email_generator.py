"""
Standalone script to validate Groq LLM connectivity and prompt behavior.
Not used in the Streamlit application runtime. I used this to test the Groq integration. -Author.
"""
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

# Load API key from .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize the ChatGroq model
llm = ChatGroq(
    temperature=0,
    groq_api_key=api_key,
    model_name="groq/compound-mini"  # default model for personal API keys
)

# Test query
try:
    response = llm.invoke("The first person to land on the moon was ...")
    print("Response from Groq model:")
    print(response.content)
except Exception as e:
    print("Error calling Groq model:", e)

