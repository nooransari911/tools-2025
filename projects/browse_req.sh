# Get the current working directory (pwd)
base_dir=$(pwd)

# Search for all Python files and process them
find . -name "*.py" | while read file; do
    # Get the absolute path of the file, relative to the base directory (current working directory)
    relative_path=$(realpath --relative-to="$base_dir" "$file")

    # Extract the top-level directory from the relative path (first part of the path)
    root_dir=$(echo "$relative_path" | cut -d'/' -f1)

    # Extract all the module names (imports) from the Python file
    awk '/^\s*(import|from)\s+/ {gsub(/,/, "", $2); gsub(/^[ \t]+|[ \t]+$/, "", $2); print $2}' "$file" | while read package; do
        # Output the module and the root directory with padding
        printf "%-30s %-20s\n" "$package" "$root_dir"
    done
done | sort -u -k2,2 | fzf -m
