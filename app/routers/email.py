from fastapi import APIRouter, Request, HTTPException, Depends
import schemas
from schemas import EmailSchema, GroupEmailSchema
from services import GmailService
from dependencies import get_credentials
import os
import httpx
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from database import get_db
from models import EmailMetric, SequenceMapping, Contact
from datetime import datetime
from sqlalchemy import func
from typing import List
from schemas import EmailGroup
from urllib.parse import urlparse
import asyncio
from config import settings 
from routers.auth import get_authenticated_credentials
from google.oauth2.credentials import Credentials
from config import Settings
from dependencies import get_settings
from googleapiclient.discovery import build
import models
from fastapi.responses import FileResponse
import time

router = APIRouter(
    tags=["email"]  # Remove the prefix
)

def get_template(template_name):
    template_path = os.path.join("templates", f"{template_name}.txt")
    with open(template_path, "r") as file:
        return file.read()

async def fetch_article_content(url: str) -> str:
    """Fetch and extract the main content from the article URL"""
    if not url or not url.strip():
        return """
        <div class='blog-content' style='text-align: justify;'>
            <p>No article link provided.</p>
        </div>
        """
        
    try:
        # Add timeout and follow_redirects parameters
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            print(f"Attempting to fetch content from: {url}")  # Debug log
            
            # Add headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            response = await client.get(url, headers=headers)
            print(f"Response status code: {response.status_code}")  # Debug log
            
            if response.status_code != 200:
                return f"""
                <div class='blog-content' style='text-align: justify;'>
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="cid:logo" alt="US Observer Logo" style="max-width: 100%; height: auto;">
                    </div>
                    <p>The article content is currently unavailable (Status: {response.status_code}). Please visit 
                    <a href="{url}">the article page</a> directly to read the full content.</p>
                </div>
                """
            
            # Print the first 500 characters of the response for debugging
            print(f"Response content preview: {response.text[:500]}")
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            article_content = soup.find('div', class_='blog-content')
            
            if not article_content:
                print("Could not find blog-content div")  # Debug log
                # Try alternative content selectors
                article_content = (
                    soup.find('article') or 
                    soup.find('div', class_='post-content') or
                    soup.find('div', class_='entry-content')
                )
            
            if article_content:
                print("Successfully found article content")  # Debug log
                # Only remove potentially harmful elements
                for script in article_content.find_all('script'):
                    script.decompose()
                for iframe in article_content.find_all('iframe'):
                    iframe.decompose()
                
                # Add container styles to article_content
                article_content['style'] = (
                    "padding: 30px; "
                    "border-radius: 5px; "
                    "overflow: hidden;"  # This ensures floating images stay within
                )
                
                # Add padding to the first paragraph
                first_p = article_content.find_all('p')
                if first_p:  # Check if any paragraphs exist
                    first_p[0]['style'] = 'padding: 0 20px; text-align: center;'  # Center alignment with padding
                
                # Keep all style tags and CSS classes
                # Convert relative URLs to absolute URLs
                base_url = urlparse(url)
                base_domain = f"{base_url.scheme}://{base_url.netloc}"
                
                # Enhance image handling
                for img in article_content.find_all('img'):
                    try:
                        # Convert relative URLs to absolute
                        src = img.get('src', '')
                        if src:
                            if src.startswith('/'):
                                img['src'] = f"{base_domain}{src}"
                            elif not src.startswith(('http://', 'https://')):
                                img['src'] = f"{base_domain}/{src.lstrip('/')}"
                        
                        # Find parent wp-caption div if it exists
                        wp_caption = img.find_parent('div', class_=lambda x: x and 'wp-caption' in x.split())
                        
                        # Determine alignment from wp-caption classes
                        alignment = 'left'  # default
                        if wp_caption:
                            classes = wp_caption.get('class', [])
                            if isinstance(classes, str):
                                classes = classes.split()
                            if 'alignright' in classes:
                                alignment = 'right'
                            elif 'aligncenter' in classes:
                                alignment = 'center'
                        
                        # Create container with alignment-specific styles
                        container = soup.new_tag('div')
                        container['class'] = 'image-container'
                        
                        # Base styles
                        container_style = (
                            "border: 1px solid #ddd; "
                            "padding: 4px; "
                            "margin: 10px 0; "
                            "display: inline-block; "
                            "max-width: 100%; "
                            "box-sizing: border-box; "
                        )
                        
                        # Add alignment-specific styles
                        if alignment == 'right':
                            container_style += (
                                "float: right; "
                                "margin-left: 15px; "
                                "margin-bottom: 10px;"
                            )
                        elif alignment == 'center':
                            container_style += (
                                "float: none; "
                                "margin: 10px auto; "
                                "display: block; "
                                "text-align: center;"
                            )
                        else:  # left alignment
                            container_style += (
                                "float: left; "
                                "margin-right: 15px; "
                                "margin-bottom: 10px;"
                            )
                        
                        container['style'] = container_style
                        
                        # Rest of the image handling remains the same
                        img['style'] = "max-width: 100%; height: auto; display: block; margin: 0;"
                        img.wrap(container)
                        
                        # Caption handling with alignment
                        caption = None
                        if wp_caption:
                            caption = wp_caption.find('p', class_='wp-caption-text')
                        if not caption:
                            caption = img.find_next('p', class_='wp-caption-text')
                        if not caption:
                            caption = img.find_next('p', id=lambda x: x and 'caption-attachment' in x)
                        
                        if caption:
                            caption_div = soup.new_tag('div')
                            caption_div['style'] = f"margin: 5px 0 0 0; text-align: {alignment}; font-style: italic;"
                            caption_div.string = caption.get_text()
                            container.append(caption_div)
                            if wp_caption:
                                wp_caption.unwrap()  # Remove the original wp-caption div
                            caption.decompose()  # Remove original caption
                    
                    except Exception as img_error:
                        print(f"Error processing image: {str(img_error)}")
                        continue
                
                # Add clearfix at the end of content
                clear_div = soup.new_tag('div')
                clear_div['style'] = "clear: both;"
                article_content.append(clear_div)
                
                # Preserve all original classes and styles
                # Remove the logo from article_content
                return f"""
                    <div style='text-align: justify;'>
                        {str(article_content)}
                    </div>
                """
            else:
                print("No article content found with any selector")  # Debug log
                return f"""
                <div class='blog-content' style='text-align: justify;'>
                    <p>Unable to extract the article content. Please visit 
                    <a href="{url}">the article page</a> directly to read the full content.</p>
                </div>
                """
    except Exception as e:
        print(f"Error fetching article content: {str(e)}")
        print(f"Error type: {type(e)}")  # Additional error info
        print(f"Error details: {e.__dict__}")  # More error details if available
        return f"""
        <div class='blog-content' style='text-align: justify;'>
            <p>The article content is temporarily unavailable (Error: {str(e)}). Please visit 
            <a href="{url}">the article page</a> directly to read the full content.</p>
        </div>
        """

