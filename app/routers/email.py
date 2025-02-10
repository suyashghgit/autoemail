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
        except FileNotFoundError as e:
            print(f"Template error: {str(e)}")
            signature = ""
            disclaimer = ""
        
        # Combine message body with signature and disclaimer in HTML format
        full_message = f"""
        <html>
            <body>
                {email.body}
                {signature}
                <div style="color: #666; font-size: 12px; margin-top: 20px;">
                    {disclaimer}
                </div>
            </body>
        </html>
        """
        
        gmail_service = GmailService(credentials)
        message = gmail_service.create_message(
            to=email.recipient,
            subject=email.subject,
            message_text=full_message
        )
        result = gmail_service.send_message(message)
        return {"message": "Email sent successfully", "message_id": result.get("id")}
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        ) 