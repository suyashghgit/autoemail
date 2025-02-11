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

class Contact(BaseModel):
    id: int
    user_id: str
    first_name: str
    last_name: str
    email: str
    sequence: str

    class Config:
        from_attributes = True 

class SequenceMappingBase(BaseModel):
    email_body: str
    article_link: HttpUrl

class SequenceMappingCreate(SequenceMappingBase):
    sequence_id: int

class SequenceMapping(SequenceMappingBase):
    sequence_id: int

    class Config:
        from_attributes = True 

class SequenceStats(BaseModel):
    sequence_id: int
    sequence_name: str
    total_contacts: int
    completed_contacts: int
    pending_contacts: int
    success_rate: float

    class Config:
        from_attributes = True 