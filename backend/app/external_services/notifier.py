from app.external_services.availability_finder import AvailabilityFinder

from app.core.config import settings
from app.external_services.email_service import SMTPGmailService
from logging_config import setup_logging
import logging
# todo: import structure

setup_logging()
logger = logging.getLogger(__name__)


def main():
    # Step 1: Find available dates
    availability_finder = AvailabilityFinder()
    availability_finder.find_available_dates()

    # Step 2: Send an email if there are available dates
    if availability_finder.do_email:
        gmail_service = SMTPGmailService(
            app_password=settings.APP_PASSWORD,
            sender_email=settings.SENDER_EMAIL,
            to_emails=settings.TO_EMAILS
        )
        prepared_message = prepare_message(availability_finder.available_dates_result)
        message = gmail_service.create_message(
            subject=settings.MAIL_SUBJECT,
            message=prepared_message,
            from_header = settings.FROM_HEADER
        )
        gmail_service.send_message(message)
        gmail_service.close_connection()
    else:
        logger.info("No available dates found.")


def prepare_message(available_dates_result): # todo: improve html UI
    # Create the body of the message (HTML version).
    html_content = "<html><body><h2>ICBC Road Test Availability</h2><ul>"
    for location, dates in available_dates_result.items():
        html_content += f"<li><strong>{location}</strong>:<ul>"
        for date_info in dates:
            html_content += f"<li>{date_info['date']} ({date_info['day_of_week']}) - {date_info['start_at']}</li>"
        html_content += "</ul></li>"
    html_content += "</ul></body></html>"

    logger.info("Message content prepared for sending.")

    return html_content


if __name__ == "__main__":
    main()
