#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A chatbot script to interact with Fireworks.ai models.
This is a complete port of an original script that used Google Cloud Vertex AI.
All original functions are included, with modifications isolated to the service provider interface.
"""

import os, re
import sys
import time
from datetime import datetime
import uuid
import readline
import base64
import json
import pathlib
import logging
import http.client
import requests  # --- MODIFIED: Replaced Anthropic SDK with requests

from dotenv import load_dotenv
from requests.sessions import Request

# Assuming a user-provided utility module exists at this path
from src.utils import gemini_utils as utils

#from fireworks import LLM


# --- Basic Setup ---
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# Ensure the .env path is correct for your environment
load_dotenv("/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/.env")





# http.client.HTTPConnection.debuglevel = 1
# requests_log = logging.getLogger("urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True




# --- MODIFIED: Fireworks.ai Configuration (Replaces Vertex AI Config) ---
# Strip leading/trailing whitespace and newlines from the key
AWS_API_GW_API_KEY = os.getenv ("AWS_API_GW_API_KEY").strip ()
if not AWS_API_GW_API_KEY:
    logger.warn ("WARNING: AWS API GW API KEY is not set")
API_KEY = os.getenv("FIREWORKS_API_KEY").strip()


AWS_API_GW = "https://z8sw7kg1o2.execute-api.us-west-2.amazonaws.com/v1-initial/api/AI/logs"
API_URL = "https://api.fireworks.ai/inference/v1/chat/completions"
#API_URL = "https://webhook.site/c39f67cc-7bc7-46d1-ab68-dca68eba4dac"

# --- Application Configuration (Unchanged) ---
TOKENS_STORE_JSON_FILE_NAME = os.getenv("CLAUDE_TOKENS_STORE_JSON_FILE_NAME")
SESSION_ID = str (uuid.uuid4 ())
logger.info (f"SESSION ID: {SESSION_ID}")


def validate_api_key():
    """
    Validates that the Fireworks API key is set.
    This function replaces the `configure_vertex_client` function.
    """
    if not API_KEY:
        logger.error("FATAL: FIREWORKS_API_KEY environment variable not set.")
        sys.exit(1)
    logger.info("Fireworks.ai API key configured successfully.")


# --- UNCHANGED FUNCTIONS: The following functions are provider-agnostic ---

def load_system_instructions() -> str:
    """
    Loads system instructions from a text file.
    NOTE: The system prompt will be sent as a separate message with the 'system' role.
    """
    instructions_file_path = os.getenv('SYSTEM_INSTRUCTIONS_PATH')
    if instructions_file_path and os.path.exists(instructions_file_path):
        try:
            with open(instructions_file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading system instructions: {e}")
    return ""


def load_usage_json():
    """Loads the token usage data from a JSON file."""
    try:
        with open(TOKENS_STORE_JSON_FILE_NAME, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"input_tokens": 0, "output_tokens": 0}


def save_usage_json(data: list):
    """Saves updated token usage data to a JSON file."""
    os.makedirs(os.path.dirname(TOKENS_STORE_JSON_FILE_NAME), exist_ok=True)
    old_data = load_usage_json()
    new_data = {
        "input_tokens": old_data.get("input_tokens", 0) + data[0],
        "output_tokens": old_data.get("output_tokens", 0) + data[1]
    }
    with open(TOKENS_STORE_JSON_FILE_NAME, 'w') as f:
        json.dump(new_data, f, indent=4)


def reset_usage():
    """Resets the token usage data to zero."""
    with open(TOKENS_STORE_JSON_FILE_NAME, 'w') as f:
        json.dump({"input_tokens": 0, "output_tokens": 0}, f, indent=4)


def load_directory_files(directory_path):
    """
    Load all text files from a directory and combine them into a single string.
    Each file is separated by a clear delimiter.
    """
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory")
        return None
    combined_content = ""
    file_count = 0
    text_extensions = ['.txt', '.md', '.html', '.xml', '.json', '.csv', '.log', '.py', '.js', '.css', '.yaml', '.yml', '.cfg', '.ini', '.sh', '.bat', '.tex']
    try:
        for filename in sorted(os.listdir(directory_path)):
            file_path = os.path.join(directory_path, filename)
            if os.path.isdir(file_path):
                continue
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                file_delimiter = f"\n\n{'='*50}\nFILE: {filename}\n{'='*50}\n\n"
                combined_content += file_delimiter + file_content
                file_count += 1
            except Exception as e:
                print(f"Skipping {filename} due to read error: {e}")
                continue
        if file_count > 0:
            print(f"Successfully loaded {file_count} text files from {directory_path}")
            return combined_content
        else:
            print(f"No readable text files found in {directory_path}")
            return ""
    except Exception as e:
        print(f"Error reading directory {directory_path}: {e}")
        return None


def load_image(dir: str, batch_size=None):
    """Load batch_size base-64-encoded images from dir into a list of content blocks."""
    # NOTE: The OpenAI-compatible API format for images is different.
    # This function's output would need to be transformed before being sent.
    # Keeping the function for structural integrity.
    content = []
    if not os.path.isdir(dir):
        print(f"Error: Provided path is not a directory: {dir}")
        return None
    image_extensions = ('jpg', 'jpeg', 'png', 'gif', 'webp')
    files = sorted(os.listdir(dir))
    for path in files:
        full_path = os.path.join(dir, path)
        if os.path.isdir(full_path) or not full_path.lower().endswith(image_extensions):
            continue
        try:
            with open(full_path, 'rb') as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            ext = pathlib.Path(full_path).suffix.lower().replace('.', '')
            if ext == "jpg":
                ext = "jpeg"
            mime_type = f"image/{ext}"
            content.append(prepare_message_with_data(base64_image, "image", mime_type))
            print(f"Loaded image: {full_path}")
        except Exception as e:
            print(f"An exception occurred for {full_path}: {e}")
    if batch_size is not None:
        return content[:batch_size]
    return content


def prepare_message(text_string, role="user"):
    """Formats a text string into the standard message structure."""
    return {"role": role, "content": text_string}


def prepare_message_generic(obj, role="user"):
    """Formats a pre-structured content object into the standard message structure."""
    return {"role": role, "content": [obj]}


def prepare_message_with_data(data, type_string, mime_type):
    """Formats a message that includes base64 encoded data."""
    return {"type": type_string, "source": {"type": "base64", "media_type": mime_type, "data": data}}


def prepare_message_with_file(user_message, file_content):
    """Formats a message including both a user query and file content."""
    combined_message = f"Prompt: {user_message}\n\n\n\nDocument content:\n{file_content}"
    return {"role": "user", "content": [{"type": "text", "text": combined_message}]}




def generate_responsedebug(model_id: str, messages: list, max_op_tokens=8192, system_prompts: str | None = None):
    """
    DEBUGGING FUNCTION: Compares the generated payload with a known-good payload.
    """
    logger.info("--- DEBUG: Comparing generated payload with known-good payload ---")

    # --- PAYLOAD 1: The one your application is generating ---
    app_payload = {
        "model": model_id,
        "max_tokens": max_op_tokens,
        "messages": messages
    }

    # --- PAYLOAD 2: The "known-good" payload from our test script ---
    # We build this from a raw Python dictionary for a fair comparison.
    known_good_payload = {
        "model": "accounts/fireworks/models/deepseek-r1-basic",
        "max_tokens": max_op_tokens,
        "messages": [{
            "role": "user",
            "content": "Say this is a test"  # Using a fixed input for the test
        }]
    }
    
    # --- Convert both to prettified JSON strings for visual comparison ---
    app_payload_json_str = json.dumps(app_payload, indent=4)
    known_good_payload_json_str = json.dumps(known_good_payload, indent=4)

    print("\n" + "="*30 + " PAYLOAD COMPARISON " + "="*30)

    print("\n--- [1] Your Application's Generated Payload ---")
    print(app_payload_json_str)
    print(f"\nType of 'messages' list: {type(messages)}")
    if messages:
        print(f"Type of first element in 'messages': {type(messages[0])}")

    print("\n" + "-"*80)

    print("\n--- [2] Known-Good Payload (from successful test script) ---")
    print(known_good_payload_json_str)

    print("\n" + "="*80)

    # --- Automated Check for Differences ---
    if app_payload_json_str == known_good_payload_json_str:
        print("\n[CONCLUSION] The JSON strings are IDENTICAL. This is unexpected.")
    else:
        print("\n[CONCLUSION] The payloads are DIFFERENT. The problem is in the generated payload above.")
        print("Look for extra keys, different value types, or structural differences in the 'messages' list.")

    # Stop the script so we can analyze the output
    sys.exit(0)

    # The actual API call is disabled during this test
    # response = requests.post(...)






# --- MODIFIED FUNCTION: This is the core of the migration ---
def generate_response(
    model_id: str,
    messages: list,
    max_op_tokens=8192,
    system_prompts: str | None = None
):
    """
    Sends messages to the Fireworks.ai API using the Fireworks Python SDK and returns the response.
    """
    logger.info("Generating response from Fireworks.ai (via SDK)...")
    think_content = None
    try:
        from fireworks import LLM

        llm = LLM(
            model=model_id,
            deployment_type="serverless",
            api_key=API_KEY
        )
        reqid = None
        reqtime = datetime.now().astimezone().isoformat()
        response_generator = llm.chat.completions.create(
            messages=messages,
            max_tokens=max_op_tokens,
            stream=True
        )

        response_text = ""
        usage_info = None

        for chunk in response_generator:
            # Append token content
            if chunk.choices and chunk.choices[0].delta.content:
                response_text += chunk.choices[0].delta.content

            if hasattr (chunk, "id") and chunk.id:
                reqid = chunk.id
                

            # Capture usage info from the final chunk if available
            if hasattr (chunk, "usage") and chunk.usage:
                input_tokens = chunk.usage.prompt_tokens
                output_tokens = chunk.usage.completion_tokens
                stop_reason = chunk.choices[0].finish_reason if chunk.choices else "unknown"

                usage_info = {
                    "prompt_token_count": input_tokens,
                    "completion_token_count": output_tokens,
                    "total_token_count": input_tokens + output_tokens,
                    "stop_reason": stop_reason
                }

        if usage_info:
            logger.info("\n" + "-" * 40)
            logger.info(f"{'Input tokens':<15}: {usage_info['prompt_token_count']}")
            logger.info(f"{'Output tokens':<15}: {usage_info['completion_token_count']}")
            logger.info(f"{'Stop reason':<15}: {usage_info['stop_reason']}")
            logger.info("-" * 40)

        if reqid:
            reqlogbody = {
                "timestamp": reqtime,
                "request_id": reqid,
                "model_id": model_id,
                "session_id": SESSION_ID
            }
            headers = {
                "Content-Type": "application/json",
                "x-api-key": AWS_API_GW_API_KEY
            }
            awsapigwreq = requests.post (AWS_API_GW, json=reqlogbody, headers=headers)
            
            logger.info (f"Timestamp: {reqtime}")
            logger.info (f"Request Id: {reqid}")

        match = re.search(r'<think>(.*?)</think>', response_text, re.DOTALL)
        if match:
            think_content = match.group(1)
            response_text = re.sub (r"<think>.*?</think>", "", response_text, flags=re.DOTALL).strip ()

        else:
            print("No <think> block found.")


        logger.info(f"Size of response: {sys.getsizeof(response_text)} bytes")
        return (think_content, response_text)

    except ImportError:
        logger.error("Fireworks SDK not installed. Please install it via `pip install fireworks-ai`.")
        return (None, "Fireworks SDK not installed.")
    except Exception as e:
        logger.error(f"An unexpected error occurred in generate_response: {e}")
        return (None, "An unexpected error occurred.")






def run_chatbot():
    """Main chatbot loop."""
    logger.info("--- Starting Chatbot with Fireworks.ai ---")
    
    validate_api_key() # MODIFIED: Replaced client configuration
    
    # MODIFIED: Use Fireworks.ai model ID from .env
    model_id = os.getenv("FIREWORKS_MODEL", "accounts/fireworks/models/qwen3-235b-a22b-thinking-2507")
    logger.info(f"Using model: {model_id}")

    system_prompts = load_system_instructions()
    messages = []
    messages.append (prepare_message(text_string=system_prompts, role="system"))

    # --- MODIFICATION: Check for headless mode ---
    is_headless = "--headless" in sys.argv
    if is_headless:
        # Remove the flag so it doesn't interfere with other argument parsing
        sys.argv.remove("--headless")
        logger.info("Running in headless (non-interactive) mode.")
    # --- END OF MODIFICATION ---

    # --- Retaining original command-line argument processing logic ---
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "im":
            images_dir = sys.argv[2] if len(sys.argv) > 2 else "../../img"
            initial_prompt_string = "This is the first prompt. It is used to provide images to you. Tell me what you see in the images provided."
            content = load_image(images_dir)
            if content:
                # Note: This part may need adjustment for Fireworks image format
                content.append({"type": "text", "text": initial_prompt_string})
                initial_message = {"role": "user", "content": content}
                messages.append(initial_message)
                # MODIFIED: Removed client from function call
                _, initial_response = generate_response(model_id, system_prompts, messages)
                if initial_response:
                    print(initial_response)
                    # The response is a string, so it needs to be formatted back into a message object
                    messages.append(prepare_message(initial_response, "assistant"))
                else:
                    logger.error("Failed to get initial response for images.")
        
        elif mode == "file":
            # --- MODIFICATION: Adjust argument count check ---
            if len(sys.argv) < 5:
                print("Usage: python -m src.fireworks_chatbot [--headless] file <prompt_file> <text_path> <output_file>")
                sys.exit(1)
            # --- END OF MODIFICATION ---


            prompt_file_path, text_path, output_file_path = sys.argv[2], sys.argv[3], sys.argv[4]
            should_print = sys.argv[5].lower() == "print" if len(sys.argv) > 5 else False

            with open(prompt_file_path, "r") as f:
                prompt_string = f.read()
            
            if os.path.isfile(text_path):
                with open(text_path, "r") as f:
                    text_content = f.read()
            elif os.path.isdir(text_path):
                text_content = load_directory_files(text_path)
            else:
                logger.error(f"Invalid text path: {text_path}")
                sys.exit(1)
            
            # The message list for file mode should be self-contained
            messages.append (prepare_message_with_file(prompt_string, text_content))
            # print (json.dumps (messages, indent=4))
            
            # MODIFIED: Removed client from function call
            thinking_content, response_text = generate_response(model_id, messages)
            
            if response_text:
                messages.append(prepare_message(response_text, "assistant"))
                with open(output_file_path, "w") as f:
                    # 'thinking_blocks' will be None, so this check prevents an error
                    if thinking_content:
                        pass
                        # f.write(f"<think>\n{thinking_content}\n</think>\n\n")
                    f.write(response_text)
                if should_print:
                    print("\n--- Response ---\n", response_text)
            else:
                logger.error("Failed to get response for file-based prompt.")
            # --- MODIFICATION: Exit only if in headless mode ---
            if is_headless:
                logger.info("Headless mode: Exiting after file processing.")
                sys.exit(0)
            # --- END OF MODIFICATION ---

    # --- Conversation History Setup (Unchanged) ---
    file_v_path_str = pathlib.Path("./data/output_file_version.json").resolve()
    os.makedirs(file_v_path_str.parent, exist_ok=True)
    try:
        file_v = utils.load_json_file(file_v_path_str)
        if not file_v: file_v = {}
    except FileNotFoundError:
        file_v = {}
    file_v_int = int(file_v.get("claude_messages_conversation_version", 0)) + 1
    file_v["claude messages conversation version"] = file_v_int
    dest_dir = pathlib.Path("./data/claude/").resolve()
    os.makedirs(dest_dir, exist_ok=True)
    dest_messages_file_path_str = dest_dir / f"Claude_Messages_Conversation_v{file_v_int}.json"
    utils.save_json_file(file_v, file_v_path_str, indent=4)

    print("\033[92mChatbot started. Type 'exit' to quit or press Ctrl+D.\033[0m")
    while True:
        try:
            user_input = input("\033[94mYou: \033[0m")
            if user_input.lower() == 'exit':
                break

            if user_input:
                messages.append(prepare_message(user_input, "user"))
                # print (json.dumps (messages, indent=4))
                
                start_time = time.time()
                # MODIFIED: Removed client from function call
                thinking_content, response_text = generate_response(model_id, messages)
                end_time = time.time()

                if response_text is not None:
                    # 'thinking_blocks' will be None, so prepare_message_generic won't be called.
                    if thinking_content:
                        messages.append(prepare_message (f"<think>\n{thinking_content}\n</think>\n\n", "assistant"))
                    messages.append(prepare_message (response_text, "assistant"))
                    utils.save_json_file(messages, str(dest_messages_file_path_str), indent=4)
                    
                    elapsed_time = end_time - start_time
                    # 'thinking_blocks' is None, so this part of the output will be empty.
                    thinking_output = f"<think>\n{thinking_content}\n</think>\n\n" if thinking_content else "\n"
                    print(f"\n\033[91mChatbot ({elapsed_time:.2f}s):\n{thinking_output}\033[0m{response_text}\n\n")
                else:
                    logger.error("Received an empty or error response. Please try again.")
                    messages.pop()

        except KeyboardInterrupt:
            print("^C")
            user_input = ""
            readline.insert_text('')  # Clear input buffer
            continue  # Go back to the start of the loop

        except EOFError:  # Ctrl+D
            print("\n\033[92mChatbot exiting.\033[0m")
            sys.exit (0)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")  # Catch-all for other errors
            continue
    
    print("\n\033[92mChatbot exiting. Goodbye!\033[0m")

if __name__ == "__main__":
    try:
        run_chatbot()

    except KeyboardInterrupt:
        print ("^C")
        sys.exit (0)
    except EOFError:
        print ("^D")
        sys.exit (0)
