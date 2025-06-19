# scripts/action_A.py
# This script's only job is to prepare the target directory and copy files.

import sys
import os
import shutil

# --- Configuration ---
TARGET_DIR = "/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/img/test/"
# ---------------------

def main(files_to_process):
    """
    Cleans the target directory and copies a given list of files into it.
    """
    print(f"  [Python] Preparing '{TARGET_DIR}' and copying {len(files_to_process)} files...")

    try:
        # 1. Clean the target directory
        if os.path.exists(TARGET_DIR):
            shutil.rmtree(TARGET_DIR)
        os.makedirs(TARGET_DIR)

        # 2. Copy the provided files over
        for file_path in files_to_process:
            if os.path.exists(file_path):
                shutil.copy(file_path, TARGET_DIR)
            else:
                # Log a warning but don't fail the whole script
                print(f"  [Python] WARNING: File {file_path} not found. Skipping.")

        print(f"  [Python] File copy successful.")

    except Exception as e:
        print(f"  [Python] ERROR: An error occurred during file operation: {e}")
        sys.exit(1) # Exit with a non-zero code to signal failure to Bash

if __name__ == "__main__":
    incoming_files = sys.argv[1:]
    if not incoming_files:
        print("  [Python] Error: This script requires file paths as arguments.")
        sys.exit(1)

    main(incoming_files)