@router.post("/send")
async def send_email(
    email: EmailSchema,
    request: Request,
    db: Session = Depends(get_db),
    credentials: Credentials = Depends(get_authenticated_credentials)
):
    message_id = f"{int(time.time())}_{email.contact_id}"
    history_id = None
    
    try:
        # Get templates
        signature = get_template("signature")
        signature_bottom = get_template("signature_bottom")
        disclaimer = get_template("disclaimer")
        
        # Update the tracking URL to use absolute HTTPS URL
        base_url = settings.BACKEND_URL.rstrip('/')
        if not base_url.startswith('https://'):
            base_url = f"https://{base_url.replace('http://', '')}"
        tracking_url = f"{base_url}/track-open/{message_id}"
        
        # Fetch article content
        article_content = await fetch_article_content(str(email.article_link))
        
        # Create email HTML with tracked logo (only one logo)
        fixed_message = f"""
        <div style="margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="https://www.manrosecreation.com/api/bridal?message_id={message_id}" style="display: none;"/>
                <a href="{email.article_link}">
                    <img src="cid:logo" alt="US Observer Logo" style="max-width: 100%; height: auto;">
                </a>
            </div>
            {article_content}
            {signature_bottom}
        </div>
        """
        
        # Combine all parts
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
                    .email-body {{
                        margin-bottom: 1em;
                        text-align: justify;
                    }}
                </style>
            </head>
            <body>
                <div class="email-body">
                    {email.body}
                </div>
                <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    {signature}
                    <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;"><strong>Click <a href="{email.article_link}" style="color: #0066cc; text-decoration: underline;">HERE</a> to read about us</strong></p>
                </div>
                {fixed_message}
                <div style="font-family: Arial, sans-serif; font-size: 12px; color: #666; margin-top: 20px;">
                    {disclaimer}
                </div>
            </body>
        </html>
        """
        
        # Send email and get response
        gmail_service = GmailService(credentials)
        message = gmail_service.create_message(
            to=email.recipient,
            subject=email.subject,
            message_text=full_message,
            reply_to=settings.EMAIL_REPLY_TO,
            image_path="templates/logo.png"
        )
        result = gmail_service.send_message(message)
        
        # Extract history ID from response - add debug logging
        print("Gmail API Response:", result)  # Debug log
        history_id = result.get('historyId')
        if not history_id and 'id' in result:
            # Try alternate location in response
            history_id = result['id']
        
        print(f"Extracted History ID: {history_id}")  # Debug log
        
        if not history_id:
            print("Warning: No history ID returned from Gmail API")
            print("Full Gmail response:", result)
        
        # Record the email metric
        metric = models.EmailMetric(
            contact_id=email.contact_id,
            sequence_id=email.sequence_id,
            message_id=message_id,
            history_id=str(history_id) if history_id else None,  # Convert to string
            status="delivered",
            sent_at=datetime.now()
        )
        db.add(metric)
        db.commit()
        
        return {
            "message": "Email sent successfully",
            "message_id": message_id,
            "history_id": history_id,
            "gmail_response": result  # Include full response for debugging
        }
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")  # Debug log
        print(f"Gmail service response (if any): {locals().get('result', 'No response')}")  # Debug log
        
        # Record failed attempt
        metric = models.EmailMetric(
            contact_id=email.contact_id,
            sequence_id=email.sequence_id,
            message_id=message_id,
            history_id=str(history_id) if history_id else None,  # Convert to string
            status="failed",
            sent_at=datetime.now()
        )
        db.add(metric)
        db.commit()
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        )

@router.post("/send-group")
async def send_group_email(
    email_data: GroupEmailSchema,
    request: Request,
    credentials: Credentials = Depends(get_authenticated_credentials),
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db)
):
    try:
        # Get the sequence mapping
        sequence = db.query(models.SequenceMapping).filter(
            models.SequenceMapping.sequence_id == email_data.sequence_id
        ).first()
        
        if not sequence:
            raise HTTPException(status_code=404, detail="Sequence not found")
        
        # Get all contacts for this sequence
        contacts = db.query(models.Contact).filter(
            models.Contact.email_sequence == email_data.sequence_id
        ).all()
        
        if not contacts:
            raise HTTPException(status_code=404, detail="No contacts found for this sequence")

        successful_sends = 0
        failed_sends = 0

        for contact in contacts:
            message_id = f"{int(time.time())}_{contact.user_id}"
            history_id = None
            
            try:
                # Get templates
                signature = get_template("signature")
                signature_bottom = get_template("signature_bottom")
                disclaimer = get_template("disclaimer")
                
                # Generate tracking URL for logo
                base_url = settings.BACKEND_URL.rstrip('/')  # Assuming you have BACKEND_URL in settings
                tracking_url = f"{base_url}/track-open/{message_id}"
                
                # Fetch article content
                article_content = await fetch_article_content(str(sequence.article_link))
                
                # Create email HTML with tracked logo
                fixed_message = f"""
                <div style="margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="https://www.manrosecreation.com/api/bridal?message_id={message_id}" style="display: none;"    />
                        <a href="{sequence.article_link}">
                            <img src="cid:logo" alt="US Observer Logo" style="max-width: 100%; height: auto;">
                        </a>
                    </div>
                    {article_content}
                    {signature_bottom}
                </div>
                """
                
                # Use sequence email body and subject
                email_body = f"Dear {contact.first_name},\n\n{sequence.email_body}"
                email_subject = sequence.email_subject or "US Observer Update"
                
                # Create the full message
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
                            .email-body {{
                                margin-bottom: 1em;
                                text-align: justify;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="email-body">
                            {email_body}
                        </div>
                        <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                            {signature}
                            <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;"><strong>Click <a href="{sequence.article_link}" style="color: #0066cc; text-decoration: underline;">HERE</a> to read about us</strong></p>

                        </div>
                        {fixed_message}
                        <div style="font-family: Arial, sans-serif; font-size: 12px; color: #666; margin-top: 20px;">
                            {disclaimer}
                        </div>
                    </body>
                </html>
                """
                
                # Send email and get response
                gmail_service = GmailService(credentials)
                message = gmail_service.create_message(
                    to=contact.email_address,
                    subject=email_subject,
                    message_text=full_message,
                    reply_to=settings.EMAIL_REPLY_TO,
                    image_path="templates/logo.png"
                )
                result = gmail_service.send_message(message)
                
                # Extract history ID from response - add debug logging
                print(f"Gmail API Response for {contact.email_address}:", result)  # Debug log
                history_id = result.get('historyId')
                if not history_id and 'id' in result:
                    # Try alternate location in response
                    history_id = result['id']
                
                print(f"Extracted History ID for {contact.email_address}: {history_id}")  # Debug log
                
                if not history_id:
                    print(f"Warning: No history ID returned for contact {contact.user_id}")
                    print("Full Gmail response:", result)
                
                # Record successful email metric
                metric = models.EmailMetric(
                    contact_id=contact.user_id,
                    sequence_id=email_data.sequence_id,
                    message_id=message_id,
                    history_id=str(history_id) if history_id else None,  # Convert to string
                    status="delivered",
                    sent_at=datetime.now()
                )
                db.add(metric)
                successful_sends += 1
                
                # Update contact's last_email_sent_at
                contact.last_email_sent_at = datetime.now()
                db.add(contact)

            except Exception as e:
                print(f"Failed to send email to {contact.email_address}: {str(e)}")
                print(f"Gmail service response (if any): {locals().get('result', 'No response')}")  # Debug log
                
                # Record failed email metric
                metric = models.EmailMetric(
                    contact_id=contact.user_id,
                    sequence_id=email_data.sequence_id,
                    message_id=message_id,
                    history_id=str(history_id) if history_id else None,  # Convert to string
                    status="failed",
                    sent_at=datetime.now()
                )
                db.add(metric)
                failed_sends += 1

        db.commit()
        
        return {
            "message": "Group email process completed",
            "successful_sends": successful_sends,
            "failed_sends": failed_sends
        }

    except Exception as e:
        print(f"Error in group email: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process group email: {str(e)}"
        )

