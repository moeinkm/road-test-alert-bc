import datetime
import json
import os
import requests

class AvailabilityFinder:
    def __init__(self, icbc_api_endpoint, login_headers, apos_ids):
        self.icbc_api_endpoint = icbc_api_endpoint
        self.login_headers = login_headers
        self.apos_ids = apos_ids

    def get_auth_token(self):
        response = requests.put(
            self.icbc_api_endpoint + '/webLogin/webLogin',
            headers=self.login_headers,
            json={'drvrLastName': 'sample', 'licenceNumber': 'sample', 'keyword': 'sample'}
        )
        return response.headers['Authorization']

    def find_available_dates(self):
        available_dates_result = {}
        for center_name, apos_id in self.apos_ids.items():
            available_appointments_json_data = {
                'aPosID': apos_id,
                'examType': '5-R-1',
                'examDate': '2024-10-25',
                'ignoreReserveTime': False,
                'prfDaysOfWeek': '[0,1,2,3,4,5,6]',
                'prfPartsOfDay': '[0,1]',
                'lastName': 'sample',
                'licenseNumber': '30298989',
            }

            response = requests.post(
                self.icbc_api_endpoint + '/web/getAvailableAppointments',
                headers={'Authorization': self.get_auth_token()},
                json=available_appointments_json_data,
            )
            available_dates = []
            for item in response.json():
                if item.get('appointmentDt', dict()).get('date'):
                    date = datetime.datetime.strptime(item.get('appointmentDt', dict()).get('date'), "%Y-%m-%d").date()
                    if date - datetime.timedelta(15) < datetime.datetime.now().date():
                        available_dates.append({
                            'date': item.get('appointmentDt').get('date'),
                            'day_of_week': item.get('appointmentDt').get('dayOfWeek'),
                            'start_at': item.get('startTm'),
                        })
            available_dates_result[center_name] = available_dates
        return available_dates_result