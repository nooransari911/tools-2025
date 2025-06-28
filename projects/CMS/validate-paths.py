import io
import re
import argparse
from ruamel.yaml import YAML
from pathlib import Path
from typing import Optional, Tuple, Iterator, Any

# --- Configuration ---
# Set this to the root of your Hugo site.
HUGO_ROOT_DIRECTORY = "."
CONTENT_DIRECTORY = Path(HUGO_ROOT_DIRECTORY) / "content"

# ==============================================================================
# Component 1: ContentFileFinder (The Scout)
# Responsibility: Find all content files to process.
# ==============================================================================

def find_content_files(directory: Path) -> Iterator[Path]:
    """
    Finds all Markdown (.md) files by recursively searching the given directory.
    
    Args:
        directory: The Path object for the content directory.
        
    Yields:
        A Path object for each content file found.
    """
    if not directory.is_dir():
        print(f"❌ Error: Directory not found at '{directory}'")
        return
        
    for file_path in directory.rglob("*.md"):
        # Ignore files like _index.md, whose URL is determined by the directory.
        if file_path.name.startswith("_index"):
            continue
        yield file_path

# ==============================================================================
# Component 2: FrontMatterParser (The Extractor)
# Responsibility: Extract YAML front matter and content from a file.
# ==============================================================================

def parse_front_matter(file_path: Path) -> Optional[Tuple[Any, str]]:
    """
    Parses YAML front matter ('---') and content from a file.

    Returns:
        A tuple of (front_matter_data, content_string), or None if no valid
        YAML front matter is found. `front_matter_data` is a ruamel.yaml object.
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        # This regex specifically looks for '---' delimiters.
        pattern = r"^---\s*\n(.*?)\n---"
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            return None

        fm_string = match.group(1)
        main_content = content[match.end(0):].lstrip()
        
        yaml = YAML()
        front_matter = yaml.load(fm_string)
            
        return front_matter, main_content

    except Exception as e:
        print(f"❌ Error parsing/reading file {file_path}: {e}")
        return None

# ==============================================================================
# Component 3: PathGeneratorAndValidator (The Logician)
# Responsibility: Generate expected path from file location and validate it.
# ==============================================================================

def generate_and_validate_path(
    front_matter: dict, 
    file_path: Path, 
    content_root: Path
) -> Tuple[bool, str]:
    """
    Generates the expected path and validates if the current path matches.
    Example: 'content/blog/my-post.md' -> 'blog/my-post'

    Returns:
        A tuple (needs_correction: bool, expected_path: str).
    """
    relative_path = file_path.relative_to(content_root)
    # path_without_ext = relative_path.with_suffix('')
    path_without_ext = relative_path
    expected_path = path_without_ext.as_posix()
    # expected_path = path_without_ext

    current_path = front_matter.get("path")

    # Correction is needed if the path key doesn't exist or if it's different.
    return current_path != expected_path, expected_path

# ==============================================================================
# Component 4: FileUpdater (The Writer)
# Responsibility: Write the updated YAML content back to the file.
# ==============================================================================

def update_file(
    file_path: Path, 
    front_matter: Any, 
    content_body: str
) -> None:
    """Writes the modified YAML front matter and content back to the file."""
    try:
        yaml = YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        string_stream = io.StringIO()
        yaml.dump(front_matter, string_stream)
        fm_string = string_stream.getvalue()

        # Reconstruct the file with the '---' delimiters.
        new_content = f"---\n{fm_string}---\n{content_body}"
        file_path.write_text(new_content, encoding='utf-8')
            
    except Exception as e:
        print(f"  └─ ❌ Failed to write updates to {file_path}: {e}")

# ==============================================================================
# Component 5: Orchestrator (The Conductor)
# Responsibility: Coordinate the process and report results.
# ==============================================================================

def run_validator(content_dir: Path, dry_run: bool = True):
    """
    Main orchestrator to find, parse, validate, and correct Hugo content paths.
    """
    if dry_run:
        print("💧 Running in DRY-RUN mode. Only incorrect paths will be shown.")
        print("-" * 50)
    else:
        print("🔥 Running in LIVE mode. Files will be modified.")
    
    processed_count = 0
    issue_count = 0

    for file_path in find_content_files(content_dir):
        processed_count += 1
        
        parsed_data = parse_front_matter(file_path)
        if not parsed_data:
            if not dry_run:
                print(f"\n📄 Processing: {file_path.relative_to(content_dir.parent)}")
                print("  └─ No YAML front matter found. Skipping.")
            continue
            
        front_matter, content_body = parsed_data
        
        needs_correction, expected_path = generate_and_validate_path(
            front_matter, file_path, content_dir
        )
        
        if needs_correction:
            issue_count += 1
            current_path = front_matter.get("path", "[Not Set]")
            
            print(f"\nFile: {file_path.relative_to(content_dir.parent)}")
            print(f"  ├─ Current Path:  '{current_path}'")
            print(f"  └─ Expected Path: '{expected_path}'")
            
            if not dry_run:
                front_matter["path"] = expected_path
                update_file(file_path, front_matter, content_body)
                print("     ✨ File Updated.")
        elif not dry_run:
            print(f"\n📄 Processing: {file_path.relative_to(content_dir.parent)}")
            print("  └─ ✅ 'path' field is correct.")

    print("\n" + "="*50)
    print("📊 Validation Complete!")
    print(f"   - Files Scanned: {processed_count}")
    print(f"   - Issues Found:  {issue_count}")
    if not dry_run and issue_count > 0:
        print(f"   - Files Fixed:   {issue_count}")
    print("="*50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Validate and correct the 'path' YAML front matter in Hugo content files.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Run the script without modifying any files.\n"
             "It will only report the files with incorrect paths."
    )

    args = parser.parse_args()

    if not CONTENT_DIRECTORY.exists():
        print(f"Error: The content directory '{CONTENT_DIRECTORY}' does not exist.")
        print("Please check the HUGO_ROOT_DIRECTORY variable at the top of the script.")
    else:
        run_validator(CONTENT_DIRECTORY, dry_run=args.dry_run)
