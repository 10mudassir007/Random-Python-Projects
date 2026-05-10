from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

SKIP_DIRS = {"node_modules", ".git", "dist", "build", "__pycache__", ".next", "venv", '.ipynb_checkpoints'}
SKIP_EXTENSIONS = {".png", ".jpg", ".svg", ".ico", ".lock", ".sum", ".woff", ".ttf", ".keras", ".pickle", ".joblib", ".pyc", ".pkl", ".txt",".html"}

def get_github_token() -> str:
  return os.getenv("GITHUB_TOKEN")

def get_llm():
  model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=1.0,  # Gemini 3.0+ defaults to 1.0
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=os.getenv("GEMINI_API_KEY"),
  ) 
  return model