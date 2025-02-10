from pydantic import BaseModel, EmailStr, HttpUrl

class EmailSchema(BaseModel):
    recipient: EmailStr
    subject: str
    body: str  # This will now contain HTML content
    article_link: HttpUrl  # This will validate that it's a proper URL
    
    class Config:
        json_schema_extra = {
            "example": {
                "recipient": "example@email.com",
                "subject": "Important Information About Your Company",
                "body": "<html><body><h1>Your email content here...</h1></body></html>",
                "article_link": "https://www.usobserver.com/article/123"
            }
        } 