from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class Contact(Base):
    __tablename__ = "mailing_list"

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email_address = Column(String(255), nullable=False, unique=True)
    email_sequence = Column(Integer, default=0)
    join_date = Column(DateTime(timezone=True), nullable=False)
    last_email_sent_at = Column(DateTime(timezone=True), nullable=False) 