import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)  # Ensure the directory for logs exists


def setup_logging(name: str, log_file: str = "application.log", level=logging.INFO):
    """
    Sets up and returns a logger with a rotating file handler.

    :param name: The name of the logger (use __name__ to tie it to the module).
    :param log_file: The name of the log file where logs are saved.
    :param level: The threshold level of the logger (e.g., INFO, DEBUG).
    :return: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # File handler with rotation (5 MB per file, keeping 2 backup files)
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, log_file),
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=2
    )
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )

    # Stream handler (optional, for console output)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        logging.Formatter("%(levelname)s | %(message)s")
    )

    # Adding handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Avoid duplicate log entries
    logger.propagate = False

    return logger
