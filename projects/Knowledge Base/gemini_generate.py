import sys
import os
import logging
import concurrent.futures
from multiprocessing import cpu_count, Manager
import google.generativeai as genai
from dotenv import load_dotenv
import time
import pyperclip
import functools








load_dotenv()

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







# Initialize the API once
def configure_genai():
    genai.configure(api_key=os.environ["API_KEY_PAID"])
    return genai.GenerativeModel(os.environ["GEMINI_20_FL"])








@log_entry_exit
def gen_response(prompts, record):
    """Generate a response from the Gemini API using multiple prompts."""
    # logger.debug("Entering gen_response")
    gemini_response = None
    RESPONSES = []
    model = configure_genai()  # Initialize the model once



    
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
            # Call the Gemini API to generate a response based on the combined record and prompt list
            gemini_response = model.generate_content(record)
            logger.info(f"Successfully generated response for prompt: {prompt}".rstrip())
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






def files_content ():
    md_directory = './md/'

    try:
        # Get all .md files in the directory
        records = [open(os.path.join(md_directory, f), 'r').read() for f in os.listdir(md_directory) if f.endswith('.md')]
        return records
    except FileNotFoundError:
        logger.error(f"Directory not found: {md_directory}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)




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
    prompts = f"{base_prompt} {agg_prompt}"

    base_responses.append (prompts)
    
    # global model
    model = configure_genai ()




    gemini_response = model.generate_content (base_responses)
    aggregate_responses = [gemini_response.text]
    
    return aggregate_responses














@log_entry_exit
def main():
    """Main function to read input, parallelize the work, and print the results."""
    if len(sys.argv) < 1:
        logger.error("Insufficient arguments provided. You need to provide at least one record and one prompt.")
        sys.exit(1)


    logger.critical ("A new run;")
    logger.critical ("<run>")



    # Remaining arguments are the prompts
    # prompts = sys.argv[2:]

    # Read the prepend string from base_prompts.md
    try:
        with open("base_prompts.md", "r") as file:
            prepend_string = file.readline().strip()  # Read the first line and remove any trailing whitespace
    except FileNotFoundError:
        print("Error: base_prompts.md not found.")
        prepend_string = ""  # If the file isn't found, set prepend_string to an empty string

    # Modify sys.argv[2:] by adding the prepend string before each prompt
    # prompts = [f"{prepend_string} {prompt}" for prompt in sys.argv[2:]]


    prompts = []
    # prepend_string = "Your prepend string here"

    # Interactive loop with break condition
    while True:
        user_input = input('Enter a prompt (or "done" to finish): ')
        if user_input.lower() == 'done':
            break
        prompts.append(f"{prepend_string} {user_input}")








    # print("Modified prompts:", prompts)

    # Prompt user for input
    user_input = input("Choose the content source (1 for files, 2 for lines): ")
    agg_opt = input ("Do you want to perform aggregate operation? 1 for agg, 2 for no agg; ")
    # Assign records based on the input
    if user_input == '1':
        records = files_content()
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
        logger.info(f"Responses for record {i + 1}:\n{responses}".rstrip())
    # for i, responses in enumerate(all_responses):
    #     print(f"{responses.rstrip()}")


    if (agg_opt == '1'):
        all_responses = res_agg (all_responses)
    else:
        pass



    # Clean and print all responses, then copy them to the clipboard
    cleaned_responses = "\n\n".join(responses.rstrip() for responses in all_responses)
    # logger.info(cleaned_responses)
    print(cleaned_responses)  # Print the cleaned responses
    # pyperclip.copy(cleaned_responses)  # Copy them to the clipboard


    with open("links_base.md", "w") as file:
        file.write(cleaned_responses + "\n\n")



    
    logger.critical ("</run>")












    
if __name__ == "__main__":
    # trace_span = client.start_span(name="application_start")
    main()
    # trace_span.end ()

