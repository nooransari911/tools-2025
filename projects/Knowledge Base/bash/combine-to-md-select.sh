#!/bin/bash

# --- Configuration ---
# Use command-line arguments for flexibility.
# Usage: ./combine_files.sh <output_file.md> <input_file_or_dir_1> [input_file_or_dir_2...]
# Example: ./combine_files.sh combined_docs.md src/ common/README.md utils.js

# --- Input Validation ---
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <output_file.md> <input_file_or_dir_1> [input_file_or_dir_2...]"
  echo "Error: Please provide an output file name and at least one input file or directory."
  exit 1
fi

# --- Argument Parsing ---
# First argument is the output file
output_file="$1"
shift # Remove the first argument (output file) from the list

# Remaining arguments are the input files and directories
input_items=("$@")

# --- Processing ---

# Clear the output file or create it if it doesn't exist
# Check if writable first
if ! > "$output_file"; then
  echo "Error: Cannot write to output file '$output_file'. Check permissions or path."
  exit 1
fi
echo "Combining files into '$output_file'..."

# Loop through all provided input items (files or directories)
for item in "${input_items[@]}"; do
  if [ -f "$item" ]; then
    # If it's a file, process it directly
    echo "Processing file: $item"
    # Append the file path as a header
    echo "# $item" >> "$output_file"
    # Append the file content
    cat "$item" >> "$output_file" || echo "Warning: Failed to read file '$item'. Skipping."
    # Add separation between files
    echo -e "\n\n" >> "$output_file"

  elif [ -d "$item" ]; then
    # If it's a directory, find all files within it recursively
    echo "Processing directory: $item"
    # Use find to get all regular files (-type f) within the directory
    # Use null-terminated output (-print0) and read -d '' for safety with special filenames
    find "$item" -type f -print0 | while IFS= read -r -d $'\0' file; do
      echo "  Adding file: $file"
      # Append the file path as a header
      echo "# $file" >> "$output_file"
      # Append the file content
      cat "$file" >> "$output_file" || echo "Warning: Failed to read file '$file'. Skipping."
      # Add separation between files
      echo -e "\n\n" >> "$output_file"
    done
  else
    # If it's neither a file nor a directory that exists
    echo "Warning: Input '$item' is not a valid file or directory. Skipping."
  fi
done

echo "Done. Combined file created at '$output_file'."

# --- Optional Final Copy (Removed) ---
# The hardcoded copy step is removed for generality.
# If you need to copy the result elsewhere, do it as a separate command:
# cp "$output_file" "/path/to/destination/"

# --- Cleanup (Removed) ---
# The temporary "md" directory is no longer used or created.

exit 0
