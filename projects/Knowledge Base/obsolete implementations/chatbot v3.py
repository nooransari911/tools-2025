import google.generativeai as genai
import os
import sys
import signal
import readline
import threading
from dotenv import load_dotenv

def load_system_instructions():
    """Loads system instructions (unchanged)."""
    instructions_file_path = os.getenv('SYSTEM_INSTRUCTIONS_PATH')
    if instructions_file_path:
        try:
            with open(instructions_file_path, 'r') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading system instructions: {e}")
    return ""

def configure_genai():
    """Configures and returns the Gemini GenerativeModel (unchanged)."""
    PRO_MODEL_NAME = "gemini-1.5-pro-002"
    FLASH_MODEL_NAME = "gemini-1.5-flash-002"
    API_KEY_PAID_STR = "API_KEY_PAID"
    API_KEY_FREE_STR = "API_KEY_FREE"
    SYS_INS = load_system_instructions()

    if len(sys.argv) < 3:
        print("Usage: python your_script.py <pro|flash> <free|paid>")
        sys.exit(1)

    model_type = sys.argv[1].lower()
    api_key_type = sys.argv[2].lower()

    if model_type == "pro":
        model_name = PRO_MODEL_NAME
    elif model_type == "flash":
        model_name = FLASH_MODEL_NAME
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


def run_chatbot():
    load_dotenv()
    model = configure_genai()
    history = []

    # Signal handler (runs in a separate thread)
    def signal_handler(signum, frame):
        if signum == signal.SIGINT:
            nonlocal user_input
            print("^C")
            print("\033[94mYou ^C: \033[0m", end="", flush=True) #print prompt
            user_input = ""

            readline.set_startup_hook(None) #remove hook
            readline.remove_history_item(readline.get_current_history_length() - 1) #remove history
            readline.insert_text ('') #clear input
            readline.redisplay() #redraw prompt

    # Set up the signal handler in a separate thread
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGQUIT, lambda sig, frame: sys.exit(0)) #Ctrl+D
    signal.signal(signal.SIGTSTP, signal.SIG_IGN)  # Ignore Ctrl+Z

    print("\033[92mChatbot started. Type 'exit' to quit or press Ctrl+D.\033[0m")

    while True:
        try:
            print("\033[2K\r", end="", flush=True)  # Clear the line
            user_input = input("\033[94mYou: \033[0m")
            if user_input.lower() == 'exit':
                print("\033[92mChatbot exiting.\033[0m")
                break

            if user_input: # Handle Empty string.
                print (user_input)

                history.append(user_input)
                full_prompt = "\n".join(history)
                try:
                    response = model.generate_content(full_prompt)
                    print("\033[91mChatbot:\033[0m " + response.text)
                    history.append(response.text)
                except Exception as e:
                    print(f"Chatbot: (Error generating response: {e})")

        except EOFError:
            print("\n\033[92mChatbot exiting.\033[0m")
            sys.exit(0)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run_chatbot()
