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
                print(f"Failed to fetch content. Status code: {response.status_code}")
                return f"""
                <div class='blog-content'>
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
                        
                        # Create new container
                        container = soup.new_tag('div')
                        container['class'] = 'image-container'
                        container['style'] = (
                            "border: 1px solid #ddd; "
                            "padding: 4px; "
                            "margin: 10px 0; "
                            "display: inline-block; "
                            "max-width: 100%; "
                            "box-sizing: border-box; "
                            "float: left; "
                            "margin-right: 15px; "
                            "margin-bottom: 10px;"
                        )
                        
                        # Add styling to image
                        img['style'] = "max-width: 100%; height: auto; display: block; margin: 0;"
                        
                        # Wrap image in container
                        img.wrap(container)
                        
                        # Look specifically for WordPress caption
                        caption = img.find_next('p', class_='wp-caption-text')
                        if not caption:
                            # Also look for caption by ID if class not found
                            caption = img.find_next('p', id=lambda x: x and 'caption-attachment' in x)
                        
                        if caption:
                            # Create new caption div inside container
                            caption_div = soup.new_tag('div')
                            caption_div['style'] = "margin: 5px 0 0 0; text-align: center; font-style: italic;"
                            caption_div.string = caption.get_text()
                            container.append(caption_div)
                            caption.decompose()  # Remove original caption
                    
                    except Exception as img_error:
                        print(f"Error processing image: {str(img_error)}")
                        continue
                
                # Add clearfix at the end of content
                clear_div = soup.new_tag('div')
                clear_div['style'] = "clear: both;"
                article_content.append(clear_div)
                
                # Preserve all original classes and styles
                return f"""
                <div class="article-container" style="max-width: 100%; margin: 0 auto; overflow: hidden;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="cid:logo" alt="US Observer Logo" style="max-width: 100%; height: auto;">
                    </div>
                    {str(article_content)}
                </div>
                """
            else:
                print("No article content found with any selector")  # Debug log
                return f"""
                <div class='blog-content'>
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="cid:logo" alt="US Observer Logo" style="max-width: 100%; height: auto;">
                    </div>
                    <p>Unable to extract the article content. Please visit 
                    <a href="{url}">the article page</a> directly to read the full content.</p>
                </div>
                """
    except Exception as e:
        print(f"Error fetching article content: {str(e)}")
        print(f"Error type: {type(e)}")  # Additional error info
        print(f"Error details: {e.__dict__}")  # More error details if available
        return f"""
        <div class='blog-content'>
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="cid:logo" alt="US Observer Logo" style="max-width: 100%; height: auto;">
            </div>
            <p>The article content is temporarily unavailable (Error: {str(e)}). Please visit 
            <a href="{url}">the article page</a> directly to read the full content.</p>
        </div>
        """

@router.post("/send")
async def send_email(
    email: EmailSchema,
    request: Request,
    db: Session = Depends(get_db),
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
        
        # The email body is now HTML from ReactQuill
        email_body = email.body  # No need to wrap in div, it's already HTML
        
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
                    .email-body {{
                        margin-bottom: 1em;
                    }}
                </style>
            </head>
            <body>
                <div class="email-body">
                    {email_body}
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
        
        # Record the email metric - UPDATED
        metric = models.EmailMetric(
            contact_id=email.contact_id,
            sequence_id=email.sequence_id,
            message_id=result.get("id"),
            status="delivered",
            sent_at=datetime.now()
        )
        db.add(metric)
        db.commit()
        
        return {"message": "Email sent successfully", "message_id": result.get("id")}
    except FileNotFoundError as e:
        print(f"File error: {str(e)}")
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        # Record failed attempt - UPDATED
        if 'email' in locals():
            metric = models.EmailMetric(
                contact_id=email.contact_id,
                sequence_id=email.sequence_id,
                message_id=None,
                status="failed",
                sent_at=datetime.now()
            )
            db.add(metric)
            db.commit()
        
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
        print(f"Received request for sequence_id: {group_email.sequence_id}")
        
        # Get sequence mapping data
        sequence_mapping = db.query(models.SequenceMapping).filter(
            models.SequenceMapping.sequence_id == group_email.sequence_id
        ).first()
        
        if not sequence_mapping:
            raise HTTPException(
                status_code=404,
                detail=f"No sequence mapping found for sequence_id: {group_email.sequence_id}"
            )

        # Handle null or empty article_link
        article_link = sequence_mapping.article_link or ""
        if article_link and not article_link.startswith(('http://', 'https://')):
            article_link = f'https://{article_link}'
        
        # Track results
        results = {
            "successful": [],
            "failed": []
        }

        # Get all contacts
        contacts = db.query(models.Contact).filter(
            models.Contact.email_sequence == group_email.sequence_id
        ).all()
        
        if not contacts:
            raise HTTPException(
                status_code=404,
                detail=f"No contacts found in sequence {group_email.sequence_id}"
            )

        # Update group_email with sequence mapping data
        group_email.body = sequence_mapping.email_body
        
        # Send email to each contact
        for contact in contacts:
            try:
                # Create EmailSchema for each contact
                email = EmailSchema(
                    recipient=contact.email_address,
                    subject=group_email.subject,
                    body=f"Dear {contact.first_name},\n\n{group_email.body}",
                    article_link=article_link,
                    contact_id=contact.user_id,
                    sequence_id=group_email.sequence_id
                )
                
                # Use the existing send_email function
                result = await send_email(email, request, db, credentials)
                
                # Update last_email_sent_at
                contact.last_email_sent_at = datetime.now()
                db.commit()
                
                results["successful"].append({
                    "email": contact.email_address,
                    "message_id": result["message_id"]
                })
                
            except Exception as e:
                print(f"Failed to send email to {contact.email_address}: {str(e)}")
                results["failed"].append({
                    "email": contact.email_address,
                    "error": str(e)
                })

        return {
            "message": f"Completed sending group emails for sequence {group_email.sequence_id}",
            "total_contacts": len(contacts),
            "successful_sends": len(results["successful"]),
            "failed_sends": len(results["failed"]),
            "details": results
        }

    except Exception as e:
        print(f"Global error: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send group emails: {str(e)}"
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