from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
import json
import re
import models, schemas
from database import get_db

router = APIRouter(
    prefix="/webhook",
    tags=["webhook"]
)

def extract_email_info(email_body: str) -> str:
    """
    Extract failed email address from the raw email body.
    Returns the email address found after "Your message wasn't delivered to".
    """
    try:
        failed_email_pattern = r"Your message wasn't delivered to \*(.*?@.*?)\*"
        failed_email_match = re.search(failed_email_pattern, email_body)
        
        if failed_email_match:
            # Return just the captured group (the email address)
            failed_email = failed_email_match.group(1)  # group(1) returns just what's in the parentheses
            print(failed_email)
            return failed_email
        return None
            
    except Exception as e:
        raise ValueError(f"Failed to extract email: {str(e)}")

@router.post("/zapier_status")
async def update_email_status(email_body: schemas.EmailBody, db: Session = Depends(get_db)):
    try:
        email_address = extract_email_info(email_body.email_body)
        if not email_address:
            raise HTTPException(
                status_code=400,
                detail="Could not extract email address from the email body"
            )
        
        # Updated to use Contact model with correct primary key name
        contact = db.query(models.Contact).filter(
            models.Contact.email_address == email_address
        ).first()
        
        if not contact:
            raise HTTPException(
                status_code=404,
                detail=f"Email address {email_address} not found in contacts"
            )
        
        latest_message = db.query(models.EmailMetric).filter(
            models.EmailMetric.contact_id == contact.user_id  # Changed from contact.id to contact.user_id
        ).order_by(desc(models.EmailMetric.sent_at)).first()
        
        if not latest_message:
            raise HTTPException(
                status_code=404,
                detail=f"No messages found for contact_id {contact.user_id}"  # Changed from contact.id to contact.user_id
            )
        
        latest_message.status = "failed"
        db.commit()
        
        return {
            "message": "Email status updated successfully",
            "email_address": email_address,
            "contact_id": contact.user_id,  # Changed from contact.id to contact.user_id
            "message_id": latest_message.message_id
        }
            
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process email body: {str(e)}"
        ) 
    