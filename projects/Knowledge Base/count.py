import sys
import os, json
import asyncio
import logging
import concurrent.futures
from multiprocessing import cpu_count, Manager
import google.generativeai as genai
from google.genai import types

from dotenv import load_dotenv
import functools
import google.api_core
import pprint
import pathlib



load_dotenv()
SYS_INS = ""
MODEL_NAME = "GEMINI_20_FL"
API_KEY_PAID_STR = "API_KEY_PAID"
API_KEY_FREE_STR = "API_KEY_FREE"





def load_system_instructions():
    global SYS_INS
    # Retrieve the file path from the environment variable
    instructions_file_path = os.getenv('SYSTEM_INSTRUCTIONS_PATH')

    if instructions_file_path:
        try:
            # Open and read the system instructions file
            with open(instructions_file_path, 'r') as file:
                SYS_INS = file.read()

            # print ("sys_ins L70: ", sys_ins, "\n")
        except Exception as e:
            print(f"Error reading system instructions file: {e}")
    else:
        print("Environment variable 'SYSTEM_INSTRUCTIONS_PATH' not set.")






# Initialize the API once
def configure_genai():
    load_system_instructions ()

    
    global SYS_INS
    global MODEL_NAME

    genai.configure (api_key=os.environ [API_KEY_PAID_STR])
    return genai.GenerativeModel(
        os.environ [MODEL_NAME],
        system_instruction = SYS_INS
    )







async def files_count_tokens_async () -> dict:
    """
    Reads files and "asynchronously" counts tokens (using asyncio.to_thread).
    ONLY uses asyncio.to_thread for count_tokens. File reading is synchronous
    Returns only the files_tokens dictionary.
    """
    
    md_directory = './files/'
    files_tokens = {}
    model = configure_genai ()


    async def process_file(file_path):
        nonlocal files_tokens

        if file_path.endswith((".txt", ".md")):
            try:
                # Synchronous file reading:
                with open(file_path, 'r', encoding="utf-8") as f:
                    content = f.read()

                # "Asynchronous" token counting (using asyncio.to_thread):
                token_count = await asyncio.to_thread(model.count_tokens, content)
                files_tokens[file_path] = token_count.total_tokens


            except Exception as e:
                print(f"Error processing {file_path}: {e}", file=sys.stderr)
                files_tokens[file_path] = -1

        elif file_path.endswith(".pdf"):
            try:
                # Synchronous file reading:
                pathlib_file_path = pathlib.Path(file_path)
                content = pathlib_file_path.read_bytes()
                part = types.Part.from_bytes(data=content, mime_type='application/pdf').inline_data
                blob = google.generativeai.protos.Blob (data=part.data, mime_type=part.mime_type)


                # "Asynchronous" token counting (using asyncio.to_thread):
                token_count = await asyncio.to_thread(model.count_tokens, blob)
                files_tokens[file_path] = token_count.total_tokens
            except Exception as e:
                print(f"Error processing {file_path}: {e}", file=sys.stderr)
                files_tokens[file_path] = -1
        else:
            print(f"Skipping unsupported file type: {file_path}", file=sys.stderr)

    try:
        tasks = [process_file(os.path.join(md_directory, f)) for f in os.listdir(md_directory)]
        await asyncio.gather(*tasks)
        return files_tokens

    except FileNotFoundError:
        print(f"Error: Directory not found: {md_directory}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)




async def count_tokens_in_file(file_path: str) -> int:
    """Counts the tokens in a single file.

    Args:
        file_path: The path to the file.

    Returns:
        The number of tokens in the file, or -1 if an error occurred.
    """
    model = configure_genai()

    try:
        if file_path.endswith((".txt", ".md")):
            with open(file_path, 'r', encoding="utf-8") as f:
                content = f.read()
            token_count = await asyncio.to_thread(model.count_tokens, content)
            return token_count.total_tokens
        elif file_path.endswith(".pdf"):
            pathlib_file_path = pathlib.Path(file_path)
            content = pathlib_file_path.read_bytes()
            part = types.Part.from_bytes(data=content, mime_type='application/pdf').inline_data
            blob = google.generativeai.protos.Blob(data=part.data, mime_type=part.mime_type)
            token_count = await asyncio.to_thread(model.count_tokens, blob)
            return token_count.total_tokens
        else:
            print(f"Unsupported file type: {file_path}", file=sys.stderr)
            return -1  # Indicate unsupported file type
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return -1
    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return -1







async def main():
    try:
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        token_count = await count_tokens_in_file(file_path)
        print(f"Token count for {file_path}: {token_count}")
    except IndexError:
        # No file path provided, process the directory
        token_counts = await files_count_tokens_async()
        pprint.pprint(token_counts, indent=4)




if __name__ == "__main__":
    # trace_span = client.start_span(name="application_start")
    asyncio.run (main())
    # trace_span.end ()


