# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    ENDEE_URL = os.getenv("ENDEE_URL", "http://127.0.0.1:8080/api/v1")
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
    REPO_STORAGE_PATH = "data/repos"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

settings = Settings()


