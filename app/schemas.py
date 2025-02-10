from pydantic import BaseModel, EmailStr
from datetime import datetime

class EmailSchema(BaseModel):
    sender: EmailStr
    recipient: EmailStr
    subject: str
    body: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "sender": "your@email.com",
                "recipient": "recipient@email.com",
                "subject": "Test Email",
                "body": "This is a test email sent using Gmail API"
            }
        } 