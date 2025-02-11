from fastapi import APIRouter, Request, HTTPException, Depends
from app import schemas
from app.schemas import EmailSchema, GroupEmailSchema
from app.services import GmailService
from app.dependencies import get_credentials
import os
import httpx
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from datetime import datetime
from sqlalchemy import func
from typing import List
from app.schemas import EmailGroup
from urllib.parse import urlparse

router = APIRouter(
    tags=["email"]  # Remove the prefix
)

def get_template(template_name):
    template_path = os.path.join("app", "templates", f"{template_name}.txt")
    with open(template_path, "r") as file:
        return file.read()

async def fetch_article_content(url: str) -> str:
    """Fetch and extract the main content from the article URL"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                # Return a default message instead of raising an exception
                return f"""
                <div class='blog-content'>
                    <p>The article content is currently unavailable. Please visit 
                    <a href="{url}">the article page</a> directly to read the full content.</p>
                </div>
                """
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the specific div with class "blog-content"
            article_content = soup.find('div', class_='blog-content')
            
            if article_content:
                # Clean up the content
                # Remove unwanted elements
                for script in article_content.find_all('script'):
                    script.decompose()
                for style in article_content.find_all('style'):
                    style.decompose()
                for iframe in article_content.find_all('iframe'):
                    iframe.decompose()
                
                # Convert relative URLs to absolute URLs
                base_url = str(url)
                for img in article_content.find_all('img'):
                    src = img.get('src', '')
                    if src and not src.startswith(('http://', 'https://')):
                        img['src'] = f"{base_url.rstrip('/')}/{src.lstrip('/')}"
                
                for a in article_content.find_all('a'):
                    href = a.get('href', '')
                    if href and not href.startswith(('http://', 'https://')):
                        a['href'] = f"{base_url.rstrip('/')}/{href.lstrip('/')}"
                
                return str(article_content)
            
            # If blog-content div not found, return a default message
            return f"""
            <div class='blog-content'>
                <p>The article content could not be extracted. Please visit 
                <a href="{url}">the article page</a> directly to read the full content.</p>
            </div>
            """
    except Exception as e:
        # Handle any network or parsing errors
        print(f"Error fetching article content: {str(e)}")
        return f"""
        <div class='blog-content'>
            <p>The article content is temporarily unavailable. Please visit 
            <a href="{url}">the article page</a> directly to read the full content.</p>
        </div>
        """

@router.post("/send")
async def send_email(
    email: EmailSchema,
    request: Request,
    credentials: dict = Depends(get_credentials)
):
    try:
        # Get signature and disclaimer text
        try:
            signature = get_template("signature")
            disclaimer = get_template("disclaimer")
        except FileNotFoundError as e:
            print(f"Template error: {str(e)}")
            signature = ""
            disclaimer = ""
        
        # Get absolute path to logo file
        logo_path = os.path.abspath(os.path.join("app", "templates", "logo.png"))
        print(f"Logo path: {logo_path}")  # Debug print
        
        if not os.path.exists(logo_path):
            print(f"Logo file not found at: {logo_path}")  # Debug print
            raise FileNotFoundError(f"Logo file not found at: {logo_path}")
        
        # Fetch article content
        article_content = await fetch_article_content(str(email.article_link))
        
        # Fixed message with dynamic link and embedded article
        fixed_message = f"""
        <div style="margin: 20px 0;">
            <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">Let's clear up your business's issues and protect what you've built.</p>
            <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;"><strong>Contact us today to learn how the US Observer can deliver results.</strong></p>
            <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;"><strong>Click <a href="{email.article_link}" style="color: #0066cc; text-decoration: underline;">HERE</a> to read about us</strong></p>
        </div>
        <div style="margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
            {article_content}
        </div>
        """
        
        # Combine message body with logo, signature and disclaimer in HTML format
        full_message = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        font-size: 14px;
                        color: #333;
                        line-height: 1.6;
                    }}
                </style>
            </head>
            <body>
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="cid:logo" alt="US Observer Logo" style="max-width: 100%; height: auto;">
                </div>
                <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    {email.body}
                </div>
                {fixed_message}
                <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    {signature}
                </div>
                <div style="font-family: Arial, sans-serif; font-size: 12px; color: #666; margin-top: 20px;">
                    {disclaimer}
                </div>
            </body>
        </html>
        """
        
        gmail_service = GmailService(credentials)
        message = gmail_service.create_message(
            to=email.recipient,
            subject=email.subject,
            message_text=full_message,
            image_path=logo_path
        )
        result = gmail_service.send_message(message)
        return {"message": "Email sent successfully", "message_id": result.get("id")}
    except FileNotFoundError as e:
        print(f"File error: {str(e)}")
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        )

