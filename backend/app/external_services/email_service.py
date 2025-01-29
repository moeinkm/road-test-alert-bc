import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from app.core.config import settings

logger = logging.getLogger(__name__)


class SMTPGmailService:
    SMTP_SERVER = settings.SMTP_SERVER
    SMTP_PORT = settings.SMTP_PORT
    
    def __init__(self, app_password: str, sender_email: str, to_emails: str):
        """
        Initialize the SendEmail class with SMTP server connection and login.

        This method sets up an SMTP connection, upgrades it to a secure SSL/TLS connection,
        and logs in using the provided credentials.

        Parameters:
        app_password (str): The application-specific password for the sender's email account.
        sender_email (str): The email address of the sender.
        to_emails (str): A comma-separated string of recipient email addresses.
        """
        self.server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
        self.server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        self.server.login(sender_email, app_password)
        self.sender_email = sender_email
        self.to_emails = to_emails

    def create_message(self, subject, message, from_header, subtype='html'):
        """Create an email message."""
        msg = MIMEMultipart('alternative') # todo: what is subtype
        msg['Subject'] = subject
        msg['From'] = f'{from_header}{self.sender_email}'
        msg['To'] = self.to_emails

        # Attach content
        part = MIMEText(message, subtype)
        msg.attach(part)

        return msg

    def send_message(self, message):
        """Send the email message using Gmail SMTP."""
        try:
            self.server.sendmail(self.sender_email, self.to_emails.split(', '), message.as_string())
            logger.info("Email sent successfully!")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise e
    
    def close_connection(self):
        """Close the SMTP connection."""
        self.server.quit()