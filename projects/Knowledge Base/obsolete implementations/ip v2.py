import sys
import signal
import tty
import termios

import google.generativeai as genai
import os
import sys
import signal
import readline
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




def get_char(fd):
    """Reads a single character from stdin."""
    ch = sys.stdin.read(1)
    return ch




def run_chatbot():
    load_dotenv()
    model = configure_genai()
    history = []

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    def restore_terminal():
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def signal_handler_ctrl_d(sig, frame):
        restore_terminal()
        print("\nChatbot exiting")
        sys.exit(0)

    signal.signal(signal.SIGQUIT, signal_handler_ctrl_d)  # Ctrl+D
    signal.signal(signal.SIGTSTP, signal.SIG_IGN)  # Ignore Ctrl+Z
    signal.signal(signal.SIGINT, signal.SIG_IGN)  # Ignore Ctrl+C

    print("Chatbot started. Type 'exit' to quit or press Ctrl+D.")

    try:
        while True:
            print("\033[2K\r", end="", flush=True)  # Clear the line
            print("You: ", end="", flush=True)  # Initial prompt
            user_input = ""
            tty.setraw(fd)  # Set raw mode for each input

            try:
                while True:
                    char = get_char(fd)

                    if char == '\x03':  # Ctrl+C
                        raise KeyboardInterrupt

                    elif char == '\x04':  # Ctrl+D
                        raise EOFError

                    elif char == '\r' or char == '\n':
                        # print() #explain this
                        break

                    elif char == '\x7f':  # Backspace
                        if user_input:
                            user_input = user_input[:-1]
                            print('\b \b', end="", flush=True)
                    else:
                        user_input += char
                        print(char, end="", flush=True)

            except KeyboardInterrupt:
                print("^C")
                restore_terminal()
                continue  # Go back to the beginning of the outer loop

            finally:
                restore_terminal()

            if user_input.lower() == 'exit':
                break

            # print("\nchatbot: this is a simulated response.", user_input, "\n\n")
            print ("\n")

            if user_input: #handle empty
                history.append(user_input)
                full_prompt = "\n".join(history)
                try:
                    response = model.generate_content(full_prompt)
                    print("\033[91mChatbot:\033[0m", response.text)
                    history.append(response.text)
                except Exception as e:
                    print(f"Chatbot: (Error generating response: {e})")




    except EOFError:
        print("\nChatbot exiting")
    finally:
        restore_terminal()  # Always restore terminal settings

if __name__ == "__main__":
    run_chatbot()
