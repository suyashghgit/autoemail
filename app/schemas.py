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
    is_active: bool = True  # Add is_active field with default True

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
    success_rate: Optional[float] = 0.0  # Make it optional with default value

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
    subject: str = "Test subject"  # Default subject
    body: str = ""  # Will be populated from sequence_mapping
    article_link: Optional[str] = None  # Changed from HttpUrl to str
    
    class Config:
        json_schema_extra = {
            "example": {
                "sequence_id": 1,
                "subject": "Test subject"
            }
        } 

class ActiveWeek(BaseModel):
    sequence_id: int
    is_active: bool

    class Config:
        from_attributes = True 