import google.generativeai as genai
import os
import sys
import signal
from dotenv import load_dotenv
import readline  # Import readline for better input handling

def load_system_instructions():
    """Loads system instructions from a file."""
    instructions_file_path = os.getenv('SYSTEM_INSTRUCTIONS_PATH')
    if instructions_file_path:
        try:
            with open(instructions_file_path, 'r') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading system instructions: {e}")
    return ""

def configure_genai():
    """Configures and returns the Gemini GenerativeModel."""
    PRO_MODEL_NAME = "gemini-1.5-pro-002"  # Use correct model names
    FLASH_MODEL_NAME = "gemini-1.5-flash-002"  # Use correct model names
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
    """Runs a simple CLI chatbot with improved UI."""

    load_dotenv()
    model = configure_genai()

    def signal_handler(sig, frame):
        print("\nChatbot exiting gracefully...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    print("\033[92mChatbot started. Type 'exit' to quit or press Ctrl+C.\033[0m")  # Green start message

    history = []  # Conversation history

    while True:
        try:
            user_input = get_multiline_input ("\033[94mYou: \033[0m")
            if user_input.lower() == 'exit':
                print("\033[92mChatbot exiting.\033[0m") # Green exit message
                break

            history.append(user_input)
            # Combine history with current input for context
            full_prompt = "\n".join(history)

            response = model.generate_content(full_prompt)

            # Handle potential errors within the response (e.g., safety filters)
            try:
                response_text = response.text
            except RuntimeError as e:
                response_text = f"Chatbot: (Error generating response: {e})"

            print("\033[91mChatbot:\033[0m", response_text)  # Red "Chatbot:"

            history.append(response_text)  # Add bot response to history


        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_chatbot()
