import sys, os, re
import time
import signal
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()






# Define the gen_response function
def gen_response(prompt_list, record):
    genai.configure(api_key=os.environ["API_KEY_PAID"])

    model = genai.GenerativeModel(os.environ["GEMINI_20_FL"])


    
    gemini_response = None
    RESPONSES = []

    if not prompt_list:
        raise Exception("No prompts")
        return "No prompts"

    for pri in prompt_list:
        record.append(pri)
        if gemini_response:
            record.append(gemini_response.text)

        try:
            gemini_response = model.generate_content(record)  # Define your model here
            RESPONSES.append(gemini_response.text)
        except Exception as e:
            gemini_response = f"Error: {str(e)}"
            RESPONSES.append(f"Error: {str(e)}")
            return f"Error: {str(e)}"

        record = []

    return gemini_response.text

def main():
    # Step 1: Get the record (line from the file) and prompt list passed from Bash
    record = sys.argv[1]  # First argument is the record (line from the file)
    prompt_list = sys.argv[2:]  # Remaining arguments are the prompts

    # Step 2: Process the record and get the response
    response = gen_response(prompt_list, [record])  # Pass record and prompts to gen_response
    print(response)  # Handle or log the response

if __name__ == "__main__":
    main()

