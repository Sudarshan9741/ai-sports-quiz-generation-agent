import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Model
GEMINI_MODEL = "gemini-flash-latest"

# ChromaDB Database Path
CHROMA_DB_PATH = "./chroma_db"

# Sports Data Path
SPORTS_DATA_PATH = "./data/sports_facts.json"

# Validate API Key
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Please add it to your .env file."
    )

