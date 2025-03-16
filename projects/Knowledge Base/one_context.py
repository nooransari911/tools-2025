import sys
import os, signal, atexit
import concurrent.futures
from multiprocessing import cpu_count, Manager
import google.generativeai as genai
from google.genai import types
from dotenv import load_dotenv
import pathlib
import logging
import functools
import readline
import pprint, json





# --- Configuration and Setup ---
load_dotenv()
SYS_INS = ""
MODEL_NAME = "GEMINI_20_FL"  # Placeholder
PRO_MODEL_NAME = "GEMINI_20_PRO"
FLASH_MODEL_NAME = "GEMINI_20_FL"
API_KEY_PAID_STR = "API_KEY_PAID"
API_KEY_FREE_STR = "API_KEY_FREE"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("gemini_one_context.log")]
    # handlers=[logging.FileHandler("gemini_one_context.log")]
)
logger = logging.getLogger(__name__)

def log_entry_exit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Entering {func.__name__}")
        try:
            return func(*args, **kwargs)
        finally:
            logger.debug(f"Exiting {func.__name__}")
    return wrapper



def handle_sigpipe(signum, frame):
    print("SIGPIPE on stdout", file=sys.stdout)
    print("SIGPIPE on stderr", file=sys.stderr)
    logging.warning("SIGPIPE Warning: Attempting to write to a closed pipe....")

signal.signal (signal.SIGPIPE, handle_sigpipe)


def at_exit_function():
    print("atexit function called", file=sys.stderr)
    logging.info("atexit function called")

atexit.register(at_exit_function)


# Utility Functions

def load_system_instructions():
    """Loads system instructions."""
    global SYS_INS
    instructions_file_path = os.getenv('SYSTEM_INSTRUCTIONS_PATH')
    if instructions_file_path:
        try:
            with open(instructions_file_path, 'r') as file:
                SYS_INS = file.read()
        except Exception as e:
            logger.error(f"Error reading system instructions file: {e}")
    else:
        logger.warning("Environment variable 'SYSTEM_INSTRUCTIONS_PATH' not set.")

def configure_genai():
    """Configures the Gemini API."""
    global SYS_INS, PRO_MODEL_NAME, FLASH_MODEL_NAME, API_KEY_PAID_STR, API_KEY_FREE_STR

    if len(sys.argv) < 4:
        raise ValueError("Model type, API key type, and root/noroot must be provided.")


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

    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name=model_name, system_instruction=SYS_INS)



@log_entry_exit
def gen_response(prompt, record):
    """Generates a response."""
    model = configure_genai()
    # print (type (prompt))
    contents = record + prompt
    try:
        response = model.generate_content(contents=contents)
        # print ("<response>: ", response.text [:100], "\n\n")
        logger.debug(f"Response length: {len(response.text)}") #Best Practice
        return response.text
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return f"Error: {e}"

@log_entry_exit
def process_record(directory, record, prompt, results_dict):
    """Processes a single record and stores result in a dictionary."""
    response = gen_response(prompt, record)
    results_dict[directory] = response  # Use directory as the key

@log_entry_exit
def collect_results_from_queue(results_queue):
    """Collects results from the queue."""
    all_responses = []
    while not results_queue.empty():
        response = results_queue.get()
        all_responses.append(response)
    return all_responses




@log_entry_exit
def parallelize_processing(directories, prompt):
    """Parallelizes processing using a dictionary for results."""
    num_workers = cpu_count()

    with Manager() as manager:
        results_dict = manager.dict()  # Use a managed dictionary

        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = []
            for directory in directories:
                record = files_content(directory)
                if not record:
                    continue
                # Pass directory to process_record
                futures.append(executor.submit(process_record, directory, record, prompt, results_dict))

            concurrent.futures.wait(futures)
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()  # Check for errors
                except Exception as e:
                    logger.error(f"Error during future processing: {e}")


        use_json = True
        filename = "rawresult.json"

        try:
            with open(filename, 'w') as f:
                if use_json:
                    json.dump(results_dict.copy (), f, indent=4)  # Use JSON with indentation
                else:
                    pprint.pprint(results_dict, stream=f) # Use pprint
        except Exception as e:
            logger.error (f"Error writing to file: {e}")




        # No need for collect_results_from_queue
        write_results_to_files(directories, results_dict)  # Pass the dictionary
    return list(results_dict.values()) #return values





