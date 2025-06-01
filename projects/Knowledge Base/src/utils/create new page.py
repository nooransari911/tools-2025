#!/usr/bin/env python3

import argparse
import datetime
import os, io
from pathlib import Path
import sys
import yaml # type: ignore # For PyYAML
import subprocess # For the debug function
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString
from ruamel.yaml.error import YAMLError as RuamelYAMLError



# --- Constants for Front Matter Fields ---
FM_PATH = "path"
FM_TITLE = "title"
FM_LIST_TITLE = "list-title"
FM_SUBTITLE = "subtitle"
FM_DATE = "date"
FM_CATEGORIES = "categories"
FM_TAGS = "tags"
FM_SET = "set"
FM_WEIGHT = "weight"
FM_DRAFT = "draft"
FM_DESCRIPTION = "description"
FM_SUMMARY = "summary"
FM_FEATURED_IMAGE = "featured_image"
# New top-level and nested params fields
FM_SHOW_TOC = "ShowToc"
FM_PARAMS = "params"
FM_PARAMS_SHOW_CODE_COPY_BUTTONS = "ShowCodeCopyButtons"
FM_PARAMS_SHOW_BREADCRUMBS = "ShowBreadCrumbs"
FM_PARAMS_META = "meta"
FM_SCHEMA = "schema_org_type"
FM_CASCADE = "cascade"
FM_SCH_ABOUT = "about"
SECTION_FILENAME = "_index.md"


# Default values for auto-populated fields
DEFAULT_WEIGHT = 0
DEFAULT_DRAFT = False
FM_PARAMS_META_GOOGLE_SITE_NAME  = "google-site-verification"
FM_PARAMS_META_GOOGLE_SITE_CONTENT = "zsVm68p-q-NLM02swJYWtnt7jMVj2ZX0NidrEWIgEhs"
FM_PARAMS_META_DUMMY_NAME = "dummy"
FM_PARAMS_META_DUMMY_CONTENT = "dummy meta tag from content front matter"
FM_SCHEMA_VALUE = "notes"


# --- Path Handling Module ---
def resolve_and_prepare_target_path(path_str: str) -> Path:
    """
    Resolves a path string (relative or absolute) against the PWD
    and ensures parent directories exist for the target file.
    """
    absolute_path = Path(path_str).resolve()
    try:
        absolute_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Ensured directory exists for target: {absolute_path.parent}")
    except OSError as e:
        raise IOError(f"Could not create directories for {absolute_path.parent}: {e}") from e
    return absolute_path

def resolve_source_file_production(path_str: str | None) -> Path | None:
    """
    Resolves an optional source file path (relative or absolute) against PWD
    and checks for its existence and readability. (Production Version)
    """
    if not path_str:
        return None

    source_file_path = Path(path_str).resolve()

    if not source_file_path.is_file():
        print(
            f"Warning: Source file '{source_file_path}' not found or is not a file. Content will not be copied.",
            file=sys.stderr
        )
        return None
    try:
        # Perform a basic read check. os.access(path, os.R_OK) could also be used
        # but open() is more direct for files.
        with open(source_file_path, 'rb') as f:
            f.read(1)
        return source_file_path
    except IOError as e:
        print(
            f"Warning: Source file '{source_file_path}' found but cannot be read. Error: {e}. Content will not be copied.",
            file=sys.stderr
        )
        return None

