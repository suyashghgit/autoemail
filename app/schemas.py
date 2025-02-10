from pydantic import BaseModel, EmailStr

class EmailSchema(BaseModel):
    recipient: EmailStr
    subject: str
    body: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "recipient": "recipient@example.com",
                "subject": "Test Email",
                "body": "This is a test email sent using Gmail API"
            }
        } 