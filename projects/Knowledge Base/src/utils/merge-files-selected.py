#!/usr/bin/env python3

import sys
import os
import shutil
import argparse
import datetime

# --- Configuration ---
BACKUP_SUFFIX = ".bak"
HEADER_FORMAT = "======== {file_path} ========\n"
SEPARATOR = "\n\n"

def create_backup(file_path):
    """Attempts to create a backup of the given file."""
    backup_path = file_path + BACKUP_SUFFIX
    try:
        # copy2 preserves more metadata than copy
        shutil.copy2(file_path, backup_path)
        print(f"Info: Backup of previous version created at '{backup_path}'")
        return True
    except Exception as e:
        print(f"Warning: Failed to create backup for '{file_path}'. Error: {e}", file=sys.stderr)
        return False

def process_file(file_path, output_handle):
    """Reads a single file and appends its content to the output."""
    try:
        # Try reading as UTF-8, replace errors to avoid crashing on weird bytes
        with open(file_path, 'r', encoding='utf-8', errors='replace') as infile:
            output_handle.write(HEADER_FORMAT.format(file_path=file_path))
            shutil.copyfileobj(infile, output_handle) # Efficiently copies content
            output_handle.write(SEPARATOR)
            return True
    except IOError as e:
        print(f"Warning: Failed to read file '{file_path}'. Error: {e}. Skipping.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Warning: An unexpected error occurred while processing '{file_path}'. Error: {e}. Skipping.", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Combine selected files and/or contents of directories into a single output file.",
        epilog="Example: ./combine_files.py combined_docs.md src/ common/README.md utils.js"
    )
    parser.add_argument("output_file", help="Path to the output file.")
    parser.add_argument(
        "input_items",
        nargs='+', # Requires at least one input item
        help="One or more input files or directories to process."
    )

    args = parser.parse_args()

    output_file = args.output_file
    input_items = args.input_items
    backup_created = False
    output_existed = False

    # --- Backup Logic ---
    if os.path.exists(output_file):
        output_existed = True
        if os.path.isfile(output_file):
            print(f"Info: Output file '{output_file}' exists.")
            backup_created = create_backup(output_file)
        else:
            print(f"Error: Output path '{output_file}' exists but is not a regular file. Cannot proceed.", file=sys.stderr)
            sys.exit(1)

    # --- Prepare and Open Output File ---
    processed_count = 0
    try:
        # Open in write mode ('w'), specify UTF-8 encoding
        with open(output_file, 'w', encoding='utf-8') as outfile:
            if output_existed:
                 if backup_created:
                    print(f"Info: Overwriting '{output_file}' with combined content...")
                 else:
                    print(f"Info: Overwriting '{output_file}' (backup failed or skipped)...")
            else:
                print(f"Info: Creating new file '{output_file}' with combined content...")

            print("Starting combination process...")

            # --- Processing Input Items ---
            for item in input_items:
                if os.path.isfile(item):
                    print(f"Processing file: {item}")
                    if process_file(item, outfile):
                        processed_count += 1
                elif os.path.isdir(item):
                    print(f"Processing directory: {item}")
                    # Walk through the directory recursively
                    for root, _, files in os.walk(item):
                        for filename in files:
                            file_path = os.path.join(root, filename)
                            print(f"  Adding file: {file_path}")
                            if process_file(file_path, outfile):
                                processed_count += 1
                else:
                    print(f"Warning: Input '{item}' is not a valid file or directory. Skipping.", file=sys.stderr)

            # --- Final Feedback ---
            print("----------------------------------------")
            print(f"Done. Processed {processed_count} files.")
            print(f"Combined file created/updated at '{output_file}'.")
            if backup_created:
                print(f"Previous version backed up to '{output_file}{BACKUP_SUFFIX}'.")
            print("----------------------------------------")

    except IOError as e:
        print(f"\nError: Cannot write to output file '{output_file}'. Error: {e}", file=sys.stderr)
        # Note: If backup was created, it still exists even if writing the new file fails.
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
