from contextlib import contextmanager

from app.crud.crud_lead import get_lead_preference_to_filter_for_email
from app.db.session import db_session_as_context
from app.external_services.availability_finder import AvailabilityFinder

from app.core.config import settings
from app.external_services.email_service import SMTPGmailService
from logging_config import setup_logging
import logging
# todo: import structure
# todo: write test for this file. Test if dates are inclusive
# todo: refactor this file to send email asynchronous

setup_logging()
logger = logging.getLogger(__name__)


def main():
    # Step 1: Find available dates
    availability_finder = AvailabilityFinder()
    availability_finder.find_available_dates()

    with db_session_as_context() as session:
        lead_preferences = get_lead_preference_to_filter_for_email(session)

    full_availability = availability_finder.available_dates_result

    for lead_preference in lead_preferences:
        lead_email = lead_preference.get("email")
        if not lead_email:
            logger.warning(f"Skipping lead without email: {lead_preference}")
            continue

        # Filter availability based on lead's preferences
        filtered_availability = filter_availability_by_preferences(full_availability, lead)

        if not filtered_availability:
            logger.info(f"No matching availability for lead: {lead_email}")
            continue

        # Step 3: Email the filtered availability to the lead
        try:
            logger.info(f"Sending email to lead: {lead_email}")
        # Step 2: Send an email if there are available dates
        gmail_service = SMTPGmailService(
            app_password=settings.APP_PASSWORD,
            sender_email=settings.SENDER_EMAIL,
            to_emails=settings.TO_EMAILS
        )
        prepared_message = prepare_message(filtered_availability)
        message = gmail_service.create_message(
            subject=settings.MAIL_SUBJECT,
            message=prepared_message,
            from_header = settings.FROM_HEADER
        )
        gmail_service.send_message(message)
        gmail_service.close_connection()
    else:
        logger.info("No available dates found.")


def filter_availability_by_preferences(availability, preferences):
    """
    Filters the availability data based on a lead's preferences, including their date interval.

    :param availability: Full availability data (dict).
    :param preferences: Lead's filtering criteria (dict, e.g., preferred locations, start_date, end_date).
    :return: Filtered availability data (dict).
    """
    filtered_availability = {}

    # Extract filtering criteria from preferences
    preferred_locations = preferences.get("preferred_locations", [])
    start_date = preferences.get("start_date")  # Expected to be in ISO format
    end_date = preferences.get("end_date")  # Expected to be in ISO format

    for location, available_slots in availability.items():
        # Check if the location matches the lead's preferences
        if location in preferred_locations or not preferred_locations:
            filtered_slots = []
            for slot in available_slots:
                # Ensure slot date falls within the preferred date interval
                if start_date <= slot['date'] <= end_date:
                    filtered_slots.append(slot)

            if filtered_slots:
                filtered_availability[location] = filtered_slots

    return filtered_availability



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
