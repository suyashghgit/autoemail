from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import uvicorn
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import httpx

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

# Set up scheduler
scheduler = BackgroundScheduler()

# Function to update sequences
async def update_sequences_job():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(
                "http://localhost:8000/contacts/update-sequences"
            )
            print("Sequences updated:", response.status_code)
        except Exception as e:
            print("Error updating sequences:", str(e))

# Schedule the job to run daily at midnight
scheduler.add_job(
    update_sequences_job,
    trigger=CronTrigger(hour=0, minute=0),
    id='update_sequences',
    name='Update email sequences daily'
)

# Function to send scheduled emails
async def send_scheduled_emails():
    """Send emails to all active groups every Tuesday"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/schedule-group-emails"
            )
            print("Tuesday scheduled emails:", response.status_code)
            print("Response:", response.json())
    except Exception as e:
        print("Error sending scheduled emails:", str(e))

# Add the Tuesday schedule
scheduler.add_job(
    send_scheduled_emails,
    trigger=CronTrigger(
        day_of_week='tue',  # Every Tuesday
        hour=9,  # At 9 AM
        minute=0
    ),
    id='send_tuesday_emails',
    name='Send group emails every Tuesday'
)

@app.on_event("startup")
async def start_scheduler():
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_scheduler():
    scheduler.shutdown()

# Include routers
from app.routers import auth, email, contacts, sequences, dashboard, weeks, zapier_status
app.include_router(auth.router)
app.include_router(email.router)
app.include_router(contacts.router)
app.include_router(sequences.router, prefix="/sequences")
app.include_router(dashboard.router)
app.include_router(weeks.router)
app.include_router(zapier_status.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Gmail API Service. Go to /auth/gmail to authenticate."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)