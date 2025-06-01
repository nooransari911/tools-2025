#!/usr/bin/env python3
import os
import sys
import re
from typing import TextIO, Optional, Match, List, Tuple

# Define highlight markers globally or pass them around
HIGHLIGHT_PREFIX: str = "\033[91m\033[1m<<\033[0m" # Bold Red <<
HIGHLIGHT_SUFFIX: str = "\033[91m\033[1m>>\033[0m" # Bold Red >>
RESET_COLOR: str = "\033[0m"

# --- Match and Display Function (modified to store match info) ---
def find_and_display_match(
    pattern: str,
    line_number: int,
    line_content: str,
    potential_changes: List[Tuple[int, int, int]]
) -> None:
    """
    Finds the first match on a line, displays it highlighted,
    and stores its location for later replacement.
    """
    match: Optional[Match[str]] = re.search(pattern, line_content)

    if match:
        if match.group(1):  # Group 1 is "(## )"
            start_highlight_index: int = match.start(1)
            end_highlight_index: int = match.end(1)

            # Store: (line_index_in_original_lines, start_of_group1, end_of_group1)
            # We use line_number - 1 because list of lines will be 0-indexed
            potential_changes.append((line_number - 1, start_highlight_index, end_highlight_index))

            before_selection: str = line_content[:start_highlight_index]
            selected_text: str = line_content[start_highlight_index:end_highlight_index]
            after_selection: str = line_content[end_highlight_index:]

            highlighted_line: str = (
                f"{before_selection}{HIGHLIGHT_PREFIX}{selected_text}{HIGHLIGHT_SUFFIX}{after_selection}"
            )
            print(f"L{line_number}: {highlighted_line}{RESET_COLOR}")
    # else:
        # Optionally print lines that don't match for full context during review
        # print(f"L{line_number}: {line_content}")


# --- Main Application Logic ---
def process_file_for_replacement(filepath: str) -> None:
    """
    Processes a file:
    1. Displays potential changes.
    2. Asks for user confirmation.
    3. If confirmed, applies changes to the file.
    """
    pattern: str = r"#*(## )"  # Target "## " in group 1
    replacement_text: str = "# "    # What "## " will be replaced with

    original_lines: List[str] = []
    potential_changes: List[Tuple[int, int, int]] = [] # (line_idx, start_g1, end_g1)

    try:
        with open(filepath, 'r', encoding='utf-8') as f_read:
            print("--- Potential Changes ---")
            for i, raw_line in enumerate(f_read):
                line: str = raw_line.rstrip('\n')
                original_lines.append(line) # Store original line (without \n for now)
                find_and_display_match(pattern, i + 1, line, potential_changes)
            print("--- End of Potential Changes ---\n")

    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)

    if not potential_changes:
        print("No matches found that would be changed. Exiting.")
        sys.exit(0)

    # --- User Confirmation ---
    while True:
        confirm = input(f"Proceed with replacing {len(potential_changes)} occurrences of '## ' with '# ' in '{filepath}'? (yes/no): ").strip().lower()
        if confirm == 'yes':
            break
        elif confirm == 'no':
            print("Operation cancelled by user.")
            sys.exit(0)
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

    # --- Apply Changes (if confirmed) ---
    print(f"\nApplying changes to '{filepath}'...")
    modified_lines: List[str] = list(original_lines) # Create a mutable copy

    # Iterate through changes in reverse order of line number and then reverse order of start index
    # This is crucial if multiple changes are on the same line or if replacement length differs,
    # to ensure character indices remain valid for subsequent replacements on that line.
    # For this specific replacement "## " -> "# ", length changes, so reverse processing is safer.
    
    # Since our current pattern with re.search only finds one match per line,
    # the complexity of multiple changes *on the same line* is avoided for this specific script.
    # However, processing changes from bottom-up (last line first) is still good practice
    # if we were to modify lines directly in a list representing file content.

    # A simpler way when we have line_idx and char_idx for each unique match (one per line here):
    # Build the new lines from scratch for each modified line.
    
    # For this problem, since re.search finds only one match per line,
    # we can simply iterate through our stored `potential_changes`.
    # Each tuple in `potential_changes` refers to a unique line and a unique match on that line.

    lines_to_rewrite = list(original_lines) # Start with a copy of original content

    for line_idx, start_g1, end_g1 in potential_changes:
        line_to_modify = lines_to_rewrite[line_idx]
        
        # Reconstruct the line with the replacement
        new_line = (
            line_to_modify[:start_g1] +       # Part before group 1
            replacement_text +                # The replacement
            line_to_modify[end_g1:]           # Part after group 1
        )
        lines_to_rewrite[line_idx] = new_line

    try:
        with open(filepath, 'w', encoding='utf-8') as f_write:
            for line in lines_to_rewrite:
                f_write.write(line + '\n') # Add back the newline
        print(f"Successfully updated '{filepath}'.")
    except Exception as e:
        print(f"Error writing changes to file '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <filepath>", file=sys.stderr)
        sys.exit(1)

    target_filepath: str = sys.argv[1]
    process_file_for_replacement(target_filepath)
