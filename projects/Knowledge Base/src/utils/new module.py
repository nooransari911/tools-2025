#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys

# --- Global Configuration ---
SOURCE_HTML_BASE_PATH = "/home/ansarimn/Downloads/Industrial Automation/"
DESTINATION_DIR_PATH = "/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/files/"

def process_specific_module():
    # --- State variables for summary ---
    original_module_status = "Pending"
    second_copy_status = "Pending"
    error_occurred = False
    error_messages = [] # To store detailed error messages

    try:
        # 0. Pre-flight check for distinct paths
        if os.path.normpath(SOURCE_HTML_BASE_PATH) == os.path.normpath(DESTINATION_DIR_PATH):
            raise ValueError(f"Config Error: Source ({SOURCE_HTML_BASE_PATH}) and Destination ({DESTINATION_DIR_PATH}) paths cannot be the same.")

        # 1. Get Module Number
        module_number_str = input("Enter module number: ")
        try:
            module_number = int(module_number_str)
            if module_number <= 0:
                raise ValueError("Module number must be a positive integer.")
        except ValueError as e:
            raise ValueError(f"Invalid module number input: {e}") from e
        
        html_filename = f"Module {module_number}.html"
        source_filepath = os.path.join(SOURCE_HTML_BASE_PATH, html_filename)

        # 2. Create/Overwrite empty source file & Edit
        os.makedirs(SOURCE_HTML_BASE_PATH, exist_ok=True)
        with open(source_filepath, "w", encoding="utf-8") as f:
            pass
        # At this point, file is created. Now try editing.

        try:
            # No verbose output from hx itself unless it errors and we capture it.
            process_result = subprocess.run(["hx", source_filepath])
            
            if not os.path.exists(source_filepath): # Check after hx closes
                 raise FileNotFoundError(f"File '{source_filepath}' was removed or not saved during editing.")

            original_module_status = "Success" # If we reach here, creation and editing (or at least hx run) happened.
            if os.path.getsize(source_filepath) == 0:
                original_module_status += " (file is empty)" # Add a note if empty

        except FileNotFoundError: # Specifically for 'hx' command not found
            original_module_status = "Failed (hx not found)"
            raise # Re-raise to be caught by the main error handler
        except Exception as e_hx: # Other errors during hx execution
            original_module_status = "Failed (editor error)"
            raise RuntimeError(f"Error during Helix execution: {e_hx}") from e_hx


        # 3. Prepare Destination Directory & Copy
        if not os.path.exists(DESTINATION_DIR_PATH):
            os.makedirs(DESTINATION_DIR_PATH)
        elif not os.path.isdir(DESTINATION_DIR_PATH):
            raise NotADirectoryError(f"Destination path '{DESTINATION_DIR_PATH}' exists but is not a directory.")
        else:
            # Clean contents
            for item_name in os.listdir(DESTINATION_DIR_PATH):
                item_path = os.path.join(DESTINATION_DIR_PATH, item_name)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
        
        shutil.copy(source_filepath, DESTINATION_DIR_PATH)
        second_copy_status = "Success"

    except Exception as e:
        error_occurred = True
        error_messages.append(str(e)) # Capture the full error message
        # Update status for summary based on where the error likely occurred
        if original_module_status == "Pending":
            original_module_status = "Failed"
        if second_copy_status == "Pending":
            # If original module creation/editing didn't fail explicitly above but an error still happened
            if original_module_status == "Success" or "empty" in original_module_status:
                 second_copy_status = "Failed" # Error occurred during destination prep or copy
            else: # Original module already failed
                 second_copy_status = "Not Attempted"


    # --- Final Output ---
    if error_occurred:
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! ERRORS OCCURRED: ")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        for i, msg in enumerate(error_messages):
            print(f"\nERROR {i+1}:\n{msg}")
        print("\n--- Summary ---") # Still print summary on error
    else:
        print("\n--- Summary ---")

    print(f"  {'Original Module Processed':<30}: {original_module_status}")
    print(f"  {'Second Copy to Destination':<30}: {second_copy_status}")
    print("---------------")

    if error_occurred:
        # Optionally, clean up the source file if it was created and an error occurred afterwards
        # if 'source_filepath' in locals() and os.path.exists(source_filepath) and original_module_status != "Success":
        #     try:
        #         os.remove(source_filepath)
        #         print(f"  -> Cleaned up source file: {source_filepath}")
        #     except OSError:
        #         pass # Ignore cleanup error
        sys.exit(1)


if __name__ == "__main__":
    process_specific_module()
