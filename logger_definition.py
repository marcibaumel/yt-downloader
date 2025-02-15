import logging
import colorlog
from logging.handlers import RotatingFileHandler

# Define log format and colors for console
log_colors = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red'
}

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    log_colors=log_colors
)

# Create a logger
logger = logging.getLogger("yt_downloader")
logger.setLevel(logging.DEBUG)

# Console handler (with colors)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# File handler (without colors)
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = RotatingFileHandler("app.log", maxBytes=5*1024*1024, backupCount=3)  # 5MB max size
file_handler.setFormatter(file_formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