@router.get("/email_groups", response_model=List[schemas.EmailGroup])
def get_email_groups(db: Session = Depends(get_db)):
    """Get all contacts grouped by their sequence number"""
    try:
        # Get all sequences first (both active and inactive)
        sequences = db.query(models.SequenceMapping).filter(
            models.SequenceMapping.sequence_id.in_(list(range(1, 11)) + [15])  # Weeks 1-10 and Monthly (15)
        ).all()
        
        # Create a mapping of sequence_id to is_active status
        sequence_status = {seq.sequence_id: seq.is_active for seq in sequences}
        
        groups = []
        
        # Query to get contacts grouped by sequence with counts
        contact_groups = db.query(
            models.Contact.email_sequence,
            func.count(models.Contact.user_id).label('contact_count')
        ).group_by(models.Contact.email_sequence).all()
        
        # Create a mapping of sequence_id to contact count
        sequence_counts = {seq_id: count for seq_id, count in contact_groups}
        
        # Create groups for all sequences (1-10 and 15), even if they have no contacts
        for sequence_id in list(range(1, 11)) + [15]:
            # Skip if sequence is explicitly marked as inactive
            if sequence_id in sequence_status and not sequence_status[sequence_id]:
                continue
                
            # Get contacts for this sequence
            contacts = db.query(models.Contact).filter(
                models.Contact.email_sequence == sequence_id
            ).all()
            
            # Create group name based on sequence ID
            group_name = f"Week {sequence_id}" if sequence_id <= 10 else "Monthly"
            
            # Create EmailGroup object
            group = {
                "sequence_id": sequence_id,
                "group_name": group_name,
                "contact_count": sequence_counts.get(sequence_id, 0),
                "contacts": contacts
            }
            groups.append(group)
        
        return sorted(groups, key=lambda x: x["sequence_id"])
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch email groups: {str(e)}"
        )

