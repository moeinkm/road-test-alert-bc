from __future__ import print_function
import datetime
import json
import requests
import base64
import os
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

CHECK_AVAILABILITY_INTERVAL = 15  # days


class SendEmail:
    SCOPES = ['https://mail.google.com/']
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    TO_EMAIL = os.getenv('TO_EMAIL')
    SUBJECT = 'ICBC Road Test Notification'
    TOKEN_PATH = 'token.json'
    CREDENTIALS_PATH = 'credentials.json'

    def __init__(self):
        self.service = None

    def initialize_service(self):
        """Initialize the Gmail service, handling authentication and token management securely."""
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
        """Create an email message with proper encoding."""
        # Format the message in HTML
        html_content = "<html><body><h2>ICBC Road Test Availability</h2><ul>"
        print(message_text)
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
        """Send the email message securely and handle potential errors."""
        try:
            sent_message = self.service.users().messages().send(
                userId='me', body=message
            ).execute()
            print('Message sent. ID: %s' % sent_message['id'])
        except HttpError as error:
            print(f'Failed to send message: {error}')


class AvailabilityFinder:
    LOGIN_URL = 'https://onlinebusiness.icbc.com/deas-api/v1/webLogin/webLogin'
    APPOINTMENT_URL = 'https://onlinebusiness.icbc.com/deas-api/v1/web/getAvailableAppointments'

    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
        self.APOS_IDS = config.get("APOS_IDS", {})
        self.LOGIN_HEADERS = config.get("LOGIN_HEADERS", {})
        self.do_email = False
        self.available_dates_result = {center: [] for center in self.APOS_IDS.keys()}
        self.login_data = {
            'drvrLastName': os.getenv('USER_LAST_NAME'),
            'licenceNumber': os.getenv('USER_LICENSE_NUMBER'),
            'keyword': os.getenv('USER_KEYWORD')
        }

    @staticmethod
    def load_env_data():
        """Load sensitive data from environment variables securely."""
        return {
            'last_name': os.getenv('USER_LAST_NAME'),
            'license_number': os.getenv('USER_LICENSE_NUMBER'),
            'keyword': os.getenv('USER_KEYWORD')
        }

    def get_auth_token(self):
        """Authenticate and retrieve an authorization token securely."""
        try:
            response = requests.put(
                self.LOGIN_URL,
                headers=self.LOGIN_HEADERS,
                json=self.login_data,
                timeout=10
            )
            response.raise_for_status()  # Ensure we handle HTTP errors
            return response.headers.get('Authorization', None)
        except requests.RequestException as e:
            print(f"Authentication failed: {e}")
            return None

    def find_available_dates(self):
        """Check available dates and prepare results if appointments are found."""
        auth_token = self.get_auth_token()
        if not auth_token:
            print("Authorization failed; no available dates will be fetched.")
            return

        for center_name, apos_id in self.APOS_IDS.items():
            available_appointments_data = {
                'aPosID': apos_id,
                'examType': '5-R-1',
                'examDate': datetime.date.today().isoformat(),
                'ignoreReserveTime': False,
                'prfDaysOfWeek': '[0,1,2,3,4,5,6]',
                'prfPartsOfDay': '[0,1]',
                'lastName': self.login_data['drvrLastName'],
                'licenseNumber': self.login_data['licenceNumber'],
            }

            headers = {
                **self.LOGIN_HEADERS,
                'Authorization': auth_token,
            }

            try:
                response = requests.post(self.APPOINTMENT_URL, headers=headers, json=available_appointments_data)
                response.raise_for_status()
                appointments = response.json()

                for item in appointments:
                    appointment_date = item.get('appointmentDt', {}).get('date')
                    if appointment_date:
                        date = datetime.datetime.strptime(appointment_date, "%Y-%m-%d").date()
                        if date < (
                                datetime.datetime.now().date() + datetime.timedelta(days=CHECK_AVAILABILITY_INTERVAL)):
                            self.do_email = True
                            self.available_dates_result[center_name].append({
                                'date': appointment_date,
                                'day_of_week': item['appointmentDt'].get('dayOfWeek'),
                                'start_at': item.get('startTm')
                            })
            except requests.RequestException as e:
                print(f"Failed to retrieve appointments for {center_name}: {e}")


if __name__ == "__main__":
    availability_finder = AvailabilityFinder()
    availability_finder.find_available_dates()

    if availability_finder.do_email:
        gmail_service = SendEmail()
        gmail_service.initialize_service()
        message = gmail_service.create_message(
            subject="ICBC road test available dates",
            message_text=availability_finder.available_dates_result
        )
        gmail_service.send_message(message)