#!/bin/bash

# Complete Hugo Theme Changes Extractor
# Usage: ./extract_changes.sh /path/to/original-theme /path/to/modified-theme output-file.md

ORIGINAL_DIR="$1"
MODIFIED_DIR="$2"
OUTPUT_FILE="${3:-all-changes.md}"

if [ $# -lt 2 ]; then
    echo "Usage: $0 <original-theme-dir> <modified-theme-dir> [output-file]"
    exit 1
fi

echo "# Complete Hugo Theme Changes" > "$OUTPUT_FILE"
echo "Generated on: $(date)" >> "$OUTPUT_FILE"
echo "Original theme: $ORIGINAL_DIR" >> "$OUTPUT_FILE"
echo "Modified theme: $MODIFIED_DIR" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "## Modified Files (Diffs)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Find all files in modified directory
find "$MODIFIED_DIR" -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" -o -name "*.txt" -o -name "*.xml" -o -name "*.toml" -o -name "*.yaml" -o -name "*.yml" -o -name "*.md" -o -name "*.go" \) | while read modified_file; do
    # Get relative path
    relative_path=${modified_file#$MODIFIED_DIR/}
    original_file="$ORIGINAL_DIR/$relative_path"

    if [ -f "$original_file" ]; then
        # File exists in both - check if different
        if ! cmp -s "$original_file" "$modified_file"; then
            echo "### Modified: $relative_path" >> "$OUTPUT_FILE"
            echo '```diff' >> "$OUTPUT_FILE"
            diff -u "$original_file" "$modified_file" >> "$OUTPUT_FILE"
            echo '```' >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
        fi
    else
        # New file - show full content
        echo "### New File: $relative_path" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        cat "$modified_file" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    fi
done

echo "## Deleted Files" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Find deleted files
find "$ORIGINAL_DIR" -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" -o -name "*.toml" -o -name "*.yaml" -o -name "*.yml" -o -name "*.md" -o -name "*.go" \) | while read original_file; do
    relative_path=${original_file#$ORIGINAL_DIR/}
    modified_file="$MODIFIED_DIR/$relative_path"

    if [ ! -f "$modified_file" ]; then
        echo "- $relative_path" >> "$OUTPUT_FILE"
    fi
done

echo "" >> "$OUTPUT_FILE"
echo "Changes extraction complete! Output saved to: $OUTPUT_FILE"
