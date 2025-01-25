import os
import datetime
import logging
import requests
from config import Config

from app.core.config import settings

logger = logging.getLogger(__name__)


class AvailabilityFinder:
    LOGIN_URL = 'https://onlinebusiness.icbc.com/deas-api/v1/webLogin/webLogin'
    APPOINTMENT_URL = 'https://onlinebusiness.icbc.com/deas-api/v1/web/getAvailableAppointments'

    def __init__(self):
        config = Config.load()
        self.APOS_IDS = config.get("APOS_IDS", {})
        self.LOGIN_HEADERS = config.get("LOGIN_HEADERS", {})
        self.login_data = {
            'drvrLastName': settings.USER_LAST_NAME,
            'licenceNumber': settings.USER_LICENSE_NUMBER,
            'keyword': settings.USER_KEYWORD
        }
        self.available_dates_result = {center: [] for center in self.APOS_IDS.keys()}
        self.do_email = False

    def get_auth_token(self):
        """Get authentication token."""
        try:
            response = requests.put(
                self.LOGIN_URL,
                headers=self.LOGIN_HEADERS,
                json=self.login_data,
                timeout=10
            )
            response.raise_for_status()
            return response.headers.get('Authorization', None)
        except requests.RequestException as e:
            logger.error(f"Authentication failed: {e}")
            raise e

    def find_available_dates(self):
        """Find available dates for appointments."""
        auth_token = self.get_auth_token()
        if not auth_token:
            logger.error("Authorization failed; no available dates will be fetched.")
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
                                datetime.datetime.now().date() + datetime.timedelta(
                                    days=settings.CHECK_AVAILABILITY_INTERVAL
                                )
                        ):
                            if date != datetime.datetime.now().date():
                                self.do_email = True
                            self.available_dates_result[center_name].append({
                                'date': appointment_date,
                                'day_of_week': item['appointmentDt'].get('dayOfWeek'),
                                'start_at': item.get('startTm')
                            })
            except requests.RequestException as e:
                logger.error(f"Failed to retrieve appointments for {center_name}: {e}")
                raise e
