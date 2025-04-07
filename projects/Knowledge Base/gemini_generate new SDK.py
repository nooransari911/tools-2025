import sys
import os, json
import asyncio
import typing_extensions as typing
from pydantic import BaseModel # Added for schema definition
from typing import Optional, List # Added for strong typing in schema
from data.PDF_page_JSON_schema import PdfDocument



import logging
import concurrent.futures
from multiprocessing import cpu_count, Manager
# import google.generativeai as genai
from google.genai import types
from google import genai
import google
from dotenv import load_dotenv
import functools
import google.api_core
import pprint
import pathlib






load_dotenv()
SYS_INS = ""
MODEL_NAME = "GEMINI_20_FL"
PRO_MODEL_NAME = "GEMINI_20_PRO"
FLASH_MODEL_NAME = "GEMINI_20_FL"
API_KEY_PAID_STR = "API_KEY_PAID"
API_KEY_FREE_STR = "API_KEY_FREE"
OUTPUT_JSON_PATH = "OUTPUT_JSON_PATH"



# Set up logging with timestamp in the desired format (yyyy-mm-dd 24 hr)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s : %(levelname)s : %(message)s",  # Default log format with timestamp, level, and message
    datefmt="%Y-%m-%d %H:%M:%S",  # Timestamp format (yyyy-mm-dd 24 hr)
    handlers=[logging.FileHandler("gemini.log")]  # Output logs to console
)
logger = logging.getLogger(__name__)


# trace_client = trace.Client()