def resolve_source_file_debug (path_str: str | None) -> Path | None:
    """ Debug version of resolve_source_file with extensive printing. """
    if not path_str:
        return None

    print(f"\n--- Python: resolve_source_file_debug ---")
    print(f"DEBUG Python: Received path_str for source: '{path_str}' (type: {type(path_str)})")
    print(f"DEBUG Python: repr(path_str) for source: {repr(path_str)}")
    
    try:
        print(f"DEBUG Python: Hexdump of received path_str for source:")
        # Ensure path_str is encoded correctly for subprocess input
        path_bytes = path_str.encode('utf-8', errors='surrogateescape') 
        process = subprocess.run(['hexdump', '-C'], input=path_bytes, capture_output=True, check=False)
        if process.stdout:
            print(process.stdout.decode(errors='replace'))
        if process.stderr:
            print(f"Hexdump stderr: {process.stderr.decode(errors='replace')}")

    except Exception as e:
        print(f"DEBUG Python: Error during hexdump: {e}")

    source_file_path_obj = Path(path_str)
    print(f"DEBUG Python: Path object from input: '{source_file_path_obj}' (is_absolute: {source_file_path_obj.is_absolute()})")

    try:
        resolved_source_file_path = source_file_path_obj.resolve()
        print(f"DEBUG Python: Resolved source path: '{resolved_source_file_path}'")
    except Exception as e:
        print(f"DEBUG Python: ERROR resolving path '{source_file_path_obj}': {e}", file=sys.stderr)
        return None

    print(f"DEBUG Python: Current CWD in Python: '{Path.cwd()}'")
    print(f"DEBUG Python: Checking OS interaction for: '{resolved_source_file_path}'")

    try:
        stat_info = os.stat(resolved_source_file_path)
        print(f"DEBUG Python: os.stat successful: {stat_info}")
    except OSError as e:
        print(f"DEBUG Python: os.stat FAILED for '{resolved_source_file_path}'", file=sys.stderr)
        print(f"DEBUG Python:   Error type: {type(e)}", file=sys.stderr)
        print(f"DEBUG Python:   Error message: {e.strerror}", file=sys.stderr)
        print(f"DEBUG Python:   Error number (errno): {e.errno}", file=sys.stderr)
        print(f"DEBUG Python:   Filename in error: {e.filename}", file=sys.stderr)
        print(f"Warning: Source file '{resolved_source_file_path}' cannot be stat'd. Content will not be copied.", file=sys.stderr)
        return None

    exists = resolved_source_file_path.exists()
    is_file = resolved_source_file_path.is_file()
    is_dir = resolved_source_file_path.is_dir()
    print(f"DEBUG Python: Path checks - Exists: {exists}, Is File: {is_file}, Is Dir: {is_dir}")

    if not is_file:
        print(
            f"Warning: Resolved source path '{resolved_source_file_path}' is not a file. "
            f"(exists: {exists}, is_dir: {is_dir}). Content will not be copied.",
            file=sys.stderr
        )
        return None
    
    print(f"DEBUG Python: Attempting to open and read from: '{resolved_source_file_path}'")
    try:
        with open(resolved_source_file_path, 'rb') as f:
            f.read(1)
        print(f"DEBUG Python: Successfully opened and read 1 byte from '{resolved_source_file_path}'")
        print(f"--- Python: resolve_source_file_debug returning VALID path ---")
        return resolved_source_file_path
    except IOError as e:
        print(
            f"Warning: Source file '{resolved_source_file_path}' found but cannot be read (IOError). Error: {e}. Content will not be copied.",
            file=sys.stderr
        )
        print(f"--- Python: resolve_source_file_debug returning NONE due to IOError ---")
        return None
    except Exception as e: # Catch any other unexpected error
        print(
            f"Warning: An unexpected error occurred while trying to read source file '{resolved_source_file_path}'. Error: {e}. Content will not be copied.",
            file=sys.stderr
        )
        print(f"--- Python: resolve_source_file_debug returning NONE due to unexpected error ---")
        return None


# --- User Input Module ---
def get_user_front_matter_inputs() -> dict:
    """
    Prompts the user for title and description.
    Handles KeyboardInterrupt and EOFError gracefully.
    """
    print("\nPlease provide the following details for the front matter (Ctrl+C or Ctrl+D to cancel):")
    try:
        title = input("Enter Title: ").strip()
        while not title:
            title = input("Title cannot be empty. Enter Title: ").strip()

        description = input("Enter Description: ").strip()
        while not description:
            description = input("Description cannot be empty. Enter Description: ").strip()

        schema = input("Enter Schema: ").strip()
        # if not schema:
        #     schema = FM_SCHEMA_VALUE

        
    except (KeyboardInterrupt, EOFError) as e:
        raise e # Re-raise to be caught by main's handler

    return {
        FM_TITLE: title,
        FM_DESCRIPTION: description,
        FM_SCHEMA: schema
    }

