# app/core/config.py

import os


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")


settings = Settings()
