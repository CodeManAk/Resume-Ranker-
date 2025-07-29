import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from io import BytesIO
from langchain_openai import AzureChatOpenAI

load_dotenv()

def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def get_llm():
    return AzureChatOpenAI(
        api_key=os.getenv(""),
        azure_endpoint=os.getenv(""),
        api_version=os.getenv("2025-01-01-preview"),
        deployment_name=os.getenv("gpt-4o"),
        temperature=0
    )

def score_resume(llm, jd_text: str, resume_text: str) -> float:
    prompt = (
        "You are a recruiter. Based on the following job description:\n\n"
        f"{jd_text}\n\n"
        "Evaluate the following resume:\n\n"
        f"{resume_text}\n\n"
        "Give a score out of 100 based on how well this resume matches the job description. Just return the number."
    )
    response = llm.invoke(prompt)
    try:
        return float(response.content.strip().split()[0])
    except:
        return 0.0
