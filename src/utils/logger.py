# src/utils/logger.py
import logging

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set to INFO or DEBUG to see log messages

# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add formatter to ch
ch.setFormatter(formatter)

# Add ch to logger
logger.addHandler(ch)