# -*- coding: utf-8 -*-
import json
import os
import sys
import logging
import argparse
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, NoReturn

# --- Constants ---
LOG_FILE_NAME: str = "deserializer.log"
BACKUP_DIR_NAME: str = "backup" # Name of the centralized backup directory
EXPECTED_KEYS: set[str] = {"file", "content"}

# --- Custom Exception (Optional but can be useful) ---
class DeserializationError(Exception):
    """Custom exception for errors during the deserialization process."""
    path: Optional[Path] = None # Optional path context

    def __init__(self, message: str, path: Optional[Path] = None):
        super().__init__(message)
        self.path = path

class PathValidationError(DeserializationError):
    """Specific error for path validation failures."""
    pass

class FileOperationError(DeserializationError):
    """Specific error for file operation failures (backup, write, dir creation)."""
    pass


# --- Logging Setup ---
def setup_logging(log_level: int = logging.INFO) -> None:
    """
    Configures logging to output to both console and a file.

    Console logs WARNING level and above.
    File logs INFO level and above to LOG_FILE_NAME in the CWD.

    Args:
        log_level: The minimum logging level for the root logger (e.g., logging.INFO, logging.DEBUG).
    """
    log_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    log_file_path = Path.cwd() / LOG_FILE_NAME

    file_handler: Optional[logging.FileHandler] = None
    try:
        # Ensure log directory exists if LOG_FILE_NAME includes path separators
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(logging.INFO)
    except OSError as e:
        print(f"Warning: Could not open log file {log_file_path}: {e}. File logging disabled.", file=sys.stderr)

    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.WARNING)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    if file_handler:
        root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.info("="*20 + " Script Start " + "="*20)
    if file_handler:
        logging.info(f"Logging initialized. Log file: {log_file_path}")
    else:
        logging.warning("File logging is disabled due to an error opening the log file.")

