from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime
from typing import List

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

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email_address: EmailStr

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    user_id: int
    email_sequence: int
    join_date: datetime
    last_email_sent_at: datetime

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

class EmailGroup(BaseModel):
    sequence_id: int
    group_name: str  # e.g., "Week 1", "Week 2", etc.
    contact_count: int
    contacts: List[Contact]

    class Config:
        from_attributes = True 

class GroupEmailSchema(BaseModel):
    sequence_id: int
    subject: str
    body: str
    article_link: HttpUrl
    
    class Config:
        json_schema_extra = {
            "example": {
                "sequence_id": 1,
                "subject": "Weekly Update",
                "body": "Here's your weekly update...",
                "article_link": "https://www.usobserver.com/article/123"
            }
        } 