from fastapi import APIRouter, Request, HTTPException, Depends
from app.schemas import EmailSchema
from app.services import GmailService
from app.dependencies import get_credentials
import os

router = APIRouter(prefix="/email", tags=["email"])

def get_template(template_name):
    template_path = os.path.join("app", "templates", f"{template_name}.txt")
    with open(template_path, "r") as file:
        return file.read()

@router.post("/send")
async def send_email(
    email: EmailSchema,
    request: Request,
    credentials: dict = Depends(get_credentials)
):
    try:
        # Get signature and disclaimer text
        try:
            signature = get_template("signature")
            disclaimer = get_template("disclaimer")
            print(f"Disclaimer length: {len(disclaimer)}")  # Debug print
        except FileNotFoundError as e:
            print(f"Template error: {str(e)}")  # Debug print
            signature = ""
            disclaimer = ""
        
        # Combine message body with signature and disclaimer
        full_message = (
            f"{email.body}\n\n"  # Add double line break after body
            f"{signature}\n\n"    # Add double line break after signature
            f"{disclaimer}"       # Disclaimer at the end
        )
        
        gmail_service = GmailService(credentials)
        message = gmail_service.create_message(
            to=email.recipient,
            subject=email.subject,
            message_text=full_message
        )
        result = gmail_service.send_message(message)
        return {"message": "Email sent successfully", "message_id": result.get("id")}
    except Exception as e:
        print(f"Error sending email: {str(e)}")  # Add logging
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        ) 