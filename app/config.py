from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Gmail API settings
    ENABLE_GOOGLE_CONTACTS: bool = False  # Set to True only when scope is verified
    GMAIL_SEND_SCOPE: str = "https://www.googleapis.com/auth/gmail.send"
    CONTACTS_SCOPE: str = "https://www.googleapis.com/auth/contacts"
    REDIRECT_URI: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    CORS_ORIGINS: str
    EMAIL_REPLY_TO: str
    BACKEND_URL: str
    FRONTEND_URL: str
    DATABASE_URL: str
    # Login credentials
    USERNAME: str
    PASSWORD: str

    @property
    def SCOPES(self) -> List[str]:
        scopes = [self.GMAIL_SEND_SCOPE]
        if self.ENABLE_GOOGLE_CONTACTS:
            scopes.append(self.CONTACTS_SCOPE)
        return scopes

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings() 