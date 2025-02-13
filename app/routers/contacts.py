from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import models
from database import get_db
from schemas import ContactCreate
from typing import List
from services import PeopleService
from dependencies import get_credentials, get_settings
from google.oauth2.credentials import Credentials
from config import Settings

router = APIRouter()

@router.post("/contacts")
def create_contact(
    contact: ContactCreate, 
    request: Request,
    db: Session = Depends(get_db),
    credentials: Credentials = Depends(get_credentials),
    settings: Settings = Depends(get_settings)
):
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
        
        # Create new contact in database
        new_contact = models.Contact(
            user_id=next_id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            email_address=contact.email_address,
            company_name=contact.company_name,
            phone_number=contact.phone_number,
            linkedin_url=contact.linkedin_url,
            email_sequence=1,
            join_date=datetime.now(),
            last_email_sent_at=datetime.now()
        )
        
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)

        # Only attempt Google Contacts creation if enabled
        if settings.ENABLE_GOOGLE_CONTACTS:
            try:
                people_service = PeopleService(credentials)
                google_contact = people_service.create_contact(contact)
                if google_contact:
                    print("Successfully created Google contact")
            except Exception as e:
                print(f"Failed to create Google contact: {str(e)}")

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
    Update sequences based on join date and active status:
    - Week 1-10: sequence = next active week number
    - After 10 weeks: sequence = 15 (monthly)
    """
    try:
        # Get all contacts
        contacts = db.query(models.Contact).all()
        # Get all sequence mappings with their active status
        sequences = db.query(models.SequenceMapping).order_by(
            models.SequenceMapping.sequence_id
        ).all()
        
        # Create a mapping of active sequences
        active_sequences = {seq.sequence_id: seq.is_active for seq in sequences}
        now = datetime.now().date()
        
        for contact in contacts:
            contact_join_date = contact.join_date.date()
            
            # If join date is in the future or today, set sequence to 1
            if contact_join_date >= now:
                if contact.email_sequence != 1:
                    contact.email_sequence = 1
                continue
            
            # Calculate weeks since joining (excluding today and future dates)
            days_since_join = (now - contact_join_date).days
            weeks_since_join = days_since_join // 7
            
            current_sequence = contact.email_sequence
            
            if weeks_since_join < 10:
                # Find the next active sequence
                new_sequence = current_sequence
                for seq_id in range(current_sequence + 1, 11):
                    if active_sequences.get(seq_id, False):
                        new_sequence = seq_id
                        break
                    
                # If no active sequences found until 10, move to monthly
                if new_sequence == current_sequence:
                    new_sequence = 15
            else:
                new_sequence = 15  # Monthly
                
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

@router.patch("/contacts/{contact_id}")
def update_contact_notes(
    contact_id: int,
    notes: dict,
    db: Session = Depends(get_db)
):
    contact = db.query(models.Contact).filter(models.Contact.user_id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    contact.notes = notes.get('notes')
    db.commit()
    db.refresh(contact)
    return contact 