import requests

from app.external_services.crawlers import constants
from app.core.config import settings
from app.external_services.logging_config import setup_logging


logger = setup_logging(__name__, log_file="icbc_login.py")


def get_auth_token():
    """Get authentication token."""
    try:
        response = requests.put(
            settings.ICBC_LOGIN_URL,
            headers=constants.LOGIN_HEADERS,
            json={
            'drvrLastName': settings.USER_LAST_NAME,
            'licenceNumber': settings.USER_LICENSE_NUMBER,
            'keyword': settings.USER_KEYWORD
        },
            timeout=10
        )
        response.raise_for_status()
        return response.headers.get('Authorization', None)
    except requests.RequestException as e:
        logger.error(f"Authentication failed: {e}")
        raise e
