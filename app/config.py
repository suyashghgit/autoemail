from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Gmail API settings
    CLIENT_SECRETS_FILE: str = "client_secret.json"
    SCOPES: List[str] = ["https://www.googleapis.com/auth/gmail.send"]
    REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    CLIENT_ID: str
    CLIENT_SECRET: str

    class Config:
        env_file = ".env"

# Create settings instance
settings = Settings() 