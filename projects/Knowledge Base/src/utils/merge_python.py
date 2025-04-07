#!/usr/bin/env python3

import os
import argparse
import textwrap

def merge_python_files(input_files, output_file, add_descriptions=False):
    """
    Merge multiple Python files into a single file with optional descriptions.
    
    :param input_files: List of input Python files to merge
    :param output_file: Path to the output merged file
    :param add_descriptions: If True, prompt for descriptions for each file
    """
    # Collect merged content
    merged_content = []
    
    # Process each input file
    for file_path in input_files:
        # Read the original file content
        with open(file_path, 'r') as f:
            content = f.read().strip()
        
        # Add description if requested
        if add_descriptions:
            # Prompt for file description
            print(f"\nAdding description for {file_path}")
            desc_input = input("Enter a description for this file (press Enter to skip): ").strip()
            description = f"<note>{desc_input}</note>"
            
            if description:
                # Create a docstring-style description
                desc_header = f'"""\n{textwrap.fill(description, width=70)}\n"""\n\n'
                content = desc_header + content
        
        # Add a separator between files
        merged_content.append(f"\n# === Contents of {os.path.basename(file_path)} ===\n")
        merged_content.append(content)
        merged_content.append("\n")
    
    # Write merged content to output file
    with open(output_file, 'w') as f:
        f.write('\n'.join(merged_content))
    
    print(f"\nMerged {len(input_files)} files into {output_file}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Merge multiple Python files into one.')
    parser.add_argument('input_files', nargs='+', help='List of Python files to merge')
    parser.add_argument('-o', '--output', default='merged_output.py', 
                        help='Output file name (default: merged_output.py)')
    parser.add_argument('-d', '--describe', action='store_true', 
                        help='Interactively add descriptions to files')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate input files exist
    for file_path in args.input_files:
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist.")
            return
    
    # Merge files
    merge_python_files(args.input_files, args.output, args.describe)

if __name__ == '__main__':
    main()
