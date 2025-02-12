from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Gmail API settings
    CLIENT_SECRETS_FILE: str = "client_secret.json"
    ENABLE_GOOGLE_CONTACTS: bool = False  # Set to True only when scope is verified
    SCOPES: List[str] = [
        "https://www.googleapis.com/auth/gmail.send",
        # Only include contacts scope if enabled
        *(['https://www.googleapis.com/auth/contacts'] if ENABLE_GOOGLE_CONTACTS else [])
    ]
    REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    CLIENT_ID: str
    CLIENT_SECRET: str
    
    # Login credentials
    USERNAME: str = "admin"
    PASSWORD: str = "admin"  # In production, use proper password hashing

    class Config:
        env_file = ".env"

# Create settings instance
settings = Settings() 