from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from app.config import Settings
import os
from app.dependencies import get_settings
import json

router = APIRouter(prefix="/auth", tags=["auth"])

# Add this line at the top of the file
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # To allow HTTP for local development

@router.get("/gmail")
async def gmail_auth(request: Request, settings: Settings = Depends(get_settings)):
    try:
        flow = Flow.from_client_secrets_file(
            settings.CLIENT_SECRETS_FILE,
            scopes=settings.SCOPES,
            redirect_uri=settings.REDIRECT_URI
        )
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        request.session["oauth_state"] = state
        print(f"Auth URL: {authorization_url}")  # Debug print
        return RedirectResponse(authorization_url)
    except Exception as e:
        print(f"Auth error: {str(e)}")  # Debug print
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/callback")
async def oauth2callback(request: Request, settings: Settings = Depends(get_settings)):
    try:
        state = request.session.get("oauth_state")
        flow = Flow.from_client_secrets_file(
            settings.CLIENT_SECRETS_FILE,
            scopes=settings.SCOPES,
            state=state,
            redirect_uri=settings.REDIRECT_URI
        )
        
        authorization_response = str(request.url)
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        
        credentials_dict = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes,
            'expiry': credentials.expiry.isoformat() if credentials.expiry else None  # Add expiry time
        }
        
        # Store in session
        request.session["credentials"] = credentials_dict
        
        # Store in file
        with open('token.json', 'w') as token_file:
            json.dump(credentials_dict, token_file)
        
        return RedirectResponse(url="/")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Add new helper function to check and refresh token
async def get_valid_credentials(settings: Settings):
    try:
        # Try to load existing credentials
        if not os.path.exists('token.json'):
            return None
            
        with open('token.json', 'r') as token_file:
            credentials_dict = json.load(token_file)
            
        from google.oauth2.credentials import Credentials
        credentials = Credentials(
            token=credentials_dict['token'],
            refresh_token=credentials_dict['refresh_token'],
            token_uri=credentials_dict['token_uri'],
            client_id=credentials_dict['client_id'],
            client_secret=credentials_dict['client_secret'],
            scopes=credentials_dict['scopes']
        )
        
        # If credentials are expired, refresh them
        if credentials.expired:
            credentials.refresh(Request())
            # Update stored credentials
            credentials_dict = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes,
                'expiry': credentials.expiry.isoformat() if credentials.expiry else None
            }
            with open('token.json', 'w') as token_file:
                json.dump(credentials_dict, token_file)
                
        return credentials
    except Exception as e:
        print(f"Error refreshing credentials: {str(e)}")
        return None 