from fastapi import Request, HTTPException, Depends
from google.oauth2.credentials import Credentials
from app.config import Settings

def get_settings():
    return Settings()

def get_credentials(request: Request):
    credentials_dict = request.session.get("credentials")
    if not credentials_dict:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated. Please authenticate with Gmail first."
        )
    
    return Credentials(
        token=credentials_dict["token"],
        refresh_token=credentials_dict["refresh_token"],
        token_uri=credentials_dict["token_uri"],
        client_id=credentials_dict["client_id"],
        client_secret=credentials_dict["client_secret"],
        scopes=credentials_dict["scopes"]
    ) 