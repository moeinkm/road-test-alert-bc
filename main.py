from __future__ import print_function
import datetime
import json

import requests
import base64
import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


CHECK_AVAILABILITY_INTERVAL = 15  # days


class SendEmail:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://mail.google.com/']
    SENDER_EMAIL = 'amphionize@gmail.com'
    TO_EMAIL = 'moein.kameli.mk@gmail.com'
    SUBJECT = 'First email sent by python'
    MSG = "I'm happy"
    USER_ID = 'me'
    TOKEN_PATH = 'token.json'

    def __init__(self):
        self.service = None

    def main(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(self.TOKEN_PATH, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())

        try:
            # Call the Gmail API
            self.service = build('gmail', 'v1', credentials=creds)
            results = self.service.users().labels().list(userId=self.USER_ID).execute()
            labels = results.get('labels', [])
            self.service.users()
            if not labels:
                print('No labels found.')
                return
            print('Labels:')
            for label in labels:
                print(label['name'])

        except HttpError as error:
            print(f'An error occurred: {error}')

    def create_message(self, sender=SENDER_EMAIL, to=TO_EMAIL, subject=SUBJECT, message_text=MSG):
        # Create the MIME message with HTML formatting
        message = MIMEMultipart('alternative')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        # Format the message in HTML
        html_content = "<html><body><h2>ICBC Road Test Availability</h2><ul>"
        for location, dates in message_text:
            html_content += f"<li><strong>{location}</strong>:<ul>"
            for date_info in dates:
                html_content += f"<li>{date_info['date']} ({date_info['day_of_week']}) - {date_info['start_at']}</li>"
            html_content += "</ul></li>"
        html_content += "</ul></body></html>"

        # Attach text and HTML parts
        message.attach(MIMEText(html_content, 'html'))
        raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
        return {
            'raw': raw_message.decode("utf-8")
        }

    def send_message(self, raw_decoded_message):
        try:
            executed_message = self.service.users().messages().send(
                userId=self.USER_ID,
                body=raw_decoded_message
            ).execute()
            print('Message Id: %s' % executed_message['id'])
            return executed_message
        except Exception as e:
            print('An error occurred: %s' % e)

        return None


class AvailabilityFinder:
    LOGIN_HEADERS = {
        'sec-ch-ua-platform': '"Windows"',
        'Cache-control': 'no-cache, no-store',
        'Referer': 'https://onlinebusiness.icbc.com/webdeas-ui/login;type=driver',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Expires': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
    }

    APOS_IDS = {
        'Port Coquitlam': 73,
        'Burnaby claim center': 274,
        'Burnaby driver licencing': 2,
        'Surrey claim center': 269,
        'Guilford Broadwalk road test center': 11,
        'Surrey Driver Licencing': 281,
        'Newton claim center': 271,
        'North Vancouver driver licencing': 8,
        'Richmond driver licensing ': 93,
        'Vancouver driver licensing': 9,
        'Langley driver licensing': 153,
        'Maple Ridge claim centre': 279,
        'Langley claim centre': 270,
        'Abbotsford driver licensing': 1,
        'Chilliwack driver licensingv': 3,
    }

    def __init__(self):
        self.do_email = False
        self.login_json_data = {
            'drvrLastName': 'Kameli',
            'licenceNumber': '30298989',
            'keyword': 'Fatemeh',
        }

        self.available_appointments_headers = {
            'sec-ch-ua-platform': '"Windows"',
            'Authorization': self.get_auth_token(),
            'Referer': 'https://onlinebusiness.icbc.com/webdeas-ui/booking',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
        }

        self.available_dates_result = {
            'Port Coquitlam': [],
            'Burnaby claim center': [],
            'Burnaby driver licencing': [],
            'Surrey claim center': [],
            'Guilford Broadwalk road test center': [],
            'Surrey Driver Licencing': [],
            'Newton claim center': [],
            'North Vancouver driver licencing': [],
            'Richmond driver licensing ': [],
            'Vancouver driver licensing': [],
            'Langley driver licensing': [],
            'Maple Ridge claim centre': [],
            'Langley claim centre': [],
            'Abbotsford driver licensing': [],
            'Chilliwack driver licensing': []
        }

    def get_auth_token(self):
        response = requests.put(
            'https://onlinebusiness.icbc.com/deas-api/v1/webLogin/webLogin',
            headers=self.LOGIN_HEADERS,
            json=self.login_json_data
        )
        return response.headers['Authorization']

    def find_available_dates(self):
        for center_name, apos_id in self.APOS_IDS.items():
            available_appointments_json_data = {
                'aPosID': apos_id,
                'examType': '5-R-1',
                'examDate': '2024-10-25',
                'ignoreReserveTime': False,
                'prfDaysOfWeek': '[0,1,2,3,4,5,6]',
                'prfPartsOfDay': '[0,1]',
                'lastName': 'KAMELI',
                'licenseNumber': '30298989',
            }

            response = requests.post(
                'https://onlinebusiness.icbc.com/deas-api/v1/web/getAvailableAppointments',
                headers=self.available_appointments_headers,
                json=available_appointments_json_data,
            )
            print(response)
            for item in response.json():
                if item.get('appointmentDt', dict()).get('date'):
                    date = datetime.datetime.strptime(item.get('appointmentDt', dict()).get('date'), "%Y-%m-%d").date()
                    if date - datetime.timedelta(CHECK_AVAILABILITY_INTERVAL) < datetime.datetime.now().date():
                        self.do_email = True
                        print(item)
                        self.available_dates_result[center_name].append({
                            'date': item.get('appointmentDt').get('date'),
                            'day_of_week': item.get('appointmentDt').get('dayOfWeek'),
                            'start_at': item.get('startTm'),
                    })


availability_finder = AvailabilityFinder()
availability_finder.find_available_dates()

if availability_finder.do_email:
    gmail_service = SendEmail()
    gmail_service.main()
    raw_decoded_message = gmail_service.create_message(
        subject="ICBC road test available dates",
        message_text=json.dumps(availability_finder.available_dates_result)
    )
    gmail_service.send_message(raw_decoded_message)