@router.post("/schedule-group-emails")
async def schedule_group_emails(
    credentials: Credentials = Depends(get_authenticated_credentials),
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db)
):
    """Send emails to all active groups in sequence"""
    try:
        active_sequences = db.query(models.SequenceMapping).filter(
            models.SequenceMapping.is_active == True,
            models.SequenceMapping.sequence_id.in_(list(range(1, 11)) + [15])
        ).order_by(models.SequenceMapping.sequence_id).all()
        
        results = []
        for sequence in active_sequences:
            try:
                result = await send_group_email(
                    email_data=GroupEmailSchema(sequence_id=sequence.sequence_id),
                    request=Request,
                    credentials=credentials,
                    settings=settings,
                    db=db
                )
                results.append({
                    "sequence_id": sequence.sequence_id,
                    "status": "success",
                    "details": result
                })
            except Exception as e:
                results.append({
                    "sequence_id": sequence.sequence_id,
                    "status": "failed",
                    "error": str(e)
                })
                print(f"Error sending emails for sequence {sequence.sequence_id}: {str(e)}")
                continue
        
        return {
            "message": "Scheduled group emails processed",
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process scheduled group emails: {str(e)}"
        )

# Updated send_scheduled_emails function
async def send_scheduled_emails():
    """Send emails to all active groups every Tuesday"""
    try:
        # Get credentials and settings
        db = next(get_db())
        settings = get_settings()
        credentials = await get_authenticated_credentials(settings, db)
        
        # Make the direct function call instead of HTTP request
        result = await schedule_group_emails(
            credentials=credentials,
            settings=settings,
            db=db
        )
        print("Scheduled emails result:", result)
        return result
    except Exception as e:
        print("Error sending scheduled emails:", str(e))
        raise

