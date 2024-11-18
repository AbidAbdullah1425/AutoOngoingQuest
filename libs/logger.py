import logging
from logging.handlers import RotatingFileHandler

# Set up the logger
LOGS = logging.getLogger("AutoAnimeBot")
LOGS.setLevel(logging.INFO)

# Create a console handler and set the log level to INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a file handler that logs to a file and rotates the log files after 1 MB
file_handler = RotatingFileHandler("bot.log", maxBytes=1 * 1024 * 1024, backupCount=5)
file_handler.setLevel(logging.INFO)

# Create a log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add the handlers to the logger
LOGS.addHandler(console_handler)
LOGS.addHandler(file_handler)
