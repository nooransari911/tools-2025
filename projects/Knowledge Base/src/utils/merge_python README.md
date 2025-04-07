# Python File Merger

## Overview
This script allows you to merge multiple Python files into a single file, with an optional interactive description feature.

## Features
- Merge multiple Python files into one
- Optional interactive description adding
- Preserves original file contents
- Adds file separation markers

## Installation
No additional installation is required. Ensure you have Python 3 installed.

## Usage

### Basic Merge
```bash
python merge_python_files.py file1.py file2.py file3.py
```
This will create a `merged_output.py` file containing contents of all input files.

### Specify Output Filename
```bash
python merge_python_files.py file1.py file2.py -o combined_script.py
```

### Interactive Description Mode
```bash
python merge_python_files.py file1.py file2.py -d
```
This will prompt you to add a description for each file during the merge process.

## Examples

### Merge without descriptions
```bash
python merge_python_files.py utils.py main.py config.py
```

### Merge with descriptions
```bash
python merge_python_files.py utils.py main.py config.py -d
```
When running with `-d`, you'll be prompted to enter a description for each file.

## Notes
- Descriptions are added as docstrings at the top of each file's content
- File contents are separated by markers for readability
- The script preserves the original order of input files
