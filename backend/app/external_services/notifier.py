from collections import defaultdict
from typing import Any, List, Dict, DefaultDict

from sqlalchemy import Row
from sqlalchemy.engine import Row
from app.crud.crud_lead import get_lead_preferences
from app.db.session import db_session_as_context
from app.core.config import settings
from app.external_services.crawlers.availability_finder import find_available_dates
from .email_service import SMTPGmailService
from .logging_config import setup_logging

# todo: implement tommorrow_onwards logic

logger = setup_logging(__name__, log_file="notifier.log")



def match_availability_to_users(availability_data: List, lead_preference: Row) -> DefaultDict[str, List]:
    """
    Match available appointment slots to a single user's preferences based on their criteria.

    This function filters available appointment slots for one user based on their
    preferred test centers, days of the week, and date range.

    Args:
        availability_data (List): A list of availability items, each with a center object attached.
            Each item should have attributes: posId, appointmentDt (with date and dayOfWeek.value), 
            center (Center object), and other appointment details.
        lead_preference (Row): A SQLAlchemy Row object containing user preferences.
            Should have attributes: email, preferred_centers_ids (List[int]), 
            preferred_days (List[int]), start_date (date), and end_date (date).

    Returns:
        DefaultDict[str, List]: A defaultdict mapping Center.name to lists of matching 
            appointment slots for the user. Empty defaultdict if no matches found.
    """
    user_centers = lead_preference.preference.preferred_centers
    user_days = lead_preference.preference.preferred_days
    user_start_date = lead_preference.preference.start_date
    user_end_date = lead_preference.preference.end_date
    
    # Filter availability for this user
    matching_slots = defaultdict(list)
    for item in availability_data:
        # Check if slot matches user preferences
        if (
            item.center is not None and
            any(item.center.pos_id == c.pos_id for c in user_centers) and
            item.appointmentDt.dayOfWeek.value in user_days and
            user_start_date <= item.appointmentDt.date <= user_end_date
        ):  # inclusive dates
            matching_slots[item.center.name].append(item)

    return matching_slots


def prepare_message(available_slots: DefaultDict[str, List]) -> str:
    """
    Prepare HTML email message from available appointment slots.
    
    Args:
        available_slots (DefaultDict[Center, List]): A defaultdict mapping Center objects to lists of 
            appointment slot objects. Each slot should have attributes: appointmentDt (with date 
            and dayOfWeek), startTm, endTm, and other appointment details.
    
    Returns:
        str: HTML formatted message content for email.
    """
    # Create the body of the message (HTML version).
    html_content = "<html><body><h2>ICBC Road Test Availability</h2><ul>"
    
    for center_name, slots in available_slots.items():
        if slots:  # Only show centers with available slots
            html_content += f"<li><strong>{center_name}</strong>:<ul>"
            for slot in slots:
                # Access attributes from the Pydantic model objects
                date_str = slot.appointmentDt.date.strftime('%Y-%m-%d')
                day_of_week = slot.appointmentDt.dayOfWeek.name.title()
                start_time = slot.startTm
                end_time = slot.endTm
                
                html_content += f"<li>{date_str} ({day_of_week}) - {start_time} to {end_time}</li>"
            html_content += "</ul></li>"
    
    html_content += "</ul></body></html>"

    logger.info("Message content prepared for sending.")

    return html_content


def notify_lead_by_preference(lead_preferences: List[Row], full_availability: List, gmail_service: SMTPGmailService):
    for lead_preference in lead_preferences:
        lead_email = lead_preference.get("email")

        matched_availability = match_availability_to_users(full_availability, lead_preference)

        if not matched_availability:
            logger.info(f"No matching availability for user: {lead_email}")
            return

        try:
            logger.info(f"Sending email to user: {lead_email}")
            prepared_message = prepare_message(matched_availability)
            message = gmail_service.create_message(
                subject=settings.MAIL_SUBJECT,
                message=prepared_message,
                from_header=settings.FROM_HEADER
            )
            gmail_service.send_message(message)
            logger.info(f"Message sent to user: {lead_email}")
        except Exception as e:
            logger.error(f"Error sending email to {lead_email}: {str(e)}")


def main():
    try:
        with db_session_as_context() as db:
            availability_result = find_available_dates(db)
        
        if not availability_result:
            logger.error("Error getting availability.")
            return
        
        full_availability, available_tomorrow_onwards = availability_result
        if not full_availability:
            logger.info("No available dates found.")
            return

        with db_session_as_context() as session:
            lead_preferences = get_lead_preferences(session)

        gmail_service = SMTPGmailService(
            app_password=settings.APP_PASSWORD,
            sender_email=settings.SENDER_EMAIL,
            to_emails=settings.TO_EMAILS
        )

        try:
            notify_lead_by_preference(lead_preferences, full_availability, gmail_service)
        except Exception as e:
            logger.error(f"Error processing leads: {str(e)}")
        finally:
            gmail_service.close_connection()
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
