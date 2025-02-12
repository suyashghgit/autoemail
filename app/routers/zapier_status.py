from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
import json
import re
from .. import models, schemas
from ..database import get_db

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
async def update_email_status(email_body: schemas.EmailBody):
    try:
        # Extract information from the email body
        email_info = extract_email_info(email_body.email_body)
        
        return {
            "message": "Email body processed successfully",
            "request_body": email_body.email_body,  # Include the original request body
            "extracted_info": email_info
        }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process email body: {str(e)}"
        ) 
    