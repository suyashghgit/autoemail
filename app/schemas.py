from pydantic import BaseModel, EmailStr

class EmailSchema(BaseModel):
    recipient: EmailStr
    subject: str
    body: str  # This will now contain HTML content
    
    class Config:
        json_schema_extra = {
            "example": {
                "recipient": "example@email.com",
                "subject": "Important Information About Your Company",
                "body": "<html><body><h1>Your email content here...</h1></body></html>"
            }
        } 