import os
import base64
import logging
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from config import Config


logger = logging.getLogger(__name__)


class SendEmail:
    SCOPES = ['https://mail.google.com/']
    SENDER_EMAIL = Config.get_env_variable('SENDER_EMAIL')
    TO_EMAIL = Config.get_env_variable('TO_EMAIL')
    SUBJECT = 'ICBC Road Test Notification'
    TOKEN_PATH = Config.get_env_variable('TOKEN_PATH')
    CREDENTIALS_PATH = Config.get_env_variable('CREDENTIALS_PATH')

    def __init__(self):
        self.service = None

    def initialize_service(self):
        """Initialize the Gmail service."""
        creds = None
        if os.path.exists(self.TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(self.TOKEN_PATH, self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.CREDENTIALS_PATH, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())

        self.service = build('gmail', 'v1', credentials=creds)

    def create_message(self, subject, message_text):
        """Create an email message."""
        html_content = "<html><body><h2>ICBC Road Test Availability</h2><ul>"
        logger.info("Message content prepared for sending.")
        for location, dates in message_text.items():
            html_content += f"<li><strong>{location}</strong>:<ul>"
            for date_info in dates:
                html_content += f"<li>{date_info['date']} ({date_info['day_of_week']}) - {date_info['start_at']}</li>"
            html_content += "</ul></li>"
        html_content += "</ul></body></html>"

        message = MIMEText(html_content, 'html')
        message['to'] = self.TO_EMAIL
        message['from'] = self.SENDER_EMAIL
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
        return {
            'raw': raw_message.decode("utf-8")
        }

    def send_message(self, message):
        """Send the email message."""
        try:
            sent_message = self.service.users().messages().send(
                userId='me', body=message
            ).execute()
            logger.info(f'Message sent. ID: {sent_message["id"]}')
        except HttpError as e:
            logger.error(f'Failed to send message: {e}')
            raise e