@log_entry_exit
def files_content(directory_path) -> list:
    """Reads files from a directory."""
    records = []
    if not os.path.isdir(directory_path):
        logger.error(f"'{directory_path}' is not a valid directory.")
        return records

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            try:
                if filename.endswith((".txt", ".md")):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        records.append(f.read())
                elif filename.endswith(".pdf"):
                    pathlib_file_path = pathlib.Path(file_path)
                    part = types.Part.from_bytes(data=pathlib_file_path.read_bytes(), mime_type="application/pdf").inline_data
                    blob = genai.protos.Blob (data=part.data, mime_type=part.mime_type)
                    # blob = genai.types.Blob(data=part.data, mime_type=part.mime_type)
                    records.append(blob)
                else:
                    logger.warning(f"Unsupported file type: {file_path}")
            except Exception as e:
                logger.error(f"Error reading file {file_path}: {e}")
        else:
            logger.warning(f"Skipping non-file: {file_path}")
    return records




@log_entry_exit
def write_results_to_files(directories, results_dict):
    """Writes results to separate output files, using the results dictionary."""
    for i, directory in enumerate(directories):
        output_file_name = f"output_{i + 1}.md"
        with open(output_file_name, 'w') as outfile:
            outfile.write(f"# Directory: {directory}\n\n")
            # Get response directly from the dictionary using the directory as key
            if directory in results_dict:
                outfile.write(results_dict[directory])
                outfile.write("\n\n")
            else:
                logger.warning(f"No response found for directory: {directory}")
        logger.info(f"Responses for directory {directory} written to {output_file_name}")






def get_user_prompts():
    """Gets prompts interactively."""
    prompts = []
    while True:
        try:
            user_input = input('Enter a prompt (or "done" to finish): ')
        except KeyboardInterrupt: #still can be raised
            print("^C")
            readline.insert_text ('')
            user_input = ""
            continue

        except EOFError:
            print ("^D\nExiting")
            sys.exit (0)
        
        if user_input.lower() == 'done':
            break
        prompts.append(user_input)
    return prompts

def get_directories(root_or_noroot, remaining_args):
    """Gets the list of directories."""
    if root_or_noroot == "root":
        root_dir = remaining_args[0]
        if not os.path.isdir(root_dir):
            raise ValueError(f"'{root_dir}' is not a valid directory.")
        all_dirs = sorted([os.path.join(root_dir, d) for d in os.listdir(root_dir)])
        all_dirs = [d for d in all_dirs if os.path.isdir(d)]
        return all_dirs[:5]  # First 5
    elif root_or_noroot == "noroot":
        return remaining_args
    else:
        raise ValueError("Invalid option. Must be 'root' or 'noroot'.")

@log_entry_exit
def main():
    """Main function."""
    load_system_instructions()

    if len(sys.argv) < 4:
        logger.error("Usage: python script.py <pro/flash> <free/paid> <root/noroot> [<root_dir> | <dir1> <dir2> ...]")
        sys.exit(1)

    root_or_noroot = sys.argv[3].lower()
    remaining_args = sys.argv[4:]

    # Get directories with its own try-except block
    try:
        directories = get_directories(root_or_noroot, remaining_args)
        # print (directories)
        if not directories: #check for empty list
            logger.error("No directories to process.")
            sys.exit(1)
    except ValueError as e:
        logger.error(f"Error getting directories: {e}")
        sys.exit(1)



    directories.sort ()

    # Get prompts with its own try-except block
    try:
        # prompts = get_user_prompts()
        # prompts = ["summarize this with a proper H1 heading at top"]
        prompts = get_user_prompts ()
        
        if not prompts: #check for emtpry list
            logger.error("No prompts entered. Exiting.")
            sys.exit(1)
        # prompt = ' '.join(prompts)
    except Exception as e:
        logger.error(f"Error getting prompts: {e}")
        sys.exit(1)

    # print ("main", type (prompts))

    try:
       all_responses = parallelize_processing(directories, prompts)
       print("All directories processed. Check output files")
    except Exception as e: #Catch any other exception
        logger.error (f"An exception occurred: {e}")
        # sys.exit(1)



if __name__ == "__main__":
    main()
