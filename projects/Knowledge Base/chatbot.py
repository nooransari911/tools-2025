import google.generativeai as genai
from google.genai import types
from google import genai as gemini
import os, time
import sys
import signal
import readline
from dotenv import load_dotenv
import pathlib





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
    # return gemini.Client (api_key=api_key)





def files_content() -> list:
    """
    Reads files from a directory, handling text, markdown, and PDF files.
    Returns a list of file contents (strings for text/markdown, Blobs for PDFs).
    """
    md_directory = './chat/files/'
    records = []

    try:
        for f in os.listdir(md_directory):
            file_path = os.path.join(md_directory, f)

            try:  # Inner try-except for individual file processing
                if f.endswith((".txt", ".md")):
                    with open(file_path, 'r', encoding="utf-8") as file:
                        records.append(file.read())
                elif f.endswith((".pdf")):
                    pathlib_file_path = pathlib.Path(file_path)
                    content = types.Part.from_bytes(
                        data=pathlib_file_path.read_bytes(),
                        mime_type='application/pdf',
                    ).inline_data

                    blob = genai.protos.Blob (
                        data=content.data,
                        mime_type=content.mime_type
                    )
                    # print ("\nIs blob an instance of protos.Blob?: ", isinstance (blob, google.generativeai.protos.Blob), "\n")
                    # print (len (content.data))
                    records.append(blob)

                elif f.endswith((".png")):
                    pathlib_file_path = pathlib.Path(file_path)
                    content = types.Part.from_bytes(
                        data=pathlib_file_path.read_bytes(),
                        mime_type='image/png',
                    ).inline_data

                    blob = genai.protos.Blob (
                        data=content.data,
                        mime_type=content.mime_type
                    )
                    # print ("\nIs blob an instance of protos.Blob?: ", isinstance (blob, google.generativeai.protos.Blob), "\n")
                    # print (len (content.data))
                    records.append(blob)


                else:
                    print (f"Skipping unsupported file type: {f}")

            except FileNotFoundError:
                print (f"File not found: {file_path}")  # Specific file, not directory
                # Don't exit; continue processing other files
            except OSError as e:
                print (f"OS error reading file {file_path}: {e}")
                # Don't exit; continue processing other files
            except (TypeError, ValueError) as e:
                print (f"Error processing file content {file_path} : {e}")
            except Exception as e:
                print (f"Unexpected error processing {file_path}: {e}")
                # Consider logging stack trace for debugging:
                # print (f"Unexpected error processing {file_path}: {e}")

        return records  # Return even if some files had errors

    except FileNotFoundError:
        print (f"Directory not found: {md_directory}")
        sys.exit(1)  # Exit if the *directory* is not found
    except OSError as e:
        print (f"OS error accessing directory {md_directory}: {e}")
        sys.exit(1) #exit if cannot access directory
    except Exception as e:
        print (f"An unexpected error occurred: {e}")
        sys.exit(1)  # Exit for unexpected errors at the directory level









def run_chatbot():
    load_dotenv()
    model = configure_genai()
    # model = gemini.Client ()

    user_input = ""
    records = []

    # print (dir (model.start_chat ().send_message ("say Hi")))
    # print (model.start_chat ().send_message ("say Hi").usage_metadata.candidates_token_count)
    # print (model.start_chat ().send_message ("say Hi"))
    # print (model)

    # try:
    #     if sys.argv[3].lower() == "file":
    #         records = files_content ()
    # except IndexError:
    #     pass

    # session = model.start_chat (history=[
    #                                 types.Content (
    #                                     role="user",
    #                                     parts=[types.Part(records)]
    #                                 )
    #                             ])

    session = model.start_chat ()
    
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
                try:
                    start_time = time.time ()
                    response = session.send_message (user_input)
                    end_time = time.time ()
                    elapsed_time = end_time - start_time
                    tokens_count = response.usage_metadata.candidates_token_count



                    print(f"\033[91mChatbot ({elapsed_time:.2f}s, {tokens_count}):\033[0m\n" + response.text + "\n")
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
