from fastapi import APIRouter, Request, HTTPException, Depends
from app.schemas import EmailSchema
from app.services import GmailService
from app.dependencies import get_credentials
import os
import httpx
from bs4 import BeautifulSoup

router = APIRouter(prefix="/email", tags=["email"])

def get_template(template_name):
    template_path = os.path.join("app", "templates", f"{template_name}.txt")
    with open(template_path, "r") as file:
        return file.read()

async def fetch_article_content(url: str) -> str:
    """Fetch and extract the main content from the article URL"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Could not fetch article content")
        
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
        return "<p>Article content could not be extracted</p>"

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