# main.py
import argparse
import logging, uuid
import os, sys, json
from dotenv import load_dotenv
from utils import setup_logger
from config import DEFAULT_BATCH_SIZE
import file_operations
import processing



load_dotenv ("/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/.env")
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



AWS_API_GW_API_KEY = os.getenv ("AWS_API_GW_API_KEY").strip ()
API_KEY = os.getenv("FIREWORKS_API_KEY").strip()


AWS_API_GW = "https://z8sw7kg1o2.execute-api.us-west-2.amazonaws.com/v1-initial/api/AI/logs"
API_URL = "https://api.fireworks.ai/inference/v1/chat/completions"
#API_URL = "https://webhook.site/c39f67cc-7bc7-46d1-ab68-dca68eba4dac"

# --- Application Configuration (Unchanged) ---
TOKENS_STORE_JSON_FILE_NAME = os.getenv("CLAUDE_TOKENS_STORE_JSON_FILE_NAME")
SESSION_ID = str (uuid.uuid4 ())
logger.info (f"SESSION ID: {SESSION_ID}")





def main():
    """Main function to run the SEO optimization script."""
    setup_logger()
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(
        description="Batch process files for SEO optimization using AI."
    )
    parser.add_argument(
        "file_list",
        type=str,
        help="Path to a text file containing a list of file paths to process."
    )
    parser.add_argument(
        "-k", "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=f"Number of files to process in parallel per batch. Default: {DEFAULT_BATCH_SIZE}"
    )
    args = parser.parse_args()
    
    logger.info("Starting SEO optimization process...")
    
    # 1. Get the list of file paths to process
    all_paths = file_operations.read_file_paths(args.file_list)
    if not all_paths:
        logger.warning("No file paths to process. Exiting.")
        return

    # 2. Create batches from the list of paths
    batch_size = args.batch_size
    batches = [all_paths[i:i + batch_size] for i in range(0, len(all_paths), batch_size)]
    logger.info(f"Total files: {len(all_paths)}. Batch size: {batch_size}. Number of batches: {len(batches)}.")

    # 3. Process each batch
    for i, batch in enumerate(batches, 1):
        logger.info(f"========== PROCESSING BATCH {i}/{len(batches)} ==========")
        processing.process_batch(batch)
        logger.info(f"========== FINISHED BATCH {i}/{len(batches)} ==========")

    logger.info("All batches have been processed. Script finished.")

if __name__ == "__main__":
    main()
