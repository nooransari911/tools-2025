import sys
import os
import logging
import concurrent.futures
import google.generativeai as genai
from dotenv import load_dotenv
import time
import pyperclip












load_dotenv()

# Set up logging with timestamp in the desired format (yyyy-mm-dd 24 hr)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s : %(levelname)s : %(message)s",  # Default log format with timestamp, level, and message
    datefmt="%Y-%m-%d %H:%M:%S",  # Timestamp format (yyyy-mm-dd 24 hr)
    handlers=[logging.StreamHandler()]  # Output logs to console
)
logger = logging.getLogger()

# Initialize the API once
def configure_genai():
    genai.configure(api_key=os.environ["API_KEY_PAID"])
    return genai.GenerativeModel(os.environ["GEMINI_20_FL"])

def gen_response(prompts, record, model):
    """Generate a response from the Gemini API using multiple prompts."""
    gemini_response = None
    RESPONSES = []

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
            # RESPONSES.append(gemini_response.text)
            logger.info(f"Successfully generated response for prompt: {prompt}")
        except Exception as e:
            # Log and handle errors appropriately
            logger.error(f"Error generating response for prompt '{prompt}': {e}")
            gemini_response = f"Error: {str(e)}"
            # RESPONSES.append(f"Error: {str(e)}")
            return f"Error: {str(e)}"

        record = []
        # Reset the record for the next iteration
        # In this case, we do NOT reset the `record` here, because we need to keep context for subsequent prompts.

    return gemini_response.text

def process_record(record, prompts, model):
    """Process a single record with multiple prompts."""
    response = gen_response(prompts, [record], model)  # Pass record as list
    return response

def parallelize_processing(records, prompts):
    """Parallelize the processing of records and prompts using concurrent.futures."""
    model = configure_genai()  # Initialize the model once

    # Use ThreadPoolExecutor for I/O-bound tasks like API calls
    with concurrent.futures.ThreadPoolExecutor(max_workers=2000) as executor:
        futures = []
        for record in records:
            futures.append(executor.submit(process_record, record, prompts, model))

        all_responses = []
        for future in concurrent.futures.as_completed(futures):
            try:
                all_responses.append(future.result())
            except Exception as e:
                logger.error(f"Error processing future: {e}")

        return all_responses

def main():
    """Main function to read input, parallelize the work, and print the results."""
    if len(sys.argv) < 3:
        logger.error("Insufficient arguments provided. You need to provide at least one record and one prompt.")
        sys.exit(1)

    # First argument is the file containing records (e.g., links)
    input_file = sys.argv[1]

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
    prompts = [f"{prepend_string} {prompt}" for prompt in sys.argv[2:]]
    # print("Modified prompts:", prompts)



    
    try:
        with open(input_file, 'r') as f:
            records = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        logger.error(f"File not found: {input_file}")
        sys.exit(1)

    logger.info(f"Starting parallel processing for {len(records)} records with {len(prompts)} prompts.")

    # Parallelize processing
    all_responses = parallelize_processing(records, prompts)

    # Output results
    for i, responses in enumerate(all_responses):
        logger.info(f"Responses for record {i + 1}:\n{responses}")
    # for i, responses in enumerate(all_responses):
    #     print(f"{responses.rstrip()}")


    # Clean and print all responses, then copy them to the clipboard
    cleaned_responses = "\n".join(responses.rstrip() for responses in all_responses)
    print(cleaned_responses)  # Print the cleaned responses
    # pyperclip.copy(cleaned_responses)  # Copy them to the clipboard


    with open("links_base.md", "a") as file:
        file.write(cleaned_responses + "\n\n")








    
if __name__ == "__main__":
    main()

