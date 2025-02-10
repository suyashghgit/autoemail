from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

class GmailService:
    def __init__(self, credentials):
        self.service = build('gmail', 'v1', credentials=credentials)

    def create_message(self, to: str, subject: str, message_text: str):
        message = MIMEMultipart('alternative')
        message['to'] = to
        message['subject'] = subject

        # Create both plain text and HTML versions
        text_part = MIMEText(self.strip_html(message_text), 'plain')
        html_part = MIMEText(message_text, 'html')

        # Add both parts to the message
        message.attach(text_part)
        message.attach(html_part)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw_message}

    def strip_html(self, html_content: str) -> str:
        """Convert HTML content to plain text for fallback"""
        # This is a simple implementation - you might want to use a proper HTML parser
        import re
        text = re.sub('<[^<]+?>', '', html_content)
        return text

    def send_message(self, message: dict, user_id: str = "me"):
        try:
            sent_message = self.service.users().messages().send(
                userId=user_id, body=message).execute()
            return sent_message
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}") 