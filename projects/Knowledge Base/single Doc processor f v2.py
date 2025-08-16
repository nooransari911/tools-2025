# =====================================================================================
# MONKEY-PATCH FOR PROTOBUF (Still required for co-existence)
# =====================================================================================
import os
import sys

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import google.protobuf.descriptor_pool
from google.protobuf.internal import api_implementation

if api_implementation.Type() != 'python':
    print("Warning: Protobuf C++ backend active. Patch may not be effective.", file=sys.stderr)

pool = google.protobuf.descriptor_pool.Default()
_original_add_serialized_file = pool.AddSerializedFile

def _patched_add_serialized_file(serialized_proto):
    try:
        return _original_add_serialized_file(serialized_proto)
    except TypeError as e:
        if 'duplicate file name' in str(e):
            try:
                file_name = str(e).split(':')[-1].strip()
                return pool.FindFileByName(file_name)
            except Exception:
                raise e
        else:
            raise

pool.AddSerializedFile = _patched_add_serialized_file
print("✅ Protobuf patch applied.")
# --- END OF MONKEY-PATCH ---

# --- REGULAR IMPORTS ---
import argparse
import pathlib
import logging
import json
from typing import List, Optional, Union, Tuple, Any, Dict

try:
    from src.utils import gemini_utils, errors
except ImportError as e:
     print(f"Error importing local modules. Run from project root. Error: {e}", file=sys.stderr)
     sys.exit(1)

from google.genai import types as genai_types
from fireworks import LLM
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("gemini_cli")
load_dotenv("/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/.env")


# --- NEW FIREWORKS LOGIC (Ported from Chatbot) ---
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
FIREWORKS_MODEL = os.getenv("FIREWORKS_MODEL", "accounts/fireworks/models/deepseek-r1-basic")

def prepare_fireworks_message_with_file(user_message: str, file_content: str) -> Dict[str, Any]:
    """
    Formats a message including both a user query and file content.
    This is the core message structure for the Fireworks analysis step.
    """
    combined_message = f"""CONTEXT: The following text was extracted from a prior process.

--- START OF CONTEXT ---
{file_content}
--- END OF CONTEXT ---

TASK: Now, please perform the following task based *only* on the text provided in the context above.

--- START OF TASK ---
{user_message}
--- END OF TASK ---
"""
    return {"role": "user", "content": combined_message}

def generate_fireworks_content(
    messages: List[Dict[str, Any]],
    max_tokens: int = 8192,
    model: str = None
) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """
    Sends messages to the Fireworks AI API using the SDK.
    This is the new, robust version ported from your chatbot script.
    """
    if not FIREWORKS_API_KEY:
        logger.error("FATAL: FIREWORKS_API_KEY environment variable not set.")
        return None, None

    if model is None:
        model = FIREWORKS_MODEL

    logger.info(f"Generating response from Fireworks.ai (model: {model})...")

    try:
        llm = LLM(model=model, api_key=FIREWORKS_API_KEY)
        response_generator = llm.chat.completions.create(
            messages=messages,
            max_tokens=max_tokens,
            stream=True
        )

        response_text = ""
        usage_info = None
        for chunk in response_generator:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                response_text += chunk.choices[0].delta.content

            if hasattr(chunk, 'usage') and chunk.usage:
                usage_info = {
                    "prompt_token_count": chunk.usage.prompt_tokens,
                    "candidates_token_count": chunk.usage.completion_tokens,
                    "total_token_count": chunk.usage.total_tokens
                }

        if usage_info:
            logger.info(f"Fireworks API call successful. Tokens - In: {usage_info['prompt_token_count']}, Out: {usage_info['candidates_token_count']}")
        return response_text, usage_info

    except ImportError:
        logger.error("The 'fireworks-ai' package is not installed. Please run `pip install fireworks-ai`.")
        return None, None
    except Exception as e:
        logger.error(f"Unexpected error in Fireworks API call: {e}", exc_info=True)
        return None, None
# --- END OF NEW FIREWORKS LOGIC ---


# --- Provider Detection (Unchanged) ---
def get_provider_type() -> str:
    """Determines which AI provider to use based on environment variable."""
    provider = os.getenv("AI_PROVIDER", "gemini").lower()
    if provider not in ["gemini", "fireworks"]:
        logger.error(f"Invalid AI_PROVIDER: {provider}. Must be 'gemini' or 'fireworks'")
        sys.exit(1)
    return provider


# --- Input Loading (Unchanged but now used differently by Fireworks) ---
def load_input_records(input_source: str, provider_type: str) -> List[Union[str, genai_types.Part]]:
    """
    Loads input records from files/dir or lines/file.
    For Gemini (OCR step): Loads images from a directory.
    For Fireworks (Analysis step): Loads text from a single file.
    """
    records = []
    source_path = pathlib.Path(input_source)
    if source_path.is_dir(): # This path is taken by Gemini for OCR
        logger.info(f"Loading files from directory for Gemini: {source_path}")
        for f in os.listdir(source_path):
            file_path = source_path / f
            try:
                if f.endswith((".jpeg", ".jpg", ".png", ".webp", ".gif")):
                     mime_map = {'.jpeg': 'image/jpeg', '.jpg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.gif': 'image/gif'}
                     records.append(genai_types.Part.from_bytes(data=file_path.read_bytes(), mime_type=mime_map.get(file_path.suffix.lower(), 'application/octet-stream')))
                else:
                    logger.warning(f"Skipping non-image file in dir: {f}")
            except Exception as e:
                logger.error(f"Error processing image file {file_path}: {e}", exc_info=True)
    elif source_path.is_file(): # This path is taken by Fireworks for Analysis
        logger.info(f"Loading single text file for Fireworks: {source_path}")
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                records = [f.read()] # Read the entire file content as a single record
        except Exception as e:
            logger.error(f"Error reading text file {source_path}: {e}", exc_info=True)
    else:
        logger.error(f"Input source '{input_source}' not a valid file or directory.")
    logger.info(f"Loaded {len(records)} input records.")
    return records