def log_entry_exit(func):
    """Decorator to log function entry and exit with function name."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the logger for the module where the function is defined
        func_logger = logging.getLogger(func.__module__)

        # Log function entry with function name
        func_logger.debug(f"Entering {func.__name__}")

        try:
            result = func(*args, **kwargs)
            return result
        finally:
            # Log function exit with function name
            func_logger.debug(f"Exiting {func.__name__}")

    return wrapper



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



def load_output_file_version_json ():
    global OUTPUT_JSON_PATH
    output_json_path = os.environ.get (OUTPUT_JSON_PATH)
    try:
        with open(output_json_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None



def save_output_file_version_json ():
    global OUTPUT_JSON_PATH
    output_json_path = os.environ.get (OUTPUT_JSON_PATH)
    old_data = load_output_file_version_json ()
    new_data = {}
    

    if not old_data:
        old_data = {
            "version": 0,
            "filename": "./output files/output response v0.json"
        }
    
    new_data ["version"]   = old_data ["version"]   +  1
    new_data ["filepath"]  = f"./output files/output response v{new_data ["version"]}.json"
    
    with open(output_json_path, 'w') as f:
        json.dump(
            obj=new_data, 
            fp=f, 
            indent=4
        )

    return new_data ["filepath"]




def reset_output_file_version ():
    global OUTPUT_JSON_PATH
    output_json_path = os.environ.get (OUTPUT_JSON_PATH)
    old_data = {
        "version": 0,
        "filename": "./output files/output response v0.json"
    }


    with open(output_json_path, 'w') as f:
        json.dump(old_data, f, indent=4)




def configure_genai():
    global SYS_INS, PRO_MODEL_NAME, FLASH_MODEL_NAME, API_KEY_PAID_STR, API_KEY_FREE_STR

    if len(sys.argv) < 3:
        raise ValueError("Model type (pro/flash) and API key type (free/paid) must be provided.")

    SYS_INS = load_system_instructions ()

    model_type = sys.argv[1].lower()
    api_key_type = sys.argv[2].lower()

    if model_type == "pro":
        model_name = os.environ.get(PRO_MODEL_NAME)
    elif model_type == "flash":
        model_name = os.environ.get(FLASH_MODEL_NAME)
    else:
        raise ValueError("Invalid model_type. Must be 'pro' or 'flash'.")

    if api_key_type == "free":
        api_key = os.environ.get(API_KEY_FREE_STR)
        if not api_key:
             raise ValueError(f"The {API_KEY_FREE_STR} environment variable is not set.")

    elif api_key_type == "paid":
        api_key = os.environ.get(API_KEY_PAID_STR)
        if not api_key:
            raise ValueError(f"The {API_KEY_PAID_STR} environment variable is not set.")
    else:
        raise ValueError("Invalid api_key_type. Must be 'free' or 'paid'.")

    client = genai.Client(api_key=api_key)
    return client, model_name




@log_entry_exit
def gen_response(prompts, record):
    """Generate a response from the Gemini API using multiple prompts."""
    # logger.debug("Entering gen_response")
    global SYS_INS
    gemini_response = None
    RESPONSES = []
    client, model_name = configure_genai()  # Initialize the model once
    
    if not prompts:
        logger.error("No prompts provided.")
        raise Exception("No prompts provided")
    
    for prompt in prompts:
        # Append the prompt to the record for context
        record.append(prompt)
        if gemini_response:
            record.append(gemini_response.text)

        try:
            # Call the Gemini API using the client
            if record:
                gemini_response = client.models.generate_content(
                    model=model_name,
                    contents=record,
                    config=types.GenerateContentConfig(
                        system_instruction=SYS_INS,
                        response_mime_type="application/json",
                        response_schema = PdfDocument
                    ) # Pass system instruction via config
                )
            else:
                print ("empty record!!")

            # logger.info(f"Successfully generated response for prompt: {prompt}".rstrip())

        # except google.api_core.exceptions.ResourceExhausted as f:
        #     print("Error: API quota exhausted. Try again later.")
        #     return f"Error: {str(f)}"

        except Exception as e:
            # Log and handle errors appropriately
            logger.error(f"Error generating response for prompt '{prompt}': {e}")
            gemini_response = f"Error: {str(e)}"
            return f"Error: {str(e)}"

        record = []  # Reset the record for the next iteration
        # In this case, we do NOT reset the `record` here, because we need to keep context for subsequent prompts.

    return gemini_response.text

@log_entry_exit
def process_record(record, prompts, results_queue):
    """Process a single record with multiple prompts."""
    try:
        # Generate response based on record and prompts
        # print ("record L136:", [record])
        response = gen_response(prompts, [record])  # Pass record as list
        results_queue.put(response)  # Put the result in the queue
    except Exception as e:
        logger.error(f"Error processing record: {e}")
        results_queue.put(f"Error: {str(e)}")  # Put error message in the queue


@log_entry_exit
def collect_results_from_queue(results_queue):
    """Collect all results from the results_queue."""
    all_responses = []
    while not results_queue.empty():
        response = results_queue.get()
        all_responses.append(response)

    # print (len (all_responses))
    # for res in all_responses:
    #     print (res [:2000], "\n\n\n\n")
    return all_responses


@log_entry_exit
def parallelize_processing(records, prompts):
    """Parallelize the processing of records and prompts using multiprocessing."""
    # global model
    # Get the number of available CPU cores
    num_workers = cpu_count()


    # Create a Manager and get a Queue that can be shared across processes
    with Manager() as manager:
        results_queue = manager.Queue()

        # Use ProcessPoolExecutor for parallel processing
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = []
            for record in records:
                futures.append(executor.submit(process_record, record, prompts, results_queue))


            # Wait for all futures to complete
            concurrent.futures.wait(futures)



        


            # Collecting results from the queue as the workers complete
            all_responses = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    # Ensure the process completes without error
                    future.result()  # If there was an exception in the worker, it will be raised here
                except Exception as e:
                    logger.error(f"Error during future processing: {e}")

            # Now gather all results from the queue
            all_responses = collect_results_from_queue(results_queue)

    return all_responses





def files_content() -> list:
    """
    Reads files from a directory, handling text, markdown, and PDF files.
    Returns a list of file contents (strings for text/markdown, Blobs for PDFs).
    """
    md_directory = './files/'
    records = []

    try:
        for f in os.listdir(md_directory):
            file_path = os.path.join(md_directory, f)

            try:  # Inner try-except for individual file processing
                if f.endswith((".txt", ".md")):
                    with open(file_path, 'r', encoding="utf-8") as file:
                        records.append(file.read())
                elif f.endswith(".pdf"):
                    pathlib_file_path = pathlib.Path(file_path)
                    pdf_part = types.Part.from_bytes (
                        data=pathlib_file_path.read_bytes(),
                        mime_type='application/pdf'
                    )
                    records.append(pdf_part)
                elif f.endswith(".jpeg"):
                     pathlib_file_path = pathlib.Path(file_path)
                     jpeg_part = types.Part.from_bytes(
                         data=pathlib_file_path.read_bytes(),
                         mime_type='image/jpeg'
                     )
                     records.append(jpeg_part)
                else:
                    logger.warning(f"Skipping unsupported file type: {f}")

            except FileNotFoundError:
                logger.error(f"File not found: {file_path}")  # Specific file, not directory
                # Don't exit; continue processing other files
            except OSError as e:
                logger.error(f"OS error reading file {file_path}: {e}")
                # Don't exit; continue processing other files
            except (TypeError, ValueError) as e:
                logger.error(f"Error processing file content {file_path} : {e}")
            except Exception as e:
                logger.error(f"Unexpected error processing {file_path}: {e}")
                # Consider logging stack trace for debugging:
                # logger.exception(f"Unexpected error processing {file_path}: {e}")

        return records  # Return even if some files had errors

    except FileNotFoundError:
        logger.error(f"Directory not found: {md_directory}")
        sys.exit(1)  # Exit if the *directory* is not found
    except OSError as e:
        logger.error(f"OS error accessing directory {md_directory}: {e}")
        sys.exit(1) #exit if cannot access directory
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)  # Exit for unexpected errors at the directory level




def lines_content ():
    # First argument is the file containing records (e.g., links)
    input_file = sys.argv[1]


    try:
        with open(input_file, 'r') as f:
            records = [line.strip() for line in f.readlines()]
            return records
    except FileNotFoundError:
        logger.error(f"File not found: {input_file}")
        sys.exit(1)



async def files_count_tokens_async () -> dict:
    """
    Reads files and "asynchronously" counts tokens (using asyncio.to_thread).
    ONLY uses asyncio.to_thread for count_tokens. File reading is synchronous
    Returns only the files_tokens dictionary.
    """
    
    md_directory = './files/'
    files_tokens = {}
    client, model_name = configure_genai() # Get client and model_name


    async def process_file(file_path):
        nonlocal files_tokens

        if file_path.endswith((".txt", ".md")):
            try:
                # Synchronous file reading:
                with open(file_path, 'r', encoding="utf-8") as f:
                    content = f.read()

                # "Asynchronous" token counting (using asyncio.to_thread):
                token_count = await asyncio.to_thread(client.models.count_tokens, model=model_name, contents=[content])
                files_tokens[file_path] = token_count.total_tokens


            except Exception as e:
                print(f"Error processing {file_path}: {e}", file=sys.stderr)
                files_tokens[file_path] = -1

        elif file_path.endswith(".pdf"):
            try:
                pathlib_file_path = pathlib.Path(file_path)
                content = pathlib_file_path.read_bytes()
                # Create Part directly
                pdf_part = types.Part.from_bytes(data=content, mime_type='application/pdf')
                # "Asynchronous" token counting (using asyncio.to_thread):
                # Note: contents expects a list
                token_count = await asyncio.to_thread(client.models.count_tokens, model=model_name, contents=[pdf_part])
                files_tokens[file_path] = token_count.total_tokens
            except Exception as e:
                print(f"Error processing {file_path}: {e}", file=sys.stderr)
                files_tokens[file_path] = -1
        elif file_path.endswith(".jpeg"):
            try:
                pathlib_file_path = pathlib.Path(file_path)
                content = pathlib_file_path.read_bytes()
                # Create Part directly
                jpeg_part = types.Part.from_bytes(data=content, mime_type='image/jpeg')
                # "Asynchronous" token counting (using asyncio.to_thread):
                # Note: contents expects a list
                token_count = await asyncio.to_thread(client.models.count_tokens, model=model_name, contents=[jpeg_part])
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




@log_entry_exit
def res_agg (base_responses):
    # perform aggregate on base_responses

    try:
        with open("base_prompts.md", "r") as file:
            base_prompt = file.readline().strip()  # Read the first line and remove any trailing whitespace
            agg_prompt  = file.readline().strip()  # Read the second line and remove any trailing whitespace

    except FileNotFoundError:
        print("Error: base_prompts.md not found.")
        base_prompt = ""  # If the file isn't found, set base_prompt to an empty string
        agg_prompt = ""  # If the file isn't found, set agg_prompt to an empty string

    except Exception as e:
        print(f"An error occurred: {e}")

    
    prompts = ""
    custom_agg = input("Enter your custom aggregation prompt if any: ").strip()  # Take user input and strip any extra spaces

    # Append only if custom_agg is not empty
    # Now base_prompt is redundant
    if custom_agg:
        prompts = f"{agg_prompt} {custom_agg}"
    else:
        prompts = f"{agg_prompt}"

    # Log the created prompt
    logger.info(f"Aggregate prompt <agg prompt>: {prompts}")
    base_responses.append (prompts)
    
    # global model
    client, model_name = configure_genai() # Get client and model_name
    # Ensure SYS_INS is loaded (configure_genai loads it globally)



    gemini_response = client.models.generate_content(
        model=model_name,
        contents=base_responses,
        config=types.GenerateContentConfig(system_instruction=SYS_INS) # Pass system instruction via config
    )

    aggregate_responses = [gemini_response.text]
    
    return aggregate_responses







@log_entry_exit
async def main():
    """Main function to read input, parallelize the work, and print the results."""
    logger.critical ("A new run;")
    logger.critical ("<run>")

    prompts = []
    # Interactive loop with break condition
    # while True:
    #     user_input = input('Enter a prompt (or "done" to finish): ')
    #     if user_input.lower() == 'done':
    #         break
    #     # Now prepend_string is redundant
    #     prompt = f"{user_input}"
    #     prompts.append(prompt)
    #     logger.info(f"Prompt added <prompt>: {prompt}")


    user_input = input('Enter a prompt (or "done" to finish): ')
    # Now prepend_string is redundant
    prompt = f"{user_input}"
    prompts.append(prompt)
    logger.info(f"Prompt added <prompt>: {prompt}")

    # print("Modified prompts:", prompts)

    # Prompt user for input
    user_input = input("Choose the content source (1 for files, 2 for lines): ")
    agg_opt = input ("Do you want to perform aggregate operation? 1 for agg, 2 for no agg; ")
    # Assign records based on the input
    if user_input == '1':
        records = files_content()
        try:
            if sys.argv[3].lower() == "count":
                token_count = await files_count_tokens_async()
                pprint.pprint(token_count, indent=4)
        except IndexError:
            pass
        
    elif user_input == '2':
        records = lines_content()
    else:
        # Log error and exit program if the input is invalid
        logger.error(f"Invalid option chosen: {user_input}")
        sys.exit(1)    

    logger.info(f"Starting parallel processing for {len(records)} records with {len(prompts)} prompts.")

    # Parallelize processing
    all_responses = parallelize_processing(records, prompts)
    if (agg_opt == '1'):
        all_responses = res_agg (all_responses)
    else:
        pass


    print (len (all_responses))
    
    # --- Step 1 & 2: Parse each JSON string and collect the objects ---
    parsed_objects_list = []
    for i, json_string in enumerate(all_responses):
        try:
            # Clean potential whitespace just in case
            cleaned_string = json_string.strip()
            if cleaned_string: # Check if string is not empty after stripping
                # Parse the JSON string into a Python object
                python_obj = json.loads(cleaned_string)
                parsed_objects_list.append(python_obj)
            else:
                 print(f"Warning: Skipping empty string at index {i}")
                 # logging.warning(f"Skipping empty string at index {i}")
        except json.JSONDecodeError as e:
            # Handle cases where a string in the list is not valid JSON
            print(f"Error parsing string at index {i}: {e}")
            print(f"Problematic string content (first 100 chars): {json_string[:100]}...")
            # logging.error(f"Error parsing string at index {i}: {e}")
            # logging.error(f"Problematic string content: {json_string[:200]}...")
            # Decide how to handle errors: skip, add placeholder, raise exception?
            # Option: Append an error object
            # parsed_objects_list.append({"error": f"Invalid JSON at index {i}", "details": str(e)})
            continue # Skip this invalid string


    # --- Step 3: Dump the list of Python objects with indentation ---
    output_file_path = save_output_file_version_json ()


    with open(file=output_file_path, mode="w", encoding='utf-8') as f:
        json.dump(
            obj=parsed_objects_list, # Pass the list of PARSED Python objects
            fp=f,
            indent=4                 # Indent will format the list and the objects within it
        )

    print(f"Successfully wrote parsed and indented JSON to {output_file_path}")
    
    logger.critical ("</run>")
    
if __name__ == "__main__":
    # trace_span = client.start_span(name="application_start")
    asyncio.run (main())
    # trace_span.end ()

