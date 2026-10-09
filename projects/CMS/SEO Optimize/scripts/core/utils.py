# utils.py
import logging
import sys

def setup_logger():
    """Configures a basic logger to print to the console."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
