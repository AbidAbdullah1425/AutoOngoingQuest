import logging

LOGS = logging.getLogger("AutoAnimeBot")
LOGS.setLevel(logging.INFO)

# Console Handler for logs
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

LOGS.addHandler(console_handler)
