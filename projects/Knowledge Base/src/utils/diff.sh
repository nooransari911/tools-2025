#!/bin/bash

# --- Configuration ---
ORIGINAL_THEME_DIR="" # Path to the original PaperMod theme directory
MODIFIED_THEME_DIR="" # Path to your modified PaperMod theme directory
OUTPUT_PATCH_FILE="papermod_changes.patch"

# --- Helper Function for Usage ---
usage() {
  echo "Usage: $0 <original_theme_directory> <modified_theme_directory> [output_patch_file]"
  echo "  Generates a patch file capturing changes between the original and modified theme."
  echo ""
  echo "  Arguments:"
  echo "    original_theme_directory: Path to the clean, original PaperMod theme folder."
  echo "    modified_theme_directory: Path to your modified PaperMod theme folder."
  echo "    output_patch_file:        (Optional) Name of the patch file to generate."
  echo "                              Defaults to 'papermod_changes.patch' in the current directory."
  exit 1
}

# --- Argument Parsing ---
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Error: Missing required arguments."
  usage
fi

ORIGINAL_THEME_DIR="$1"
MODIFIED_THEME_DIR="$2"

if [ -n "$3" ]; then
  OUTPUT_PATCH_FILE="$3"
fi

# --- Validation ---
if [ ! -d "$ORIGINAL_THEME_DIR" ]; then
  echo "Error: Original theme directory '$ORIGINAL_THEME_DIR' not found or is not a directory."
  exit 1
fi

if [ ! -d "$MODIFIED_THEME_DIR" ]; then
  echo "Error: Modified theme directory '$MODIFIED_THEME_DIR' not found or is not a directory."
  exit 1
fi

# --- Generate the Diff ---
echo "Comparing '$ORIGINAL_THEME_DIR' with '$MODIFIED_THEME_DIR'..."

# The 'diff' command options:
# -N, --new-file: Treat absent files as empty. This is crucial for showing new files.
# -a, --text: Treat all files as text and compare them line-by-line.
# -u, --unified[=NUM]: Output NUM (default 3) lines of unified context. This is the standard patch format.
# -r, --recursive: Recursively compare any subdirectories found.
# -p, --show-c-function: Show which C function each change is in (can be helpful for code context).
#
# We redirect the output to the specified patch file.
# The order of directories matters: diff original modified (shows changes to get from original to modified)

# Note: If you have a .git directory in your modified theme, and you DON'T want to include it
# (e.g., if you initialized a git repo there for your own tracking), you can exclude it:
# --exclude=".git"
# Add other --exclude patterns as needed (e.g., --exclude="node_modules")

diff -Naurp "$ORIGINAL_THEME_DIR" "$MODIFIED_THEME_DIR" > "$OUTPUT_PATCH_FILE"

# Check if diff produced any output (i.e., if there were changes)
if [ -s "$OUTPUT_PATCH_FILE" ]; then
  echo "Changes captured in '$OUTPUT_PATCH_FILE'."
  echo "You can inspect this file to see all additions, deletions, and modifications."
  echo "To apply this patch (for example, to another copy of the original theme):"
  echo "  cd /path/to/another/original/papermod"
  echo "  patch -p1 < /path/to/$OUTPUT_PATCH_FILE"
else
  echo "No differences found between the two directories."
  # Optionally remove the empty patch file
  # rm "$OUTPUT_PATCH_FILE"
fi

exit 0
