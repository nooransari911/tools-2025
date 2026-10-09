# file_operations.py
import os
import shutil
import logging

logger = logging.getLogger(__name__)

def read_file_paths(list_file_path: str) -> list[str] | None:
    """Reads a list of file paths from a given text file."""
    try:
        with open(list_file_path, 'r', encoding='utf-8') as f:
            paths = [line.strip() for line in f if line.strip()]
        logger.info(f"Found {len(paths)} file paths in '{list_file_path}'.")
        return paths
    except FileNotFoundError:
        logger.error(f"Input file not found: '{list_file_path}'")
        return None

def read_file_content(file_path: str) -> str | None:
    """Reads the entire content of a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Content file not found: '{file_path}'")
        return None
    except Exception as e:
        logger.error(f"Error reading content from '{file_path}': {e}")
        return None

def backup_original_file(file_path: str) -> bool:
    """Renames the original file to create a backup."""
    if not os.path.exists(file_path):
        logger.error(f"Cannot backup, file does not exist: '{file_path}'")
        return False
    
    try:
        base, ext = os.path.splitext(file_path)
        backup_path = f"{base} original{ext}"
        
        # To avoid accidentally overwriting a previous backup
        if os.path.exists(backup_path):
            logger.warning(f"Backup file '{backup_path}' already exists. Overwriting.")
        
        shutil.move(file_path, backup_path)
        logger.info(f"Original file backed up to '{backup_path}'")
        return True
    except Exception as e:
        logger.error(f"Failed to backup file '{file_path}': {e}")
        return False

def write_new_content(file_path: str, content: str) -> bool:
    """Writes new content to the specified file path."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"New content successfully written to '{file_path}'")
        return True
    except Exception as e:
        logger.error(f"Failed to write new content to '{file_path}': {e}")
        return False
