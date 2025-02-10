from fastapi import APIRouter, Request, HTTPException, Depends
from app.schemas import EmailSchema
from app.services import GmailService
from app.dependencies import get_credentials

router = APIRouter(prefix="/email", tags=["email"])

@router.post("/send")
async def send_email(
    email: EmailSchema,
    request: Request,
    credentials: dict = Depends(get_credentials)
):
    try:
        gmail_service = GmailService(credentials)
        message = gmail_service.create_message(
            to=email.recipient,
            subject=email.subject,
            message_text=email.body
        )
        result = gmail_service.send_message(message)
        return {"message": "Email sent successfully", "message_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 