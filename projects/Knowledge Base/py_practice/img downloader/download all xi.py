# image_downloader.py

import logging
import os, sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, Tag

# --- Configuration ---
# Set up a logger for clear and informative output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- Core Logic (Single Responsibility Functions) ---

def fetch_html(url: str) -> Optional[str]:
    """
    Fetches the HTML content from a given URL.

    Responsibility: Network request for HTML content.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch HTML from {url}: {e}")
        return None

def extract_image_urls(html_content: str, css_class: str) -> List[str]:
    """
    Parses HTML and extracts image URLs matching a specific CSS class.

    Responsibility: HTML parsing and data extraction.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    image_tags = soup.select(f'img.{css_class.replace(" ", ".")}')
    image_urls = [tag['src'] for tag in image_tags if tag.has_attr('src')]

    if not image_urls:
        logging.warning(f"No images found with class '{css_class}' on the page.")
    else:
        logging.info(f"Found {len(image_urls)} matching images.")

    return image_urls

def download_image(image_url: str, destination_folder: str) -> None:
    """
    Downloads a single image to a specified folder.

    Responsibility: Network request for image data and file system writing.
    """
    try:
        # This function now expects a resolved, absolute path.
        os.makedirs(destination_folder, exist_ok=True)

        parsed_url = urlparse(image_url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            logging.warning(f"Could not determine filename for {image_url}. Skipping.")
            return

        filepath = os.path.join(destination_folder, filename)

        logging.info(f"Downloading {filename} to {destination_folder}...")

        response = requests.get(image_url, stream=True, timeout=30)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.info(f"Successfully saved {filepath}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download image {image_url}: {e}")
    except OSError as e:
        logging.error(f"Failed to save image to {destination_folder}: {e}")

# --- Orchestration (Combining Core Logic) ---

def process_webpage_task(target_dir: str, page_url: str) -> None:
    """
    Orchestrates the full process for a single webpage: fetch, parse, and download.
    This is the target function for our parallel execution.
    """
    logging.info(f"Processing task: URL='{page_url}' -> DIR='{target_dir}'")

    html = fetch_html(page_url)
    if not html:
        return

    image_urls = extract_image_urls(html, css_class="aligncenter size-full")
    if not image_urls:
        return

    logging.info(f"Starting sequential download of {len(image_urls)} images for {page_url}")
    for img_url in image_urls:
        download_image(img_url, target_dir)

def parse_input_file(filepath: str) -> List[Tuple[str, str]]:
    """
    Reads the input file and resolves directory paths gracefully.

    Responsibility: Input file reading, validation, and path resolution.
    """
    tasks = []
    try:
        with open(filepath, 'r') as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split()
                if len(parts) == 2:
                    raw_dir_path = parts[0]
                    # *** KEY IMPROVEMENT HERE ***
                    # 1. Expand `~` to the user's home directory.
                    expanded_path = os.path.expanduser(raw_dir_path)
                    # 2. Resolve it to an absolute path to handle relative paths like ../
                    resolved_path = os.path.abspath(expanded_path)

                    tasks.append((resolved_path, parts[1]))
                else:
                    logging.warning(f"Skipping malformed line {i}: '{line}'")
    except FileNotFoundError:
        logging.critical(f"Input file not found: {filepath}")
        return []

    return tasks

# --- Main Execution Block ---

def main():
    """
    Main function to parse arguments and manage the parallel processing pool.
    """
    parser = argparse.ArgumentParser(
        description="""
        Downloads specific images from webpages listed in a file.
        Each line in the file should contain: <directory_path> <webpage_url>
        """
    )
    parser.add_argument('input_file', help='Path to the input file containing a list of tasks.')
    parser.add_argument(
        '-w', '--workers',
        type=int,
        default=os.cpu_count() or 4,
        help='Number of parallel worker threads.'
    )
    args = parser.parse_args()

    tasks = parse_input_file(args.input_file)
    if not tasks:
        logging.info("No valid tasks to process. Exiting.")
        return

    logging.info(f"Found {len(tasks)} tasks. Starting processing with {args.workers} workers.")

    with ThreadPoolExecutor(max_workers=args.workers, thread_name_prefix='Worker') as executor:
        future_to_task = {
            executor.submit(process_webpage_task, dir_path, url): (dir_path, url)
            for dir_path, url in tasks
        }

        for future in as_completed(future_to_task):
            task_info = future_to_task[future]
            try:
                future.result()
                logging.info(f"Completed task for URL: {task_info[1]}")
            except Exception as e:
                logging.error(f"An unexpected error occurred processing task {task_info}: {e}")

    logging.info("All tasks have been processed.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print ("^C")
        sys.exit (0)
