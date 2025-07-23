import datetime
import logging
from collections import defaultdict
from typing import Dict, List, Tuple

import requests
from sqlalchemy.orm import Session

from app.external_services.availability_serializer import AvailabilitySerializer

from . import constants
from .icbc_login import get_auth_token
from app.core.config import settings
from app.models import Center

logger = logging.getLogger(__name__)
# todo: possible substitute pos_id and id
# todo: test this

def request_available_dates(center, auth_token):
    """
    Request available appointment dates for a given test center from the ICBC API.

    Args:
        center: An object representing the test center, expected to have at least a 'pos_id' and 'name' attribute.
        auth_token (str): The authentication token to be used in the request headers.

    Returns:
        dict or None: The JSON response from the ICBC API as a dictionary if the request is successful, otherwise None.

    Raises:
        Logs an error and returns None if the request fails due to a requests.RequestException.

    Example data returned:
        [
            {
                'appointmentDt': {'date': '2025-11-28', 'dayOfWeek': 'Friday'},
                'dlExam': {'code': '5-R-1', 'description': '5-R-ROAD'},
                'endTm': '15:30',
                'lemgMsgId': 35,
                'posId': 274,
                'resourceId': 21903,
                'signature': '...',
                'startTm': '14:55'
            }
        ]
    """
    available_appointments_data = {
        'aPosID': center.pos_id,
        'examType': '5-R-1',
        'examDate': datetime.date.today().isoformat(),
        'ignoreReserveTime': False,
        'prfDaysOfWeek': '[0,1,2,3,4,5,6]',
        'prfPartsOfDay': '[0,1]',
        'lastName': settings.USER_LAST_NAME,
        'licenseNumber': settings.USER_LICENSE_NUMBER,
    }

    headers = {
        **constants.LOGIN_HEADERS,
        'Authorization': auth_token,
    }
    try:
        response = requests.post(settings.ICBC_APPOINTMENT_URL, headers=headers, json=available_appointments_data)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve appointments for {center.name}: {center.pos_id}: {e}")
        return

    return response.json()


def find_available_dates(db: Session) -> Tuple[List, bool]:
    """Find available dates for appointments."""
    all_available_slots = []
    available_tomorrow_onwards = False
    auth_token = get_auth_token()
    if not auth_token:
        logger.error("Authorization failed; no available dates will be fetched.")
        raise

    for center in db.query(Center).all():
        appointments = request_available_dates(center=center, auth_token=auth_token)
        if not appointments:
            continue
        serializer = AvailabilitySerializer.with_centers(appointments, db)
        for item in serializer.root:
            if item.appointmentDt.date != datetime.datetime.now().date():
                available_tomorrow_onwards = True
            all_available_slots.append(item)

    return all_available_slots, available_tomorrow_onwards
