from pydantic import BaseModel, EmailStr

class EmailSchema(BaseModel):
    recipient: EmailStr
    subject: str
    body: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "recipient": "example@email.com",
                "subject": "Important Information About Your Company",
                "body": "Your email content here..."
            }
        } 