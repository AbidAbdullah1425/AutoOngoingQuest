import logging

# Basic Logger setup
LOGS = logging.getLogger("AutoAnimeBot")
LOGS.setLevel(logging.INFO)

# Console handler for logs
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

LOGS.addHandler(console_handler)

# For Telethon Logging
class TelethonLogger(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        LOGS.info(log_entry)