# --- Front Matter Generation Module ---
def generate_front_matter_data(
    user_inputs: dict,
    target_input_path_str: str,
    resolved_absolute_target_path: Path,
    auto_date: str,
    auto_weight: int,
    auto_draft: bool,
) -> dict:
    """
    Generates the complete front matter dictionary, including new fields.
    """
    path_obj_from_input = Path(target_input_path_str)
    cwd = Path.cwd()
    path_for_fm_field: str

    if not path_obj_from_input.is_absolute():
        path_for_fm_field = target_input_path_str
        if path_for_fm_field.startswith(("./", ".\\")):
            path_for_fm_field = path_for_fm_field[2:]
    else:
        try:
            path_for_fm_field = resolved_absolute_target_path.relative_to(cwd).as_posix()
        except ValueError:
            path_for_fm_field = resolved_absolute_target_path.as_posix()
            print(
                f"Info: Target path '{resolved_absolute_target_path}' is not under CWD '{cwd}'. "
                f"Using resolved path in front matter 'path' field: '{path_for_fm_field}'",
                file=sys.stderr
            )
    if os.sep != '/' and os.sep in path_for_fm_field:
        path_for_fm_field = path_for_fm_field.replace(os.sep, '/')

    front_matter = {
        # Auto-populated & User Input (as before)
        FM_PATH: path_for_fm_field,
        FM_DATE: auto_date,
        FM_WEIGHT: auto_weight,
        FM_DRAFT: auto_draft,
        FM_TITLE: user_inputs[FM_TITLE],
        FM_LIST_TITLE: user_inputs[FM_TITLE],
        FM_DESCRIPTION: user_inputs[FM_DESCRIPTION],
        FM_SUMMARY: user_inputs[FM_DESCRIPTION],
    }

    if user_inputs [FM_SCHEMA]:
        front_matter [FM_SCHEMA] = user_inputs [FM_SCHEMA]










    is_section: bool = target_input_path_str.lower ().endswith (SECTION_FILENAME)

    if (is_section):
        front_matter [FM_CASCADE] = {
            FM_DRAFT: auto_draft,
            FM_SHOW_TOC: True,
            FM_PARAMS: {
                FM_PARAMS_SHOW_CODE_COPY_BUTTONS: True,
                FM_PARAMS_SHOW_BREADCRUMBS: True,
                FM_PARAMS_META: [
                # {
                #     "name": DoubleQuotedScalarString (FM_PARAMS_META_GOOGLE_SITE_NAME),
                #     "content": DoubleQuotedScalarString (FM_PARAMS_META_GOOGLE_SITE_CONTENT)
                # },
                {
                    "name": DoubleQuotedScalarString (FM_PARAMS_META_DUMMY_NAME),
                    "content": DoubleQuotedScalarString (FM_PARAMS_META_DUMMY_CONTENT)
                }]
            },
            FM_SUBTITLE: "",
            FM_SET: "",
            FM_FEATURED_IMAGE: "",
            FM_CATEGORIES: [],
            FM_TAGS: [],
            FM_SCH_ABOUT: [],
            FM_SCHEMA: user_inputs [FM_SCHEMA],
        }

        front_matter [FM_SHOW_TOC] = False



    return front_matter





