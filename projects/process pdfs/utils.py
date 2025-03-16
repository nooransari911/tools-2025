import time
import signal
import google.generativeai as genai
from vertexai.generative_models import Part
from google.cloud import storage
import datetime, os, sys, io, json, re, time, signal
import requests
from contextlib import redirect_stdout
from dotenv import load_dotenv
from strings import *
import functools

from flask import Flask, request, render_template, jsonify, Response, make_response, Blueprint, stream_with_context, redirect
import multiprocessing, psutil
from multiprocessing import Manager


load_dotenv()






global_gemini_responses = {}
GLOBAL_GENERIC_LIST = []
GLOBAL_GENERIC_LIST2 = []


def timestamped_print(func):
    @functools.wraps(func)  # Preserve function metadata
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{func.__name__}] ", end="")  # Print timestamp and function name
        return func(*args, **kwargs)  # Call the original function
    return wrapper




def testsplit_markdown_file2 (input_file):
    global GLOBAL_GENERIC_LIST
    #GLOBAL_GENERIC_LIST = []
    output_dir = './ex-input files/segments/'
    os.makedirs(output_dir, exist_ok=True)
    with open(input_file, 'r') as file:
        content = file.read()

    # Replace the old format with the new format
    content = re.sub(r'# (\d+) Module (\d+): AWS Academy Data Engineering: (.*?) ##', r'# \1 Module \2: AWS Academy Data Engineering - \3 ##', content, flags=re.S | re.M)



    # Define a regular expression pattern to match H1 headings and their content
    pattern = re.compile(r'# \d+ Module \d+: AWS Academy Data Engineering(?: -|:).*?(?=\n# \d+ Module \d+:|(?:\n#\d+)|(?:\n##)|\Z)', re.S | re.M)

    # Find all matches in the content

    matches = pattern.findall(content)

    for match in matches:
        # Extract the heading and module number
        heading_match = re.match(r'# \d+ Module (\d+):', match)
        if heading_match:
            module_number = heading_match.group(1)
            file_name = f"Module {module_number}.md"
            file_path = os.path.join(output_dir, file_name)
            # Write the content to the corresponding file
            with open(file_path, 'w') as output_file:
                output_file.write(f"{datetime.datetime.now()}")
                output_file.write(match.strip())

            GLOBAL_GENERIC_LIST.append (f"{match}: {input_file}")
            print(f"Created file: {file_path}")
    #print(GLOBAL_GENERIC_LIST)


def testsplit_markdown_file (input_file):
    global GLOBAL_GENERIC_LIST
    # GLOBAL_GENERIC_LIST = []
    output_dir = './ex-input files/segments/'
    os.makedirs(output_dir, exist_ok=True)
    with open(input_file, 'r') as file:
        content = file.read()

    old_pattern = re.compile(r'# (\d+) Module (\d+): AWS Academy Data Engineering: (.+)')
    new_pattern = r'# \1 Module \2: AWS Academy Data Engineering - \3'
    content = old_pattern.sub(new_pattern, content)




    # Find all headings and extract content
    headings = re.findall(r'# \d+ Module \d+: AWS Academy Data Engineering - .+', content)
    modules = {}

    for heading in headings:
        GLOBAL_GENERIC_LIST.append(heading)  # Append heading to the global list
        module_number = re.search(r'# \d+ Module (\d+):', heading).group(1)
        if module_number not in modules:
            modules[module_number] = []
    print (headings)


    # Extract content for each module
    current_module = None
    for line in content.split('\n'):
        if old_pattern.match(line):
            current_module = re.search(r'# \d+ Module (\d+):', line).group(1)
        elif current_module:
            modules[current_module].append(line)

    # Save each module's content into separate files
    for module, lines in modules.items():
        GLOBAL_GENERIC_LIST2.append('\n'.join(lines))
        module_filename = f'Module {module}.md'
        module_filepath = os.path.join(output_dir, module_filename)
        with open(module_filepath, 'w', encoding='utf-8') as module_file:
            module_file.write(f"{datetime.datetime.now()}")
            module_file.write('\n'.join(lines))




def split_markdown_file (input_file):
    global GLOBAL_GENERIC_LIST

    output_dir = './ex-input files/segments/'
    os.makedirs(output_dir, exist_ok=True)
    with open(input_file, 'r') as file:
        content = file.read()


    # Regular expressions for processing
    heading_pattern = re.compile(r'# (\d+) Module (\d+): AWS Academy Data Engineering: (.+)')
    replacement_pattern = (r'# \1 Module \2: AWS Academy Data Engineering - \3')

    # Replace heading text
    new_content = heading_pattern.sub(replacement_pattern, content)

    old_pattern = re.compile(r'# (\d+) Module (\d+):')
    new_pattern = (r'# \2 Module \2:')
    new_content = old_pattern.sub(new_pattern, new_content)



    # Extract headings
    heading_pattern_new = re.compile(r'# \d+ Module \d+: AWS Academy Data Engineering - .+')

    headings = heading_pattern_new.findall(new_content)

    # Append headings to GLOBAL_GENERIC_LIST
    for heading in headings:
        GLOBAL_GENERIC_LIST.append(heading)
    #print(GLOBAL_GENERIC_LIST)
    # Extract content for each module
    content_lines = new_content.split('\n')
    current_module = None
    module_contents = {}

    for line in content_lines:
        heading_match = heading_pattern_new.match(line)
        if heading_match:
            current_module = re.search(r'# \d+ Module (\d+):', line).group(1)
            if current_module not in module_contents:
                module_contents[current_module] = []
        elif current_module:
            module_contents[current_module].append(line)

    # Append each module's content to GLOBAL_GENERIC_LIST2 and write to files
    for module, lines in module_contents.items():
        module_content = '\n'.join(lines).strip()
        GLOBAL_GENERIC_LIST2.append(module_content)

        # Save each module's content into separate files
        module_filename = f'Module {module}.md'
        module_filepath = os.path.join(output_dir, module_filename)


        with open(module_filepath, 'w', encoding='utf-8') as module_file:
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
            module_file.write(f"# {current_datetime}\n\n")  # Add datetime as H1 heading
            module_file.write(module_content)