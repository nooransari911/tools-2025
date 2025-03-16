import google.generativeai as genai
import os
import sys
import signal
import time
from dotenv import load_dotenv

# Use the requested environment variable names:
PRO_MODEL_NAME = "GEMINI_20_PRO"
FLASH_MODEL_NAME = "GEMINI_20_FL"
API_KEY_PAID_STR = "API_KEY_PAID"
API_KEY_FREE_STR = "API_KEY_FREE"
SYS_INS = ""

def load_system_instructions():
    """Loads system instructions from a file."""
    global SYS_INS
    instructions_file_path = os.getenv('SYSTEM_INSTRUCTIONS_PATH')
    if instructions_file_path:
        try:
            with open(instructions_file_path, 'r') as file:
                SYS_INS = file.read()
        except Exception as e:
            print(f"Error reading system instructions: {e}")

def configure_genai():
    """Configures and returns the Gemini GenerativeModel."""
    global PRO_MODEL_NAME, FLASH_MODEL_NAME, API_KEY_PAID_STR, API_KEY_FREE_STR, SYS_INS

    load_system_instructions()

    if len(sys.argv) < 3:
        print("Usage: python your_script.py <pro|flash> <free|paid>")
        sys.exit(1)

    model_type = sys.argv[1].lower()
    api_key_type = sys.argv[2].lower()

    if model_type == "pro":
        model_name = os.getenv(PRO_MODEL_NAME)
        if not model_name:
            print(f"Error: {PRO_MODEL_NAME} environment variable not set.")
            sys.exit(1)
    elif model_type == "flash":
        model_name = os.getenv(FLASH_MODEL_NAME)
        if not model_name:
            print(f"Error: {FLASH_MODEL_NAME} environment variable not set.")
            sys.exit(1)
    else:
        print("Invalid model_type. Must be 'pro' or 'flash'.")
        sys.exit(1)

    if api_key_type == "free":
        api_key = os.getenv(API_KEY_FREE_STR)
    elif api_key_type == "paid":
        api_key = os.getenv(API_KEY_PAID_STR)
    else:
        print("Invalid api_key_type. Must be 'free' or 'paid'.")
        sys.exit(1)

    if not api_key:
        print(f"Error: Required API key environment variable not set ({api_key_type}).")
        sys.exit(1)

    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name=model_name, system_instruction=SYS_INS)

def get_multiline_input(ip_prompt):
    """Reads multi-line input from the user until EOF (Ctrl+D).
       Returns None if Ctrl+C is pressed during input.
    """
    print(ip_prompt, end="", flush=True)
    try:
        user_input = sys.stdin.read()
        return user_input
    except KeyboardInterrupt:
        print("^C")  # Show ^C
        return None  # Signal to reset prompt

def run_chatbot():
    """Runs a CLI chatbot."""
    load_dotenv()
    model = configure_genai()
    history = []  # Keep track of conversation history

    def signal_handler(sig, frame):
        """Handles Ctrl+C to exit the program."""
        print("^C")
        print("\033[92mChatbot exiting (Ctrl+C).\033[0m")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)  # Register for program exit

    print("\033[92mChatbot started. Type 'exit' to quit, Ctrl+C to exit, or Ctrl+D to submit.\033[0m")

    while True:
        user_input = get_multiline_input("\033[94mYou: (Press Ctrl+D to finish input, Ctrl+C to clear)\033[0m")

        if user_input is None:  # Ctrl+C during input
            history = [] #Clear History
            continue      # Restart the loop, clear input

        if "exit" in user_input.lower():
            print("\033[92mChatbot exiting.\033[0m")
            break

        if not user_input.strip():  # Handle empty input after Ctrl+D
            continue


        history.append(user_input) # Append the user's input to the history
        full_prompt = "\n".join(history) # Use the complete history

        try:
            response = model.generate_content(full_prompt)
            response_text = response.text
        except Exception as e:
            response_text = f"Chatbot: (Error generating response: {e})"

        print(f"\033[91mChatbot:\033[0m {response_text}")
        history.append(response_text) #Append chatbot response to history


if __name__ == "__main__":
    run_chatbot()
