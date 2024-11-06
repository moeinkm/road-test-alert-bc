import base64
import json
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

class EmailService:
    def __init__(self, sender_email, to_email, subject):
        self.sender_email = sender_email
        self.to_email = to_email
        self.subject = subject
        self.service = None

    def authenticate(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', ['https://mail.google.com/']
                )
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)

    def create_message(self, message_text):
        message = MIMEText(message_text)
        message['to'] = self.to_email
        message['from'] = self.sender_email
        message['subject'] = self.subject
        raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
        return {'raw': raw_message.decode("utf-8")}

    def send_message(self, raw_decoded_message):
        try:
            executed_message = self.service.users().messages().send(
                userId='me',
                body=raw_decoded_message
            ).execute()
            print('Message Id: %s' % executed_message['id'])
            return executed_message
        except Exception as e:
            print('An error occurred: %s' % e)