@router.post("/send-group")
async def send_group_email(
    group_email: GroupEmailSchema,
    request: Request,
    db: Session = Depends(get_db),
    credentials: dict = Depends(get_credentials)
):
    try:
        print(f"Received request for sequence_id: {group_email.sequence_id}")  # Debug log
        
        # Get sequence mapping data
        sequence_mapping = db.query(models.SequenceMapping).filter(
            models.SequenceMapping.sequence_id == group_email.sequence_id
        ).first()
        
        print(f"Sequence mapping found: {sequence_mapping is not None}")  # Debug log
        
        if not sequence_mapping:
            raise HTTPException(
                status_code=404,
                detail=f"No sequence mapping found for sequence {group_email.sequence_id}"
            )

        # Get all contacts for the specified sequence
        contacts = db.query(models.Contact).filter(
            models.Contact.email_sequence == group_email.sequence_id
        ).all()
        
        print(f"Found {len(contacts)} contacts")  # Debug log
        
        if not contacts:
            raise HTTPException(
                status_code=404,
                detail=f"No contacts found in sequence {group_email.sequence_id}"
            )

        # Get templates
        try:
            signature = get_template("signature")
            disclaimer = get_template("disclaimer")
        except FileNotFoundError as e:
            print(f"Template error: {str(e)}")  # Debug log
            signature = ""
            disclaimer = ""

        # Get logo path
        logo_path = os.path.abspath(os.path.join("app", "templates", "logo.png"))
        print(f"Logo path: {logo_path}")  # Debug log
        
        if not os.path.exists(logo_path):
            print(f"Logo file not found at: {logo_path}")  # Debug log
            raise FileNotFoundError(f"Logo file not found at: {logo_path}")

        # Update group_email with sequence mapping data
        group_email.body = sequence_mapping.email_body
        
        # Ensure article_link is a valid URL
        article_link = sequence_mapping.article_link
        if not article_link.startswith(('http://', 'https://')):
            article_link = f'https://{article_link}'
        
        print(f"Article link: {article_link}")  # Debug log
        
        try:
            result = urlparse(article_link)
            if not all([result.scheme, result.netloc]):
                raise ValueError("Invalid URL format")
            group_email.article_link = article_link
        except Exception as e:
            print(f"URL parsing error: {str(e)}")  # Debug log
            raise HTTPException(
                status_code=400,
                detail=f"Invalid article link URL: {str(e)}"
            )

        # Fetch article content
        try:
            article_content = await fetch_article_content(str(group_email.article_link))
            print("Article content fetched successfully")  # Debug log
        except Exception as e:
            print(f"Error fetching article content: {str(e)}")  # Debug log
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch article content: {str(e)}"
            )

        # Create Gmail service
        gmail_service = GmailService(credentials)
        
        # Track successful and failed emails
        results = {
            "successful": [],
            "failed": []
        }

        # Send email to each contact
        for contact in contacts:
            try:
                print(f"Sending email to: {contact.email_address}")  # Debug log
                
                # Personalize message for each contact
                personalized_body = f"Dear {contact.first_name},\n\n{group_email.body}"
                
                # Create full message
                full_message = f"""
                <html>
                    <head>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                font-size: 14px;
                                color: #333;
                                line-height: 1.6;
                            }}
                        </style>
                    </head>
                    <body>
                        <div style="text-align: center; margin-bottom: 20px;">
                            <img src="cid:logo" alt="US Observer Logo" style="max-width: 100%; height: auto;">
                        </div>
                        <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                            {personalized_body}
                        </div>
                        <div style="margin: 20px 0;">
                            <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                                Let's clear up your business's issues and protect what you've built.
                            </p>
                            <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                                <strong>Contact us today to learn how the US Observer can deliver results.</strong>
                            </p>
                            <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                                <strong>Click <a href="{group_email.article_link}" style="color: #0066cc; text-decoration: underline;">HERE</a> to read about us</strong>
                            </p>
                        </div>
                        <div style="margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                            {article_content}
                        </div>
                        <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                            {signature}
                        </div>
                        <div style="font-family: Arial, sans-serif; font-size: 12px; color: #666; margin-top: 20px;">
                            {disclaimer}
                        </div>
                    </body>
                </html>
                """

                message = gmail_service.create_message(
                    to=contact.email_address,
                    subject=group_email.subject,
                    message_text=full_message,
                    image_path=logo_path
                )
                
                result = gmail_service.send_message(message)
                print(f"Email sent successfully to: {contact.email_address}")  # Debug log
                
                # Update last_email_sent_at
                contact.last_email_sent_at = datetime.now()
                db.commit()
                
                results["successful"].append({
                    "email": contact.email_address,
                    "message_id": result.get("id")
                })
                
            except Exception as e:
                print(f"Failed to send email to {contact.email_address}: {str(e)}")  # Debug log
                results["failed"].append({
                    "email": contact.email_address,
                    "error": str(e)
                })

        # Return summary
        return {
            "message": f"Completed sending group emails for sequence {group_email.sequence_id}",
            "total_contacts": len(contacts),
            "successful_sends": len(results["successful"]),
            "failed_sends": len(results["failed"]),
            "details": results
        }

    except Exception as e:
        print(f"Global error: {str(e)}")  # Debug log
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send group emails: {str(e)}"
        )

@router.get("/email_groups", response_model=List[schemas.EmailGroup])
def get_email_groups(db: Session = Depends(get_db)):
    """Get all contacts grouped by their sequence number"""
    groups = []
    
    # Query to get contacts grouped by sequence with counts
    sequences = db.query(
        models.Contact.email_sequence,
        func.count(models.Contact.user_id).label('contact_count')
    ).group_by(models.Contact.email_sequence).all()
    
    for sequence_id, count in sequences:
        # Skip sequence 0 as it's typically used for new/unassigned contacts
        if sequence_id == 0:
            continue
            
        # Get all contacts for this sequence
        contacts = db.query(models.Contact).filter(
            models.Contact.email_sequence == sequence_id
        ).all()
        
        # Create group name based on sequence ID
        group_name = f"Week {sequence_id}" if sequence_id <= 6 else "Monthly"
        
        # Create EmailGroup object
        group = {
            "sequence_id": sequence_id,
            "group_name": group_name,
            "contact_count": count,
            "contacts": contacts
        }
        groups.append(group)
    
    return sorted(groups, key=lambda x: x["sequence_id"]) 