from fastapi import Request, HTTPException, Depends
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest
import json
import os
from app.config import Settings

def get_settings():
    return Settings()

def get_credentials(request: Request, settings: Settings = Depends(get_settings)):
    # First try to get from session
    credentials_dict = request.session.get("credentials")
    
    # If not in session, try to load from file
    if not credentials_dict and os.path.exists('token.json'):
        try:
            with open('token.json', 'r') as token_file:
                credentials_dict = json.load(token_file)
        except Exception as e:
            credentials_dict = None
    
    if not credentials_dict:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated. Please authenticate with Gmail first."
        )
    
    credentials = Credentials(
        token=credentials_dict["token"],
        refresh_token=credentials_dict["refresh_token"],
        token_uri=credentials_dict["token_uri"],
        client_id=credentials_dict["client_id"],
        client_secret=credentials_dict["client_secret"],
        scopes=credentials_dict["scopes"]
    )
    
    # If credentials are expired and can be refreshed, refresh them
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(GoogleRequest())
        
        # Update the stored credentials
        credentials_dict = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        request.session["credentials"] = credentials_dict
        
        # Save to file
        with open('token.json', 'w') as token_file:
            json.dump(credentials_dict, token_file)
    
    return credentials 