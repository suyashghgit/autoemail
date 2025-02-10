from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

class GmailService:
    def __init__(self, credentials):
        self.service = build('gmail', 'v1', credentials=credentials)

    def create_message(self, to: str, subject: str, message_text: str):
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject

        msg = MIMEText(message_text)
        message.attach(msg)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw_message}

    def send_message(self, message: dict, user_id: str = "me"):
        try:
            sent_message = self.service.users().messages().send(
                userId=user_id, body=message).execute()
            return sent_message
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}") 