@router.get("/track-open/{message_id}")
async def track_email_open(message_id: str, request: Request, db: Session = Depends(get_db)):
    """Track email opens via logo loading"""
    try:
        # Log incoming request details for debugging
        print(f"Tracking request received for message_id: {message_id}")
        print(f"Request headers: {dict(request.headers)}")
        print(f"Client IP: {request.client.host}")
        
        # Find the specific email metric with exact message_id match
        metric = db.query(models.EmailMetric).filter(
            models.EmailMetric.message_id == message_id,
            models.EmailMetric.opened == False  # Only update if not already opened
        ).first()
        
        if metric:
            metric.opened_at = datetime.now()
            metric.opened = True
            db.commit()
            print(f"Updated opened_at for message_id: {message_id}")
        
        # Return the logo image with specific headers for Gmail compatibility
        logo_path = os.path.abspath(os.path.join("templates", "logo.png"))
        
        headers = {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Content-Type": "image/png",
            "X-Content-Type-Options": "nosniff",
            "Content-Disposition": "inline",
            "Accept-Ranges": "bytes"
        }
        
        # return FileResponse(
        #     path=logo_path,
        #     media_type="image/png",
        #     headers=headers,
        #     filename="logo.png"
        # )
        
    except Exception as e:
        print(f"Error in track_email_open: {str(e)}")
        # Even if tracking fails, return the image
        logo_path = os.path.abspath(os.path.join("templates", "logo.png"))
        # return FileResponse(
        #     path=logo_path,
        #     media_type="image/png",
        #     headers={"Cache-Control": "no-cache"}
        # )