from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from sqlalchemy.orm import Session
from database import get_db
from models import OAuthCredentials
from config import Settings
import os
from dependencies import get_settings
import json
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from config import settings
from pydantic import BaseModel
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest

router = APIRouter(prefix="/auth", tags=["auth"])

# Add this line at the top of the file
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # To allow HTTP for local development

security = HTTPBasic()

class LoginCredentials(BaseModel):
    username: str
    password: str

async def get_client_secrets(db: Session):
    client_secrets = db.query(OAuthCredentials).filter(
        OAuthCredentials.credential_type == "client_secret"
    ).first()
    if not client_secrets:
        raise HTTPException(status_code=500, detail="Client secrets not found in database")
    return json.loads(client_secrets.credentials_json)

async def save_token(db: Session, credentials_dict: dict):
    # Get the client_id from the credentials_dict

    if not credentials_dict.get('refresh_token'):
        print("Warning: No refresh token received. Ensure access_type='offline' and prompt='consent'.")
        return
    
    client_id = credentials_dict.get('client_id')
    
    # Find existing token record for this client_id
    token_record = db.query(OAuthCredentials).filter(
        OAuthCredentials.credential_type == "token",
        OAuthCredentials.credentials_json.contains(client_id)  # This checks if the client_id exists in the JSON
    ).first()
    
    if token_record:
        # Update existing record
        token_record.credentials_json = json.dumps(credentials_dict)
    else:
        # Create new record only if none exists
        token_record = OAuthCredentials(
            credential_type="token",
            credentials_json=json.dumps(credentials_dict)
        )
        db.add(token_record)
    
    db.commit()
    return token_record

@router.get("/gmail")
async def gmail_auth(
    request: Request, 
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db)
):
    try:
        client_secrets = await get_client_secrets(db)
        flow = Flow.from_client_config(
            client_secrets,
            scopes=settings.SCOPES,
            redirect_uri=settings.REDIRECT_URI
        )
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'  # Forces Google to show the consent screen again
        )
        
        request.session["oauth_state"] = state
        print(f"Auth URL: {authorization_url}")  # Debug print
        return RedirectResponse(authorization_url)
    except Exception as e:
        print(f"Auth error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/callback")
async def oauth2callback(
    request: Request, 
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db)
):
    try:
        state = request.session.get("oauth_state")
        client_secrets = await get_client_secrets(db)
        
        flow = Flow.from_client_config(
            client_secrets,
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
            'expiry': credentials.expiry.isoformat() if credentials.expiry else None
        }
        
        # Store in session
        request.session["credentials"] = credentials_dict
        
        # Store in database
        await save_token(db, credentials_dict)
        
        return RedirectResponse(url="/")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def get_valid_credentials(settings: Settings, db: Session = Depends(get_db)):
    try:
        # First try to get refresh token
        refresh_token_record = db.query(OAuthCredentials).filter(
            OAuthCredentials.credential_type == "refresh_token"
        ).first()
        
        # Then get the token record
        token_record = db.query(OAuthCredentials).filter(
            OAuthCredentials.credential_type == "token"
        ).first()
        
        if not refresh_token_record:
            print("No refresh token found in database")
            return None
            
        try:
            refresh_token_dict = json.loads(refresh_token_record.credentials_json)
            refresh_token = refresh_token_dict.get('refresh_token')
        except json.JSONDecodeError:
            # If the refresh token is stored as plain text, try to use it directly
            refresh_token = refresh_token_record.credentials_json.strip()
            # Update the record to store it properly as JSON
            refresh_token_record.credentials_json = json.dumps({"refresh_token": refresh_token})
            db.commit()
        
        if not refresh_token:
            print("Invalid refresh token format in database")
            return None
            
        # Get client secrets for refresh
        client_secrets = await get_client_secrets(db)
        
        # If we have a token record, use its values
        if token_record:
            try:
                credentials_dict = json.loads(token_record.credentials_json)
                token = credentials_dict.get('token')
                scopes = credentials_dict.get('scopes')
            except json.JSONDecodeError:
                print("Error parsing token record JSON")
                token = None
                scopes = settings.SCOPES
        else:
            token = None
            scopes = settings.SCOPES  # Use default scopes from settings
        
        # Create credentials object
        credentials = Credentials(
            token=token,
            refresh_token=refresh_token,
            token_uri=client_secrets['web']['token_uri'],
            client_id=client_secrets['web']['client_id'],
            client_secret=client_secrets['web']['client_secret'],
            scopes=scopes
        )
        
        # Always try to refresh the token
        if not credentials.valid:
            request = GoogleRequest()
            credentials.refresh(request)
            
            # Update stored credentials after refresh
            updated_credentials_dict = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes,
                'expiry': credentials.expiry.isoformat() if credentials.expiry else None
            }
            await save_token(db, updated_credentials_dict)
                
        return credentials
    except Exception as e:
        print(f"Error in get_valid_credentials: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None

@router.post("/login")
async def login(credentials: LoginCredentials):
    if (credentials.username == settings.USERNAME and 
        credentials.password == settings.PASSWORD):
        return {"status": "success"}
    raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )

# Add this function to auth.py
async def get_authenticated_credentials(
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db)
) -> Credentials:
    credentials = await get_valid_credentials(settings, db)
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated. Please authenticate with Gmail first.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return credentials 