import logging
import os

class Logger:
    def __init__(self, project_name):
        self.project_name = project_name
        self.log_path = f"log/{self.project_name}.log"

        # Ensure the log directory exists
        os.makedirs("log", exist_ok=True)

        # Configure logging
        self.logger = logging.getLogger(self.project_name)
        self.logger.setLevel(logging.DEBUG)  # Capture all levels

        # Create a file handler
        file_handler = logging.FileHandler(self.log_path)
        file_handler.setLevel(logging.DEBUG)

        # Create a formatter
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        # Avoid duplicate handlers
        if not self.logger.hasHandlers():
            self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)
