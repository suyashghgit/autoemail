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
        
        # Get absolute path to logo file
        logo_path = os.path.abspath(os.path.join("app", "templates", "logo.png"))
        print(f"Logo path: {logo_path}")  # Debug print
        
        if not os.path.exists(logo_path):
            print(f"Logo file not found at: {logo_path}")  # Debug print
            raise FileNotFoundError(f"Logo file not found at: {logo_path}")
        
        # Fixed message with dynamic link
        fixed_message = f"""
        <div style="margin: 20px 0;">
            <p>Contact us today to learn how the US Observer can deliver results.</p>
            <p>Click <a href="{email.article_link}" style="color: #0066cc; text-decoration: underline;">HERE</a> to read about us</p>
        </div>
        """
        
        # Combine message body with logo, signature and disclaimer in HTML format
        full_message = f"""
        <html>
            <body>
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="cid:logo" alt="US Observer Logo" style="max-width: 100%; height: auto;">
                </div>
                {email.body}
                {fixed_message}
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
            message_text=full_message,
            image_path=logo_path
        )
        result = gmail_service.send_message(message)
        return {"message": "Email sent successfully", "message_id": result.get("id")}
    except FileNotFoundError as e:
        print(f"File error: {str(e)}")
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        ) 