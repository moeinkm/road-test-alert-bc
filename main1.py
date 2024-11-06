from availaility_finder1 import AvailabilityFinder
from email_service1 import SendEmail
from logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Step 1: Find available dates
    availability_finder = AvailabilityFinder()
    availability_finder.find_available_dates()

    # Step 2: Send an email if there are available dates
    if availability_finder.do_email:
        gmail_service = SendEmail()
        gmail_service.initialize_service()
        message = gmail_service.create_message(
            subject="ICBC road test available dates",
            message_text=availability_finder.available_dates_result
        )
        gmail_service.send_message(message)
    else:
        logger.info("No available dates found.")
