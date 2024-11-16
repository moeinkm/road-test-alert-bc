import os
import base64
import logging
from abc import ABC, abstractmethod
from email.mime.text import MIMEText

import boto3
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from config import Config


logger = logging.getLogger(__name__)


class BaseTokenHandler(ABC):
    CREDENTIALS_PATH = None
    TOKEN_PATH = None

    @abstractmethod
    def load_credentials(self):
        pass

    @abstractmethod
    def save_token(self, creds):
        pass


class LocalTokenHandler(BaseTokenHandler):
    CREDENTIALS_PATH = 'credentials.json'
    TOKEN_PATH = 'token.json'

    def load_credentials(self):
        if os.path.exists(self.TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(self.TOKEN_PATH, ['https://www.googleapis.com/auth/gmail.send'])
            return creds
        return None

    def save_token(self, creds):
        with open(self.TOKEN_PATH, 'w') as token_file:
            token_file.write(creds.to_json())


class LambdaTokenHandler(BaseTokenHandler):
    CREDENTIALS_PATH = '/tmp/credentials.json'
    TOKEN_PATH = '/tmp/token.json'

    def __init__(self):
        super().__init__()
        self.s3 = boto3.client('s3')
        self.bucket_name = Config.get_env_variable('TOKEN_BUCKET')
        self.credentials_key = Config.get_env_variable('CREDENTIALS_KEY', 'credentials.json')
        self.token_key = Config.get_env_variable('TOKEN_KEY', 'token.json')

    def load_credentials(self):
        # Download credentials.json from S3
        if not self.download_from_s3(self.credentials_key, self.CREDENTIALS_PATH):
            logger.error("Unable to download credentials.json from S3. Cannot proceed.")
            return None

        # Load token if available
        if self.download_from_s3(self.token_key, self.TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(self.TOKEN_PATH, ['https://www.googleapis.com/auth/gmail.send'])
            return creds
        return None

    def save_token(self, creds):
        with open(self.TOKEN_PATH, 'w') as token_file:
            token_file.write(creds.to_json())
        self.upload_to_s3(self.TOKEN_PATH, self.token_key)

    def download_from_s3(self, s3_key, local_path):
        try:
            self.s3.download_file(self.bucket_name, s3_key, local_path)
            return True
        except Exception as e:
            logger.error(f"Error downloading {s3_key} from S3: {e}")
            return False

    def upload_to_s3(self, local_path, s3_key):
        try:
            self.s3.upload_file(local_path, self.bucket_name, s3_key)
        except Exception as e:
            logger.error(f"Error uploading {local_path} to S3 as {s3_key}: {e}")


def get_token_handler():
    env = Config.get_env_variable('ENVIRONMENT', 'lambda')
    if env == 'local':
        logger.info("Initializing LocalTokenHandler.")
        return LocalTokenHandler()
    logger.info("Initializing LambdaTokenHandler.")
    return LambdaTokenHandler()


class SendEmail:
    SCOPES = [Config.get_env_variable('GMAIL_SCOPES')]
    SENDER_EMAIL = Config.get_env_variable('SENDER_EMAIL')
    TO_EMAIL = Config.get_env_variable('TO_EMAIL')
    SUBJECT = 'ICBC Road Test Notification'

    def __init__(self):
        self.token_handler = get_token_handler()
        self.service = None

    def initialize_service(self):
        """Initialize the Gmail service."""
        creds = self.token_handler.load_credentials()

        # Refresh token if expired or run OAuth flow if no valid token exists
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            logger.info("Token refreshed successfully.")
        elif not creds:
            # Run OAuth flow for local environment only
            if isinstance(self.token_handler, LocalTokenHandler):
                flow = InstalledAppFlow.from_client_secrets_file(self.token_handler.CREDENTIALS_PATH, self.SCOPES)
                creds = flow.run_local_server(port=0)
                logger.info("New token obtained successfully.")
            else:
                logger.error("No valid credentials found. Ensure the refresh token is initialized manually.")
                raise ValueError("Unable to obtain valid credentials. Initialization failed.")

        # Save the updated credentials
        self.token_handler.save_token(creds)

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
