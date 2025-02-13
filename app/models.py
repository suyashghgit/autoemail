from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Contact(Base):
    __tablename__ = "mailing_list"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email_address = Column(String(255), nullable=False, unique=True)
    company_name = Column(String(255))
    phone_number = Column(String(50))
    linkedin_url = Column(String(255))
    email_sequence = Column(Integer, default=0)
    join_date = Column(DateTime(timezone=True), nullable=False)
    last_email_sent_at = Column(DateTime(timezone=True), nullable=False)
    notes = Column(Text, nullable=True)

    email_metrics = relationship(
        "EmailMetric",
        back_populates="contact",
        cascade="all, delete-orphan"
    )

class SequenceMapping(Base):
    __tablename__ = "sequence_mapping"

    sequence_id = Column(Integer, primary_key=True)
    email_body = Column(Text, nullable=True)
    article_link = Column(String, nullable=True)
    email_subject = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

class EmailMetric(Base):
    __tablename__ = "email_metrics"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(
        Integer, 
        ForeignKey(
            "mailing_list.user_id",
            ondelete="CASCADE"
        )
    )
    sequence_id = Column(Integer)
    message_id = Column(String)
    status = Column(String)
    sent_at = Column(DateTime, default=datetime.now)
    
    contact = relationship(
        "Contact",
        back_populates="email_metrics",
        foreign_keys=[contact_id]
    )

class ActiveWeek(Base):
    __tablename__ = "active_weeks"

    sequence_id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class OAuthCredentials(Base):
    __tablename__ = "oauth_credentials"

    id = Column(Integer, primary_key=True)
    credential_type = Column(String(50))  # 'client_secret' or 'token'
    credentials_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now) 