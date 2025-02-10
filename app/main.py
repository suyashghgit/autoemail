from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import uvicorn
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.CLIENT_SECRET  # Using CLIENT_SECRET as session key
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from app.routers import auth, email
app.include_router(auth.router)
app.include_router(email.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Gmail API Service. Go to /auth/gmail to authenticate."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)