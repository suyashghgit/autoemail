from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from .. import models
from ..database import get_db
from ..schemas import ContactCreate
from typing import List

router = APIRouter()

@router.post("/contacts")
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_contact = db.query(models.Contact).filter(
        models.Contact.email_address == contact.email_address
    ).first()
    
    if existing_contact:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    try:
        # Get the next available user_id
        max_id = db.query(func.max(models.Contact.user_id)).scalar() or 0
        next_id = max_id + 1
        
        # Create new contact
        new_contact = models.Contact(
            user_id=next_id,  # Explicitly set the next ID
            first_name=contact.first_name,
            last_name=contact.last_name,
            email_address=contact.email_address,
            email_sequence=1,  # Start with sequence 1
            join_date=datetime.now(),
            last_email_sent_at=datetime.now()
        )
        
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return new_contact
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating the contact: {str(e)}"
        )

@router.get("/contacts")
def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).order_by(models.Contact.user_id.asc()).all()
    return contacts

@router.put("/update-sequences")
def update_sequences(db: Session = Depends(get_db)):
    """
    Update sequences based on join date:
    - Week 1-6: sequence = week number
    - After 6 weeks: sequence = 9 (monthly)
    """
    try:
        # Get all contacts
        contacts = db.query(models.Contact).all()
        now = datetime.now()
        
        for contact in contacts:
            # Calculate weeks since joining
            weeks_since_join = (now - contact.join_date).days // 7
            
            # Determine new sequence
            if weeks_since_join < 6:
                new_sequence = weeks_since_join + 1
            else:
                new_sequence = 9
                
            # Update sequence if different
            if contact.email_sequence != new_sequence:
                contact.email_sequence = new_sequence
        
        db.commit()
        return {"message": "Sequences updated successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error updating sequences: {str(e)}"
        ) 