import logging


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,  # Change this to logging.DEBUG for more detailed logs
        handlers=[
            logging.StreamHandler()  # Log to console
        ]
    )