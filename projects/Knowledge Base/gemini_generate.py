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
PRO_MODEL_NAME = "GEMINI_20_PRO"
FLASH_MODEL_NAME = "GEMINI_20_FL"
API_KEY_PAID_STR = "API_KEY_PAID"
API_KEY_FREE_STR = "API_KEY_FREE"



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



    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name=model_name,
        system_instruction=SYS_INS
    )






@log_entry_exit
def gen_response(prompts, record):
    """Generate a response from the Gemini API using multiple prompts."""
    # logger.debug("Entering gen_response")
    gemini_response = None
    RESPONSES = []
    model = configure_genai()  # Initialize the model once
    # print ("record L101:", record, "\n")
    # print (len (record))

    
    if not prompts:
        logger.error("No prompts provided.")
        raise Exception("No prompts provided")
    
    for prompt in prompts:
        # Append the prompt to the record for context
        record.append(prompt)
        if gemini_response:
            # Add the previous response to the record for context
            record.append(gemini_response.text)

        try:
            # print ()
            # Call the Gemini API to generate a response based on the combined record and prompt list
            gemini_response = model.generate_content (contents=record)
            # logger.info(f"Successfully generated response for prompt: {prompt}".rstrip())

        except google.api_core.exceptions.ResourceExhausted as f:
            print("Error: API quota exhausted. Try again later.")
            return f"Error: {str(f)}"

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

    logger.info (f"Number of responses processed: {len (all_responses)}")
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
                    content = types.Part.from_bytes(
                        data=pathlib_file_path.read_bytes(),
                        mime_type='application/pdf',
                    ).inline_data

                    blob = google.generativeai.protos.Blob (
                        data=content.data,
                        mime_type=content.mime_type
                    )
                    # print ("\nIs blob an instance of protos.Blob?: ", isinstance (blob, google.generativeai.protos.Blob), "\n")
                    # print (len (content.data))
                    records.append(blob)
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
    model = configure_genai ()




    gemini_response = model.generate_content (base_responses)
    aggregate_responses = [gemini_response.text]
    
    return aggregate_responses







@log_entry_exit
async def main():
    """Main function to read input, parallelize the work, and print the results."""
    logger.critical ("A new run;")
    logger.critical ("<run>")



    # Remaining arguments are the prompts
    # prompts = sys.argv[2:]

    # # Read the prepend string from base_prompts.md
    # try:
    #     with open("base_prompts.md", "r") as file:
    #         prepend_string = file.readline().strip()  # Read the first line and remove any trailing whitespace
    # except FileNotFoundError:
    #     print("Error: base_prompts.md not found.")
    #     prepend_string = ""  # If the file isn't found, set prepend_string to an empty string

    # Modify sys.argv[2:] by adding the prepend string before each prompt
    # prompts = [f"{prepend_string} {prompt}" for prompt in sys.argv[2:]]


    prompts = []
    # prepend_string = "Your prepend string here"

    # Interactive loop with break condition
    while True:
        user_input = input('Enter a prompt (or "done" to finish): ')
        if user_input.lower() == 'done':
            break
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

    # Output results
    for i, responses in enumerate(all_responses):
        # logger.info(f"Responses for record {i + 1}:\n{responses}".rstrip())
        pass
    # for i, responses in enumerate(all_responses):
    #     print(f"{responses.rstrip()}")


    if (agg_opt == '1'):
        all_responses = res_agg (all_responses)
    else:
        pass



    # Clean and print all responses, then copy them to the clipboard
    cleaned_responses = "\n\n".join(responses.rstrip() for responses in all_responses)
    # logger.info(cleaned_responses)
    # print(cleaned_responses)  # Print the cleaned responses
    # pyperclip.copy(cleaned_responses)  # Copy them to the clipboard

    # print (cleaned_responses)
    with open("output_response.md", "w") as file:
        file.write(cleaned_responses + "\n\n")



    
    logger.critical ("</run>")












    
if __name__ == "__main__":
    # trace_span = client.start_span(name="application_start")
    asyncio.run (main())
    # trace_span.end ()

