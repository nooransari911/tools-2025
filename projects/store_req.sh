# Get the current working directory (pwd)
base_dir=$(pwd)

# Initialize an empty file for requirements (clear it if it exists)
> requirements.txt

# Debugging: Check if we are finding any Python files
echo "Searching for Python files..."

# Search for all Python files and process them
find . -name "*.py" | while read file; do
    echo "Processing file: $file"  # Debug: show which file is being processed
    
    # Get the absolute path of the file, relative to the base directory (current working directory)
    relative_path=$(realpath --relative-to="$base_dir" "$file")

    # Extract the top-level directory from the relative path (first part of the path)
    root_dir=$(echo "$relative_path" | cut -d'/' -f1)

    # Extract all the module names (imports) from the Python file
    awk '/^\s*(import|from)\s+/ {gsub(/,/, "", $2); gsub(/^[ \t]+|[ \t]+$/, "", $2); print $2}' "$file" | while read package; do
        echo "Found package: $package"  # Debug: show the package found
        # Add the package name to the requirements.txt (avoiding duplicates)
        echo "$package" >> requirements.txt
    done
done

# Remove duplicate package names and save unique ones to requirements.txt
sort -u requirements.txt -o requirements.txt

# Debug: Check the contents of the requirements.txt
echo "Contents of requirements.txt:"
cat requirements.txt
