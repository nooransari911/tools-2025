#!/bin/bash

output_file="$1"
shift  # Remove the output file from the argument list

: > "$output_file"  # Empty the output file if it exists

for file in "$@"; do
    {
        echo "===== $file ====="
        cat "$file"
        echo -e "\n"
    } >> "$output_file"
done
