import dotenv
from dotenv import load_dotenv 
import os 

load_dotenv

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

GOOGLE_SERPER_API_KEY = os.getenv("GOOGLE_SERPER_API_KEY")

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

