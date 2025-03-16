import google.generativeai as genai
import os, time
import sys
import signal
import readline
from dotenv import load_dotenv





PRO_MODEL_NAME = "GEMINI_20_PRO"
FLASH_MODEL_NAME = "GEMINI_20_FL"
API_KEY_PAID_STR = "API_KEY_PAID"
API_KEY_FREE_STR = "API_KEY_FREE"





def load_system_instructions():
    instructions_file_path = os.getenv('SYSTEM_INSTRUCTIONS_PATH')
    if instructions_file_path:
        try:
            with open(instructions_file_path, 'r') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading system instructions: {e}")
    return ""

def configure_genai():
    global API_KEY_FREE_STR, API_KEY_PAID_STR, PRO_MODEL_NAME, FLASH_MODEL_NAME


    SYS_INS = load_system_instructions()

    if len(sys.argv) < 3:
        print("Usage: python your_script.py <pro|flash> <free|paid>")
        sys.exit(1)

    model_type = sys.argv[1].lower()
    api_key_type = sys.argv[2].lower()

    if model_type == "pro":
        model_name = os.getenv (PRO_MODEL_NAME)
    elif model_type == "flash":
        model_name = os.getenv (FLASH_MODEL_NAME)
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
    user_input = ""

    # print (dir (model.start_chat ().send_message ("say Hi")))
    # print (model.start_chat ().send_message ("say Hi").usage_metadata)
    # print (model.start_chat ().send_message ("say Hi"))
    # print (model)
    
    
    print("\033[92mChatbot started. Type 'exit' to quit or press Ctrl+D.\033[0m")

    while True:
        try:
            # readline.set_pre_input_hook(pre_input_hook)
            # print("\033[2K\r", end="", flush=True)  # Clear the line
            user_input = input("\033[94mYou: \033[0m")

            if user_input.lower() == 'exit':
                print("\033[92mChatbot exiting.\033[0m")
                break

            if user_input:
                # print (user_input)
                history.append(user_input)
                full_prompt = "\n".join(history)
                try:
                    start_time = time.time ()
                    response = model.generate_content(full_prompt)
                    end_time = time.time ()
                    elapsed_time = end_time - start_time



                    print(f"\033[91mChatbot ({elapsed_time:.2f}s):\033[0m\n" + response.text + "\n")
                    history.append(response.text)
                except Exception as e:
                    print(f"Chatbot: (Error generating response: {e})")

        except KeyboardInterrupt: #still can be raised
            print("^C")
            readline.insert_text ('')
            user_input = ""
            continue


        except EOFError:
            print("\n\033[92mChatbot exiting.\033[0m")
            sys.exit(0)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run_chatbot()