# --- Argument Parsing ---
def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments for the script.

    Returns:
        An argparse.Namespace object containing the parsed arguments (json_file, base_dir).
    """
    parser = argparse.ArgumentParser(
        description="Deserializes a JSON file (list of {file, content} objects) into multiple files relative to a base directory, storing backups in a central 'backup' subdirectory."
    )
    parser.add_argument(
        "json_file",
        type=str,
        help="Path to the input JSON file."
    )
    parser.add_argument(
        "--base-dir",
        type=str,
        default=None,
        help="Base directory where files will be created. If not provided, the current working directory (PWD) is used. A 'backup' subdirectory will be created here if needed."
    )
    return parser.parse_args()

# --- Path and Directory Operations ---
def resolve_base_directory(base_dir_arg: Optional[str]) -> Path:
    """
    Determines and validates the base directory for file operations.

    Args:
        base_dir_arg: The path string provided via command line, or None.

    Returns:
        A resolved, absolute Path object for the base directory.

    Raises:
        SystemExit: If the specified base directory is invalid or not a directory.
        OSError: If there's a permission error checking the directory status.
    """
    try:
        if base_dir_arg:
            base_directory = Path(base_dir_arg).resolve()
            logging.info(f"Using specified base directory: {base_directory}")
            if not base_directory.is_dir():
                logging.critical(f"Error: Specified base directory '{base_dir_arg}' (resolved to '{base_directory}') does not exist or is not a directory.")
                sys.exit(1)
        else:
            base_directory = Path.cwd().resolve()
            logging.info(f"No base directory specified, using current working directory: {base_directory}")
        # Check write permissions in base directory early? Might be complex due to subdirs.
        # For now, rely on errors during operations.
        return base_directory
    except OSError as e:
        logging.critical(f"Error accessing base directory '{base_dir_arg or 'PWD'}': {e}")
        sys.exit(1)
    except Exception as e:
         logging.critical(f"Unexpected error resolving base directory '{base_dir_arg or 'PWD'}': {e}")
         sys.exit(1)


def validate_and_resolve_target_path(relative_path_str: str, base_dir: Path) -> Path:
    """
    Validates a relative file path string and resolves it against the base directory.

    Ensures the path is relative, does not contain disallowed components,
    and resolves to a location *within* the base directory (but not the backup dir itself).

    Args:
        relative_path_str: The file path string from the JSON object.
        base_dir: The resolved absolute base directory Path object.

    Returns:
        The resolved, absolute Path object for the target file.

    Raises:
        PathValidationError: If the path string is invalid, empty, absolute,
                             resolves outside the base directory, or targets the backup directory.
        OSError: If an OS-level error occurs during path resolution (e.g., permissions).
    """
    if not isinstance(relative_path_str, str) or not relative_path_str.strip():
        raise PathValidationError(f"Path string is empty or not a string: '{relative_path_str}'")

    try:
        if Path(relative_path_str).is_absolute():
             raise PathValidationError(f"Path specified in JSON ('{relative_path_str}') must be relative.")

        potential_path = base_dir / relative_path_str
        resolved_path = potential_path.resolve() # Can raise OSError

        resolved_base_dir = base_dir.resolve()
        resolved_backup_root = (base_dir / BACKUP_DIR_NAME).resolve()

        # Security Check 1: Within base directory
        if resolved_base_dir != resolved_path and resolved_base_dir not in resolved_path.parents:
            raise PathValidationError(
                f"Path '{relative_path_str}' resolves outside the base directory '{base_dir}'. "
                f"Resolved path: '{resolved_path}'"
            )

        # Security Check 2: Not directly *within* the backup directory
        if resolved_backup_root == resolved_path or resolved_backup_root in resolved_path.parents:
             raise PathValidationError(
                 f"Path '{relative_path_str}' attempts to write directly into the reserved backup directory '{resolved_backup_root}'. "
                 f"Resolved path: '{resolved_path}'"
             )

        # Security Check 3: Prevent writing directly to the base directory itself (e.g. if path was ".")
        if resolved_path == resolved_base_dir:
             if not Path(relative_path_str).name or Path(relative_path_str).name == '.':
                raise PathValidationError(f"Path resolves to the base directory itself, which is not allowed for file writing: '{relative_path_str}'")

        logging.debug(f"Path resolved: '{relative_path_str}' -> '{resolved_path}'")
        return resolved_path

    except (ValueError, TypeError) as e:
        raise PathValidationError(f"Invalid characters or format in path string '{relative_path_str}': {e}") from e
    # Let OSError propagate upwards if raised by resolve()


def create_directories_for_file(target_file_path: Path) -> None:
    """
    Creates parent directories for the target file path if they don't exist.

    Args:
        target_file_path: The absolute Path object for the file to be written.

    Raises:
        FileOperationError: If a path component exists but is not a directory.
        OSError: If directory creation fails due to permissions or other OS issues.
    """
    target_dir = target_file_path.parent
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        if not target_dir.is_dir():
             # Check after attempting creation, protects against edge cases/races
             raise FileOperationError(f"Path '{target_dir}' exists but is not a directory after attempting creation.", target_dir)
        logging.info(f"Ensured directory exists: {target_dir}")
    except OSError as e:
        raise FileOperationError(f"Failed to create or access directory '{target_dir}': {e}", target_dir) from e
    except Exception as e:
        raise FileOperationError(f"Unexpected error preparing directory '{target_dir}': {e}", target_dir) from e


def backup_existing_file(target_path: Path, base_dir: Path) -> None:
    """
    Creates a backup of an existing file before overwriting.

    Backs up the file to a mirrored path within the base_dir/backup directory.
    If the target path exists but is not a file (e.g., a directory), it raises an error.
    If the target path does not exist, this function does nothing.

    Args:
        target_path: The absolute Path object of the potential file to be backed up.
        base_dir: The absolute base directory, used to calculate relative backup path.

    Raises:
        FileOperationError: If the path exists but is a directory, or if backup directory
                            creation or the move operation fails.
        OSError: Underlying OS errors during file operations.
        ValueError: If target_path is not within base_dir (should not happen if validation is correct).
    """
    try:
        if target_path.is_file(): # Check if it's specifically a file first
            # Calculate relative path from base_dir
            try:
                relative_path = target_path.relative_to(base_dir)
            except ValueError as e:
                 # This indicates target_path is not under base_dir, which shouldn't happen
                 # after validate_and_resolve_target_path, but good to catch defensively.
                 logging.error(f"Internal Error: Cannot determine relative path for backup. Target '{target_path}' may not be under base '{base_dir}'.")
                 raise FileOperationError(f"Cannot backup: Target path '{target_path}' not relative to base '{base_dir}'.", target_path) from e

            backup_root = base_dir / BACKUP_DIR_NAME
            backup_path = backup_root / relative_path
            backup_dir = backup_path.parent

            logging.warning(f"Overwriting existing file: '{target_path}'. Attempting backup to '{backup_path}'")

            # --- Backup Step 1: Ensure backup directory structure exists ---
            try:
                backup_dir.mkdir(parents=True, exist_ok=True)
                if not backup_dir.is_dir(): # Verify after creation attempt
                    raise FileOperationError(f"Backup path component '{backup_dir}' exists but is not a directory after attempting creation.", backup_dir)
                logging.info(f"Ensured backup directory exists: {backup_dir}")
            except OSError as e:
                 raise FileOperationError(f"Failed to create or access backup directory '{backup_dir}': {e}. Halting overwrite.", backup_dir) from e

            # --- Backup Step 2: Remove old backup if it exists at the destination ---
            # This is less critical now as we move, not copy, but good practice if logic changes
            try:
                if backup_path.exists():
                    logging.warning(f"Pre-existing backup file found at '{backup_path}'. Removing it.")
                    backup_path.unlink() # Can raise OSError
            except OSError as e:
                raise FileOperationError(f"Failed to remove existing file at backup location '{backup_path}': {e}. Halting overwrite.", backup_path) from e

            # --- Backup Step 3: Move the current file to the backup location ---
            try:
                shutil.move(str(target_path), str(backup_path))
                logging.info(f"Backup successful: '{target_path}' -> '{backup_path}'")
            except OSError as e:
                raise FileOperationError(f"Failed to move original file '{target_path}' to backup location '{backup_path}': {e}. Halting overwrite.", target_path) from e
            except Exception as e:
                 raise FileOperationError(f"Unexpected error backing up '{target_path}' to '{backup_path}': {e}", target_path) from e

        elif target_path.exists(): # Path exists but is not a file
            # Could be a directory, symlink, etc. Error out.
             raise FileOperationError(f"Cannot overwrite. Path '{target_path}' exists but is not a regular file.", target_path)

        # else: path does not exist, no backup needed.

    except OSError as e:
        # Catch OSErrors from initial exists(), is_file() checks
        raise FileOperationError(f"Error checking status of target path '{target_path}' for backup: {e}", target_path) from e


def write_content_to_file(target_path: Path, content: str) -> None:
    """
    Writes the provided content to the target file path using UTF-8 encoding.

    Args:
        target_path: The absolute Path object of the file to write.
        content: The string content to write to the file.

    Raises:
        FileOperationError: If writing fails due to OS errors, encoding errors etc.
        OSError: Underlying OS errors during file write.
    """
    try:
        target_path.write_text(content, encoding='utf-8')
        logging.info(f"Successfully wrote file: {target_path}")
    except OSError as e:
        raise FileOperationError(f"Failed to write file '{target_path}': {e}", target_path) from e
    except Exception as e:
        raise FileOperationError(f"An unexpected error occurred writing file '{target_path}': {e}", target_path) from e


# --- JSON Processing ---
def load_and_validate_json_data(json_file_path: Path) -> List[Dict[str, str]]:
    """
    Loads JSON data, validates its root structure and item format.

    Ensures the data is a list of dictionaries, each having exactly
    'file' (string) and 'content' (string) keys with non-empty 'file' values.

    Args:
        json_file_path: The Path object of the input JSON file.

    Returns:
        The validated list of dictionaries.

    Raises:
        FileNotFoundError: If the json_file_path does not exist.
        DeserializationError: If JSON is invalid, structure is wrong, or types are incorrect.
        OSError: If the file cannot be read due to OS-level issues.
    """
    try:
        logging.info(f"Reading JSON file: {json_file_path}")
        raw_data = json.loads(json_file_path.read_text(encoding='utf-8'))
    except FileNotFoundError:
        logging.critical(f"Input JSON file not found: {json_file_path}")
        raise
    except json.JSONDecodeError as e:
        raise DeserializationError(f"Invalid JSON format in '{json_file_path}': {e}") from e
    except OSError as e:
        raise DeserializationError(f"Could not read JSON file '{json_file_path}': {e}") from e
    except Exception as e:
         raise DeserializationError(f"Unexpected error loading JSON from '{json_file_path}': {e}") from e

    if not isinstance(raw_data, list):
        raise DeserializationError("Validation Error: Input JSON's root element is not a list.")

    validated_items: List[Dict[str, str]] = []
    for index, item in enumerate(raw_data):
        item_label = f"item at index {index}"
        if not isinstance(item, dict):
            raise DeserializationError(f"Validation Error: {item_label} is not a dictionary.")

        current_keys = set(item.keys())
        if current_keys != EXPECTED_KEYS:
            missing = EXPECTED_KEYS - current_keys
            extra = current_keys - EXPECTED_KEYS
            error_msg = f"Validation Error: {item_label} has incorrect keys."
            if missing: error_msg += f" Missing: {sorted(list(missing))}."
            if extra: error_msg += f" Extra: {sorted(list(extra))}."
            raise DeserializationError(error_msg)

        file_path_str = item.get("file")
        content = item.get("content")

        if not isinstance(file_path_str, str):
             raise DeserializationError(f"Validation Error: {item_label} 'file' value is not a string (type: {type(file_path_str).__name__}).")
        if not file_path_str.strip():
            raise DeserializationError(f"Validation Error: {item_label} 'file' value is an empty or whitespace-only string.")

        if not isinstance(content, str):
            raise DeserializationError(f"Validation Error: {item_label} 'content' value is not a string (type: {type(content).__name__}).")

        validated_items.append({"file": file_path_str, "content": content})

    logging.info(f"JSON structure validation passed for {len(validated_items)} items.")
    return validated_items


# --- Core Processing Logic ---
def process_single_item(item: Dict[str, str], base_dir: Path, item_index: int) -> bool:
    """
    Processes a single item from the validated JSON list.

    Handles path validation/resolution, directory creation, backup (to central dir),
    and file writing. Uses try/except to catch errors during these steps.

    Args:
        item: A dictionary containing 'file' (relative path string) and 'content' (string).
        base_dir: The absolute, resolved base directory Path.
        item_index: The index of the item in the original list (for logging).

    Returns:
        True if the item was processed successfully, False otherwise.
    """
    relative_path_str = item["file"]
    content = item["content"]
    item_label = f"item {item_index} ('{relative_path_str}')"
    logging.debug(f"Processing {item_label}...")
    target_path: Optional[Path] = None # Keep track for error context

    try:
        # 1. Validate and resolve the path against the base directory
        target_path = validate_and_resolve_target_path(relative_path_str, base_dir)

        # 2. Ensure parent directories exist for the *target* file
        create_directories_for_file(target_path)

        # 3. Handle backup if the file already exists (needs base_dir now)
        backup_existing_file(target_path, base_dir)

        # 4. Write the actual file content
        write_content_to_file(target_path, content)

        return True

    except (PathValidationError, FileOperationError, OSError) as e:
        path_context = ""
        # Try to get path from exception attribute first, fallback to target_path if set
        err_path = getattr(e, 'path', None) or getattr(e, 'filename', None) or target_path
        if err_path:
            path_context = f" (related path: '{err_path}')"

        logging.error(f"Failed to process {item_label}: {e}{path_context}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error processing {item_label}: {e}", exc_info=True)
        return False


# --- Main Orchestration ---
def main() -> None:
    """
    Main function to orchestrate the deserialization process.
    """
    setup_logging()
    args = parse_arguments()
    base_directory: Optional[Path] = None

    try:
        base_directory = resolve_base_directory(args.base_dir)
        json_file_path = Path(args.json_file)
        validated_data = load_and_validate_json_data(json_file_path)

        if not validated_data:
            logging.warning("Input JSON file contains an empty list. No files to create.")
            sys.exit(0)

        success_count = 0
        failure_count = 0
        total_items = len(validated_data)
        logging.info(f"Starting processing of {total_items} items relative to base directory '{base_directory}'...")
        logging.info(f"Backups (if needed) will be placed in: '{base_directory / BACKUP_DIR_NAME}'")

        for index, item in enumerate(validated_data):
            if process_single_item(item, base_directory, index):
                success_count += 1
            else:
                failure_count += 1

        logging.info("-" * 20 + " Processing Complete " + "-" * 20)
        logging.info(f"Summary: {success_count} out of {total_items} items processed successfully.")
        if failure_count > 0:
            logging.warning(f"{failure_count} items failed. Please review logs above for details.")
            sys.exit(1)
        else:
            logging.info("All items processed successfully.")
            sys.exit(0)

    except (FileNotFoundError, DeserializationError, OSError) as e:
        logging.critical(f"Critical error during setup or JSON loading: {e}")
        sys.exit(1)
    except SystemExit as e:
         sys.exit(e.code)
    except Exception as e:
        logging.critical(f"An unexpected critical error occurred: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
