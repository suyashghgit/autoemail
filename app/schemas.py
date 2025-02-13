from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime
from typing import List, Optional

class EmailSchema(BaseModel):
    recipient: str
    subject: str
    body: str  # This will now contain HTML content
    article_link: str
    contact_id: int
    sequence_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "recipient": "example@email.com",
                "subject": "Important Information About Your Company",
                "body": "<p>Your <strong>formatted</strong> email content here...</p>",
                "article_link": "https://www.usobserver.com/article/123"
            }
        } 

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email_address: EmailStr
    company_name: Optional[str] = None
    phone_number: Optional[str] = None
    linkedin_url: Optional[str] = None
    notes: Optional[str] = None

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
    email_subject: Optional[str] = ''
    is_active: bool = True

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
    delivery_rate: float
    success_rate: Optional[float] = 0.0

    class Config:
        from_attributes = True 

class EmailGroup(BaseModel):
    sequence_id: int
    group_name: str
    contact_count: int
    contacts: List[Contact]

    class Config:
        from_attributes = True 

class GroupEmailSchema(BaseModel):
    sequence_id: int
    recipient: Optional[str] = None
    contact_id: Optional[int] = None
    subject: Optional[str] = None
    body: str = ""
    article_link: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "sequence_id": 1,
                "subject": "Optional fallback subject"
            }
        } 

class ActiveWeek(BaseModel):
    sequence_id: int
    is_active: bool

    class Config:
        from_attributes = True 

class EmailStatusUpdate(BaseModel):
    email_address: EmailStr
    status: str
    message_id: Optional[str] = None
    error_message: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "email_address": "example@email.com",
                "status": "bounced",
                "message_id": "12345",
                "error_message": "Mailbox full"
            }
        } 

class EmailBody(BaseModel):
    email_body: str 

class OAuthCredentialsSchema(BaseModel):
    credential_type: str
    credentials_json: str
    
    class Config:
        from_attributes = True 