# --- Main Processing Function (Overhauled for Fireworks) ---
def process_all_at_once(
    records: List[Union[str, genai_types.Part]],
    prompt: str,
    provider_type: str,
    model_type: str,
    api_key_type: str
) -> Tuple[List[str], List[Dict[str, Any]]]:
    """Processes all records in a single API call, provider-aware."""
    if not records:
        return [], []
    logger.info(f"Starting single-shot processing for {len(records)} records using {provider_type}")

    if provider_type == "fireworks":
        # --- NEW FIREWORKS PROCESSING PATH ---
        try:
            # The 'records' list contains one item: the text content from the Gemini OCR file.
            ocr_text_content = records[0]
            if not isinstance(ocr_text_content, str):
                raise TypeError("Fireworks provider expected a string input but received something else.")

            # Use the robust message preparation function from the chatbot
            messages = [prepare_fireworks_message_with_file(prompt, ocr_text_content)]

            logger.info("Calling Fireworks API with OCR'd text...")
            response_text, usage_info = generate_fireworks_content(messages=messages)

            if response_text is None:
                raise Exception("Fireworks API returned a None response.")

            logger.info("Fireworks API call successful.")
            return [response_text], [usage_info] if usage_info else []

        except Exception as e:
            logger.error(f"Error during Fireworks single-shot processing: {e}", exc_info=True)
            return [f"Error: Fireworks processing failed: {e}"], []

    else: # --- ORIGINAL GEMINI PROCESSING PATH (Unchanged) ---
        try:
            client, model_name = gemini_utils.configure_gemini(model_type, api_key_type)
            generation_config = genai_types.GenerateContentConfig(max_output_tokens=8192)
            contents = records + [prompt]
            logger.info("Calling Gemini API with all records...")
            response = gemini_utils.generate_gemini_content(
                genai_client=client,
                model_name=model_name,
                contents=contents,
                generation_config=generation_config,
                is_structured_mode=False
            )
            if response is None:
                raise errors.UnexpectedNoneError("response", "Gemini response was None/empty")
            usage_info = None
            if response.usage_metadata:
                 usage_info = {
                    "prompt_token_count": response.usage_metadata.prompt_token_count,
                    "candidates_token_count": response.usage_metadata.candidates_token_count,
                    "total_token_count": response.usage_metadata.total_token_count
                 }
            logger.info("Gemini API call successful.")
            return [response.text], [usage_info] if usage_info else []
        except Exception as e:
            logger.error(f"Error during Gemini single-shot processing: {e}", exc_info=True)
            return [f"Error: Gemini processing failed: {e}"], []


# --- Main CLI Execution (Unchanged) ---
def main_cli():
    parser = argparse.ArgumentParser(description="Process documents using Gemini API or Fireworks AI.")
    parser.add_argument("model_type", choices=['pro', 'flash'], help="Model type (Gemini: pro/flash, Fireworks: pro/...).")
    parser.add_argument("api_key_type", choices=['free', 'paid'], help="API key type (for Gemini).")
    parser.add_argument("prompt_file", help="Path to the file containing the main prompt.")
    parser.add_argument("-i", "--input-source", required=True, type=str, help="Path to input file (for Fireworks) or directory (for Gemini).")
    parser.add_argument("-o", "--output-config", type=str, default="./output_version.json", help="Path to output version config JSON.")
    parser.add_argument("-u", "--usage-file", type=str, default=None, help="Path to JSON file for tracking token usage.")
    args = parser.parse_args()

    provider_type = get_provider_type()

    prompt = gemini_utils.load_prompt_from_file(args.prompt_file)
    if prompt is None: sys.exit(1)

    records = load_input_records(args.input_source, provider_type)
    if not records:
        logger.error("Input source specified, but no records loaded.")
        sys.exit(1)

    all_responses, all_usage_dicts = process_all_at_once(
        records=records,
        prompt=prompt,
        provider_type=provider_type,
        model_type=args.model_type,
        api_key_type=args.api_key_type
    )

    gemini_utils.write_output_files(all_responses, args.output_config, is_structured_mode=False)

    # Simplified usage tracking
    if all_usage_dicts:
        usage_file_path = args.usage_file or f"./{provider_type}_tokens_usage.json"
        try:
            if os.path.exists(usage_file_path):
                with open(usage_file_path, 'r') as f: existing_usage = json.load(f)
            else:
                existing_usage = {"total_prompt_tokens": 0, "total_completion_tokens": 0, "total_tokens": 0}

            for usage_dict in all_usage_dicts:
                if usage_dict:
                    existing_usage["total_prompt_tokens"] += usage_dict.get("prompt_token_count", 0)
                    existing_usage["total_completion_tokens"] += usage_dict.get("candidates_token_count", 0)
                    existing_usage["total_tokens"] += usage_dict.get("total_token_count", 0)

            with open(usage_file_path, 'w') as f:
                json.dump(existing_usage, f, indent=2)
            logger.info(f"{provider_type.capitalize()} token usage updated in: {usage_file_path}")
        except Exception as e:
            logger.error(f"Error updating token usage: {e}")

    logger.info("CLI processing complete.")

if __name__ == "__main__":
    main_cli()