# --- File Operations Module ---
def read_file_content(file_path: Path) -> str:
    """
    Reads the entire content of a given file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except IOError as e:
        raise IOError(f"Could not read content from {file_path}: {e}") from e

def write_markdown_file(
    target_file_path: Path,
    front_matter_data: dict,
    source_content: str | None = None
) -> None:
    """
    Writes the front matter and optional source content to the target file.
    """

    # Assuming 'front_matter_data' is defined
    # And necessary imports are at the top of the file:
    # from ruamel.yaml import YAML
    # from ruamel.yaml.error import YAMLError as RuamelYAMLError # Or just YAMLError if no conflict
    # import io

    ruamel_yaml_instance = YAML()
    ruamel_yaml_instance.indent(mapping=4, sequence=4, offset=2) # 4-space indent for maps/sequences
    # ruamel.yaml defaults:
    # - Preserves dict insertion order (for Python 3.7+ dicts or CommentedMap),
    #   similar to sort_keys=False but typically more desirable.
    # - Allows Unicode characters.
    # - Uses a safe dumper.

    try:
        string_stream = io.StringIO()
        ruamel_yaml_instance.dump(front_matter_data, string_stream)
        yaml_string = string_stream.getvalue()
    except RuamelYAMLError as e: # Use ruamel.yaml's YAMLError
        # Re-raise using ruamel.yaml's error type.
        # If the calling code specifically expects the original PyYAML error type,
        # this part might need adjustment (e.g., by wrapping 'e' or raising a custom error).
        raise RuamelYAMLError(f"Error formatting front matter to YAML: {e}") from e



    content_to_write = f"---\n{yaml_string}---\n\n"
    if source_content:
        content_to_write += source_content

    try:
        with open(target_file_path, "w", encoding="utf-8") as f:
            f.write(content_to_write)
        print(f"Successfully created/updated Markdown file: {target_file_path}")
        if source_content:
            print("Appended content from source file.")
    except IOError as e:
        raise IOError(f"Could not write to file {target_file_path}: {e}") from e

# --- Main Orchestration ---
def main():
    parser = argparse.ArgumentParser(
        description="Create a new Markdown file with YAML front matter, optionally copying content from a source file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "target_file_path_arg",
        type=str,
        help='Path (relative or absolute) for the new Markdown file.',
    )
    parser.add_argument(
        "source_file_path_arg",
        type=str,
        nargs='?',
        default=None,
        help='(Optional) Path (relative or absolute) to a source Markdown file whose content will be copied.'
    )
    parser.add_argument(
        "--weight", type=int, default=DEFAULT_WEIGHT, help="Weight for sorting."
    )
    parser.add_argument(
        "--draft", action=argparse.BooleanOptionalAction, default=DEFAULT_DRAFT, help="Set draft status."
    )
    # Add a debug flag if you want to switch between resolve_source_file versions
    # parser.add_argument("--debug-source", action="store_true", help="Use debug source file resolver.")


    args = parser.parse_args()
    target_input_str = args.target_file_path_arg
    source_input_str = args.source_file_path_arg

    try:
        absolute_target_path = resolve_and_prepare_target_path(target_input_str)

        if absolute_target_path.exists():
            overwrite_input = input(
                f"Target file '{absolute_target_path}' already exists. Overwrite? (y/N): "
            ) # No strip here, allow direct Ctrl+D/Ctrl+C
            if overwrite_input.strip().lower() != 'y':
                print("Operation cancelled by user (overwrite declined).")
                sys.exit(0)

        source_content_to_copy = None
        if source_input_str:
            # CHOOSE WHICH VERSION TO USE:
            # For production:
            absolute_source_path = resolve_source_file_production(source_input_str)
            # For debugging:
            # absolute_source_path = resolve_source_file_debug(source_input_str)
            # Or use args.debug_source if flag is implemented

            if absolute_source_path:
                print(f"Reading content from source file: {absolute_source_path}")
                source_content_to_copy = read_file_content(absolute_source_path)

        user_fm_inputs = get_user_front_matter_inputs()
        current_date_iso = datetime.date.today().isoformat()

        front_matter_dict = generate_front_matter_data(
            user_inputs=user_fm_inputs,
            target_input_path_str=target_input_str,
            resolved_absolute_target_path=absolute_target_path,
            auto_date=current_date_iso,
            auto_weight=args.weight,
            auto_draft=args.draft,
        )

        write_markdown_file(
            absolute_target_path,
            front_matter_dict,
            source_content=source_content_to_copy
        )

    except (IOError, yaml.YAMLError, ValueError) as e: # ValueError for things like bad int for weight
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n^C (Keyboard Interrupt). Operation cancelled.", file=sys.stderr)
        sys.exit(130) # Standard exit code for SIGINT
    except EOFError:
        # This catches EOF from input() if STDIN is closed or Ctrl+D is pressed
        print("\n^D (EOF). Operation cancelled.", file=sys.stderr)
        sys.exit(1) # General error exit code for EOF on input

if __name__ == "__main__":
    main()
