#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A chatbot script to interact with Anthropic's Claude models via Google Cloud Vertex AI.
This is a complete port of an original script that used AWS Bedrock.
All original functions are included, with modifications isolated to the service provider interface.
"""

import os
import sys
import time
import readline
import base64
import json
import pathlib
import logging

from dotenv import load_dotenv

# --- Swapped Imports: from AWS SDK to Google Cloud + Anthropic SDK ---
from anthropic import AnthropicVertex
from anthropic.types import Message

# Assuming a user-provided utility module exists at this path
from src.utils import gemini_utils as utils

# --- Basic Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Ensure the .env path is correct for your environment
load_dotenv("/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/.env")

# --- Vertex AI Configuration (Replaces AWS Config) ---
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
REGION = os.getenv("GCP_REGION", "us-east5")

print (PROJECT_ID, REGION)


# --- Application Configuration (Unchanged) ---
TOKENS_STORE_JSON_FILE_NAME = os.getenv("CLAUDE_TOKENS_STORE_JSON_FILE_NAME")


def configure_vertex_client():
    """
    Configures and returns the Anthropic on Vertex AI client.
    This function replaces the `configure_bedrock_runtime`, `configure_bedrock`,
    and `assume_role` functions from the original AWS implementation.
    """
    if not PROJECT_ID:
        logger.error("FATAL: GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
        sys.exit(1)

    logger.info(f"Initializing Vertex AI client for project '{PROJECT_ID}' in region '{REGION}'...")
    try:
        # Authentication is handled automatically via 'gcloud auth application-default login'
        client = AnthropicVertex(project_id=PROJECT_ID, region=REGION)
        return client
    except Exception as e:
        logger.error(f"Error creating AnthropicVertex client: {e}")
        logger.error("Please ensure you have run 'gcloud auth application-default login' and that the Vertex AI API is enabled.")
        sys.exit(1)


def load_system_instructions() -> str:
    """
    Loads system instructions from a text file.
    NOTE: The Vertex AI SDK expects a simple string for the system prompt.
    """
    instructions_file_path = os.getenv('SYSTEM_INSTRUCTIONS_PATH')
    if instructions_file_path and os.path.exists(instructions_file_path):
        try:
            with open(instructions_file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading system instructions: {e}")
    return ""  # Return a default empty instruction


def load_usage_json():
    """Loads the token usage data from a JSON file."""
    try:
        with open(TOKENS_STORE_JSON_FILE_NAME, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"input_tokens": 0, "output_tokens": 0}


def save_usage_json(data: list):
    """Saves updated token usage data to a JSON file."""
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
    return {"role": role, "content": [{"type": "text", "text": text_string}]}


def prepare_message_generic(obj, role="user"):
    """Formats a pre-structured content object into the standard message structure."""
    return {"role": role, "content": [obj]}


def prepare_message_with_data(data, type_string, mime_type):
    """Formats a message that includes base64 encoded data."""
    return {"type": type_string, "source": {"type": "base64", "media_type": mime_type, "data": data}}


def prepare_message_with_file(user_message, file_content):
    """Formats a message including both a user query and file content."""
    combined_message = f"{user_message}\n\n\n\nDocument content:\n{file_content}"
    return {"role": "user", "content": [{"type": "text", "text": combined_message}]}


def generate_response(vertex_client: AnthropicVertex, model_id: str, system_prompts: str, messages: list, max_op_tokens=8192):
    """
    Sends messages to a Claude model on Vertex AI and returns the response.
    This is the core modified function, replacing the AWS `invoke_model` logic.
    """
    should_deep_think = os.getenv("SHOULD_CLAUDE_37_DEEP_THINK", "false").lower() == "true"
    deep_think_budget = int(os.getenv("CLAUDE_37_DEEP_THINK_BUDGET", "16000"))
    print (f"messages list: {json.dumps(messages, indent=4)}\n\n")
    print (f"Sys prompts: {system_prompts}\n\n")

    try:
        request_params = {
            "model": model_id,
            "system": system_prompts,
            "messages": messages,
            "max_tokens": max_op_tokens,
        }

        if should_deep_think:
            request_params["thinking"] = {"type": "enabled", "budget_tokens": deep_think_budget}

        response_message: Message = vertex_client.messages.create(**request_params)

        input_tokens = response_message.usage.input_tokens
        output_tokens = response_message.usage.output_tokens

        logger.info(f"\nInput tokens: {input_tokens:<15}")
        logger.info(f"Output tokens:  {output_tokens}")
        logger.info(f"Stop reason:    {response_message.stop_reason}")

        save_usage_json([input_tokens, output_tokens])

        output_text_parts = []
        thinking_blocks = []

        for block in response_message.content:
            if block.type == "text":
                output_text_parts.append(block.text)
            elif block.type == "thinking":
                thinking_blocks.append({"type": "thinking", "thinking": block.model_dump()})

        final_text_response = "".join(output_text_parts)
        logger.info(f"Size of response: {sys.getsizeof(final_text_response)} bytes")

        return (thinking_blocks, final_text_response)

    except Exception as e:
        logger.error(f"An unexpected error occurred in generate_response: {e}")
        return (None, None)


def run_chatbot():
    """Main chatbot loop."""
    logger.info("--- Starting Chatbot with Google Cloud Vertex AI ---")
    
    vertex_client = configure_vertex_client()
    
    # Use Vertex AI-formatted model ID. Example: claude-3-5-sonnet@20240620
    # model_id = "claude-3-7-sonnet@20250219"
    model_id = "claude-sonnet-4@20250514"
    logger.info(f"Using model: {model_id}")

    system_prompts = load_system_instructions()
    messages = []

    # --- Retaining original command-line argument processing logic ---
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "im":
            images_dir = sys.argv[2] if len(sys.argv) > 2 else "../../img"
            initial_prompt_string = "This is the first prompt. It is used to provide images to you. Tell me what you see in the images provided."
            content = load_image(images_dir)
            if content:
                content.append({"type": "text", "text": initial_prompt_string})
                initial_message = {"role": "user", "content": content}
                messages.append(initial_message)
                _, initial_response = generate_response(vertex_client, model_id, system_prompts, messages)
                if initial_response:
                    print(initial_response)
                    messages.append(prepare_message(initial_response, "assistant"))
                else:
                    logger.error("Failed to get initial response for images.")
        
        elif mode == "file":
            if len(sys.argv) < 5:
                print("Usage: python your_script.py file <prompt_file> <text_path> <output_file> [print]")
                sys.exit(1)
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
            
            final_prompt = f"{prompt_string}\n\n--- DOCUMENT CONTENT ---\n\n{text_content}"
            messages.append(prepare_message(final_prompt, "user"))
            
            thinking_blocks, response_text = generate_response(vertex_client, model_id, system_prompts, messages)
            
            if response_text:
                with open(output_file_path, "w") as f:
                    if thinking_blocks:
                        f.write(f"<thinking>\n{json.dumps(thinking_blocks, indent=2)}\n</thinking>\n\n")
                    f.write(response_text)
                if should_print:
                    print("\n--- Response ---\n", response_text)
            else:
                logger.error("Failed to get response for file-based prompt.")
            sys.exit(0) # Exit after file processing

    # --- Conversation History Setup ---
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
                
                start_time = time.time()
                thinking_blocks, response_text = generate_response(vertex_client, model_id, system_prompts, messages)
                end_time = time.time()

                if response_text is not None:
                    if thinking_blocks:
                        for block in thinking_blocks:
                            messages.append(prepare_message_generic(block, "assistant"))
                    messages.append(prepare_message(response_text, "assistant"))
                    utils.save_json_file(messages, str(dest_messages_file_path_str), indent=4)
                    
                    elapsed_time = end_time - start_time
                    thinking_output = f"<think>\n{json.dumps(thinking_blocks[0]['thinking'], indent=2)}\n</think>\n\n" if thinking_blocks else ""
                    print(f"\n\033[91mChatbot ({elapsed_time:.2f}s):\n{thinking_output}\033[0m{response_text}\n\n")
                else:
                    logger.error("Received an empty or error response. Please try again.")
                    messages.pop()

        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            logger.error(f"An unexpected error occurred in the main loop: {e}", exc_info=True)
            continue
    
    print("\n\033[92mChatbot exiting. Goodbye!\033[0m")

if __name__ == "__main__":
    try:
        run_chatbot()
    except (KeyboardInterrupt, EOFError):
        print("\n\033[92mChatbot force-exited.\033[0m")
        sys.exit(0)
