import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from config import Config

logger = logging.getLogger(__name__)


class SendEmail:
    SENDER_EMAIL = Config.get_env_variable('SENDER_EMAIL')
    TO_EMAIL = Config.get_env_variable('TO_EMAIL')
    APP_PASSWORD = Config.get_env_variable('APP_PASSWORD')
    SUBJECT = 'ICBC Road Test Notification'

    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    def create_message(self, subject, message_text):
        """Create an email message."""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f'ICBC Road Test Notifier{self.SENDER_EMAIL}'
        msg['To'] = self.TO_EMAIL

        # Create the body of the message (HTML version).
        html_content = "<html><body><h2>ICBC Road Test Availability</h2><ul>"
        logger.info("Message content prepared for sending.")
        for location, dates in message_text.items():
            html_content += f"<li><strong>{location}</strong>:<ul>"
            for date_info in dates:
                html_content += f"<li>{date_info['date']} ({date_info['day_of_week']}) - {date_info['start_at']}</li>"
            html_content += "</ul></li>"
        html_content += "</ul></body></html>"

        # Attach HTML content
        part = MIMEText(html_content, 'html')
        msg.attach(part)
        return msg

    def send_message(self, message):
        """Send the email message using Gmail SMTP."""
        try:
            server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(self.SENDER_EMAIL, self.APP_PASSWORD)
            server.sendmail(self.SENDER_EMAIL, self.TO_EMAIL.split(', '), message.as_string())
            server.quit()
            logger.info("Email sent successfully!")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise e
