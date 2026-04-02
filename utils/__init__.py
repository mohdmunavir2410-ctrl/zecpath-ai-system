import logging
import os

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/zecpath_ai.log"), # Saves to a file
        logging.StreamHandler() # Also shows in your terminal
    ]
)

logger = logging.getLogger("ZecpathAI")
logger.info("Logging System Initialized.")