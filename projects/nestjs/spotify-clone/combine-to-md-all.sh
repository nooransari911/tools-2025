#!/bin/bash

# Define base directory (make it a single variable for easier modification)
base_dir="/home/ansarimn/Downloads/tools-2025/projects/nestjs/spotify-clone"
base_dir1="$base_dir/src/common"
base_dir2="$base_dir/src/users"
#base_dir3="$base_dir" # No longer needed, use base_dir directly

# Create the "md" directory if it doesn't exist
mkdir -p ./md

# Copy files from both directories to the "md" folder
find "$base_dir/src" -type f -name "*.ts" -exec bash -c 'cp "$1" "./md/$(basename "$1" .ts).md"' _ {} \;

# Define the output file
output_file="$base_dir/comb-file-all.md"

# Clear the output file before writing
> "$output_file"

# Loop through .ts files from both directories and append their contents to the output file
find "$base_dir/src" -type f -name "*.ts" | while IFS= read -r file; do
    # Calculate the relative path using sed for consistent removal of base_dir
    relative_path=$(echo "$file" | sed "s|$base_dir/||")

    # Append the relative path and file contents to the output file
    echo "# $relative_path" >> "$output_file"
    cat "$file" >> "$output_file"
    echo -e "\n\n" >> "$output_file"
done

# Copy the combined file to the Knowledge Base folder
cp "$output_file" "/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/files/combined_file.md"

# Clean up the "md" folder
rm -rf ./md
