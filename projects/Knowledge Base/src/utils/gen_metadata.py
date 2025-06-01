import os
import json
import argparse
from datetime import datetime
import logging
from typing import Dict, List, Any, Optional

# --- Configuration & Constants ---
# These can be moved to a config file or class if the app grows
DEFAULT_WEIGHT = 100
DEFAULT_DRAFT = False  # Using boolean False, which serializes to 'false' in JSON
DEFAULT_FEATURED_IMAGE = "/feature.jpg"

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Helper Functions ---

def get_file_timestamp(file_path: str) -> Optional[float]:
    """
    Retrieves the modification timestamp of a file.
    Falls back to creation timestamp if modification time is problematic (though typically mtime is preferred).
    """
    try:
        # Prioritize modification time as it's generally more consistent
        return os.path.getmtime(file_path)
    except OSError as e:
        logger.warning(f"Could not get modification time for {file_path}: {e}. Trying creation time.")
        try:
            return os.path.getctime(file_path)
        except OSError as e_create:
            logger.error(f"Could not get creation or modification time for {file_path}: {e_create}")
            return None

def format_timestamp_to_iso_date(timestamp: float) -> str:
    """
    Converts a Unix timestamp to an ISO 8601 date string (YYYY-MM-DD).
    """
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime('%Y-%m-%d')

def normalize_path_for_json(path: str) -> str:
    """
    Ensures the path uses forward slashes, as is common in web/JSON contexts.
    """
    return path.replace(os.sep, '/')

# --- Core Logic Functions ---

def create_file_json_object(
    absolute_file_path: str,
    base_directory_path: str
) -> Optional[Dict[str, Any]]:
    """
    Creates a JSON-like dictionary for a single file.

    Args:
        absolute_file_path (str): The absolute path to the file.
        base_directory_path (str): The absolute path to the base directory for relative path calculation.

    Returns:
        Optional[Dict[str, Any]]: A dictionary representing the file's JSON object,
                                   or None if essential data (like date) cannot be retrieved.
    """
    try:
        relative_path = os.path.relpath(absolute_file_path, base_directory_path)
        normalized_relative_path = normalize_path_for_json(relative_path)

        timestamp = get_file_timestamp(absolute_file_path)
        if timestamp is None:
            logger.warning(f"Skipping file {absolute_file_path} due to missing timestamp.")
            return None

        iso_date = format_timestamp_to_iso_date(timestamp)

        file_object = {
            "path": normalized_relative_path,
            "date": iso_date,
            "weight": DEFAULT_WEIGHT,
            "draft": DEFAULT_DRAFT,
            "featured_image": DEFAULT_FEATURED_IMAGE
        }
        return file_object
    except Exception as e:
        logger.error(f"Error processing file {absolute_file_path}: {e}")
        return None

def collect_file_data_recursively(base_directory_path: str) -> List[Dict[str, Any]]:
    """
    Recursively scans a directory and collects JSON objects for each file.

    Args:
        base_directory_path (str): The absolute path to the directory to scan.

    Returns:
        List[Dict[str, Any]]: A list of JSON-like dictionaries for all found files.
    """
    all_files_data: List[Dict[str, Any]] = []
    abs_base_dir = os.path.abspath(base_directory_path)

    if not os.path.isdir(abs_base_dir):
        logger.error(f"Base directory '{abs_base_dir}' does not exist or is not a directory.")
        return all_files_data

    for root, _, files in os.walk(abs_base_dir):
        for filename in files:
            absolute_file_path = os.path.join(root, filename)
            file_json_obj = create_file_json_object(absolute_file_path, abs_base_dir)
            if file_json_obj:
                all_files_data.append(file_json_obj)
    
    return all_files_data

def write_json_to_file(data: List[Dict[str, Any]], output_file_path: str) -> bool:
    """
    Writes a list of dictionaries to a JSON file.

    Args:
        data (List[Dict[str, Any]]): The data to write.
        output_file_path (str): The path to the output JSON file.

    Returns:
        bool: True if writing was successful, False otherwise.
    """
    abs_output_path = os.path.abspath(output_file_path)
    output_dir = os.path.dirname(abs_output_path)

    try:
        if output_dir: # Ensure output directory exists if specified
            os.makedirs(output_dir, exist_ok=True)

        with open(abs_output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"Successfully wrote JSON data to {abs_output_path}")
        return True
    except IOError as e:
        logger.error(f"Failed to write JSON to {abs_output_path}: {e}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred while writing JSON to {abs_output_path}: {e}")
        return False

# --- Argument Parsing and Main Execution ---

def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate a JSON list of file metadata from a directory."
    )
    parser.add_argument(
        "base_dir",
        type=str,
        help="The base directory to scan for files recursively."
    )
    parser.add_argument(
        "output_json_file",
        type=str,
        help="The path to the JSON file where the output will be saved."
    )
    return parser.parse_args()

def main():
    """
    Main function to orchestrate the script execution.
    """
    args = parse_arguments()

    base_directory = args.base_dir
    output_file = args.output_json_file

    logger.info(f"Starting file scan in base directory: {base_directory}")

    if not os.path.isdir(base_directory):
        logger.error(f"Error: The provided base directory '{base_directory}' does not exist or is not a directory.")
        return

    file_metadata_list = collect_file_data_recursively(base_directory)

    if file_metadata_list:
        logger.info(f"Collected metadata for {len(file_metadata_list)} files.")
        if write_json_to_file(file_metadata_list, output_file):
            logger.info("Process completed successfully.")
        else:
            logger.error("Process failed during JSON writing.")
    elif os.path.isdir(base_directory): # if base_directory exists but no files processed
        logger.info("No files found or processed in the specified directory. Writing an empty list.")
        if write_json_to_file([], output_file): # Write an empty list if no files
             logger.info("Empty JSON list written successfully.")
        else:
            logger.error("Process failed during JSON writing for empty list.")
    else:
        # This case should be caught earlier, but as a safeguard
        logger.warning("No file metadata collected.")


if __name__ == "__main__":
    main()
