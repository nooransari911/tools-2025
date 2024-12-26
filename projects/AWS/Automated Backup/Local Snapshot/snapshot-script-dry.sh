#!/bin/bash

YELLOW="\033[1;33m"  # For highlighting directory names
RED="\033[1;31m"    # For warnings/errors
GREEN="\033[1;32m"  # For success messages
BLUE="\033[1;35m"
NC="\033[0m"        # No Color


# File containing the list of source directories
DIR_LIST_FILE=~/Downloads/backup/dir-list.md

# Destination directory
DEST_DIR=~/Downloads/backup/all-dirs-backup/

# Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Verbose log
echo -e "${BLUE}Reading directory list from $DIR_LIST_FILE${NC}"

# Read each directory from the list file
while IFS= read -r dir; do
    # Skip empty lines and comments
    [[ -z "$dir" || "$dir" =~ ^# ]] && continue

    # Expand the directory path
    expanded_dir=$(eval echo "$dir")
    echo -e "\n\n${YELLOW}Processing directory: $expanded_dir${NC}"

    # Extract the directory name
    dir_name="${expanded_dir#${HOME}/Downloads/}"
    dest_subdir="$DEST_DIR/$dir_name"

    # Check if it's a git repository
    if [ -d "$expanded_dir/.git" ]; then
        # echo "  -> Detected git repository: $expanded_dir"

        # Create the destination subdirectory
        mkdir -p "$dest_subdir"
        echo -e "    -> ${YELLOW}Creating destination directory: $dest_subdir${NC}\n    "

        # Use git to get a list of files respecting .gitignore and rsync to copy
        # echo "  -> Copying files from $expanded_dir to $dest_subdir, respecting .gitignore"
        git -C "$expanded_dir" ls-files -z | rsync -av --delete --dry-run --files-from=- --from0 --human-readable "$expanded_dir" "$dest_subdir"
        echo -e "    -> ${GREEN}Copy complete for $expanded_dir${NC}"



    else
        # echo "    -> Not a git repository, copying all files: $expanded_dir"

        # Create the destination subdirectory
        mkdir -p "$dest_subdir"
        # echo -e "    -> ${YELLOW}Creating destination directory: $dest_subdir${NC}\n    "

        # Copy entire directory as-is, with --delete to overwrite existing files
        rsync -av --delete --dry-run --human-readable "$expanded_dir/" "$dest_subdir"
        echo -e "    -> ${GREEN}Copy complete for $expanded_dir${NC}"
    fi
done < "$DIR_LIST_FILE"

echo "Backup operation completed."
