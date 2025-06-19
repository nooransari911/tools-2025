# =====================================================================================
# MONKEY-PATCH FOR PROTOBUF DUPLICATE REGISTRATION ERROR (v2 - Corrected)
#
# WHY: The 'fireworks-ai' and Google Cloud libraries conflict by trying to register
# the same Protobuf definitions.
#
# WHAT THIS DOES (THE RIGHT WAY):
# 1. Forces the pure-Python Protobuf implementation via an environment variable.
# 2. Intercepts the `AddSerializedFile` method.
# 3. In a `try` block, it attempts the normal operation. If it succeeds, it returns
#    the resulting file descriptor as expected.
# 4. If it fails with the specific "duplicate file name" TypeError, the `except`
#    block now intelligently PARSES the filename from the error message, USES that
#    name to FIND the already-registered descriptor in the pool, and RETURNS it.
#    This crucial step prevents the 'NoneType' AttributeError seen previously.
# =====================================================================================
import os
import sys

# Step 1: Force the Python implementation of Protobuf.
# This MUST be done before any 'google.protobuf' modules are imported.
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

# Now, we can import the necessary modules.
import google.protobuf.descriptor_pool
from google.protobuf.internal import api_implementation

# Sanity check to ensure the patch will be effective.
if api_implementation.Type() != 'python':
    print("Warning: Protobuf C++ backend is active. The patch may not be effective.", file=sys.stderr)
    print("Ensure this patch runs before any other imports.", file=sys.stderr)


# Step 2: Get a reference to the default descriptor pool and the original method.
pool = google.protobuf.descriptor_pool.Default()
_original_add_serialized_file = pool.AddSerializedFile


# Step 3: Define our new, smarter patched function.
def _patched_add_serialized_file(serialized_proto):
    """A patched version that handles duplicates by finding and returning the existing descriptor."""
    try:
        # Attempt to call the original method and return its result.
        return _original_add_serialized_file(serialized_proto)
    except TypeError as e:
        # Check if this is the specific error we want to handle.
        if 'duplicate file name' in str(e):
            # The file is already registered. We need to find its name from the error
            # string and then find the existing descriptor object in the pool.
            # Example error: "TypeError: Couldn't build proto file into descriptor pool: duplicate file name google/protobuf/field_mask.proto"
            try:
                # This parsing is fragile but necessary. It gets the filename.
                file_name = str(e).split(':')[-1].strip()
                # Find the existing file descriptor and return it. This is the fix.
                return pool.FindFileByName(file_name)
            except Exception as find_e:
                # If for some reason we can't parse or find, re-raise the original error.
                print(f"Patch Error: Could not handle duplicate registration. Sub-error: {find_e}", file=sys.stderr)
                raise e
        else:
            # If it's a different TypeError, we must re-raise it.
            raise

# Step 4: Apply the patch by replacing the original method with our new one.
pool.AddSerializedFile = _patched_add_serialized_file

print("✅ Protobuf patch v2 applied successfully. Now handles duplicates correctly.")
# --- END OF MONKEY-PATCH ---


# YOUR REGULAR IMPORTS CAN NOW PROCEED
print("Importing fireworks...")
from fireworks import LLM

print("Importing gemini_utils...")
from src.utils import gemini_utils # Or whatever your other conflicting import is

print("\nAll libraries imported successfully. Application starting.")


# ... The rest of your application code ...





import os
import sys
import argparse
import pathlib
import logging
import json
import requests, http.client
from typing import List, Optional, Union, Tuple, Any, Dict

# Import the refactored utils. Assumes script is in project root, src/ is sibling.
try:
    from src.utils import gemini_utils, errors
    # Schemas are imported/registered within gemini_utils
except ImportError as e:
     print(f"Error importing local modules. Run from project root. Error: {e}", file=sys.stderr)
     sys.exit(1)

# Third-party imports
from google.genai import types, client
from google import genai
#from fireworks import LLM
from dotenv import load_dotenv # Used in __main__

# Setup logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("gemini_cli")

load_dotenv("/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/.env")


http.client.HTTPConnection.debuglevel = 1

requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True





# --- Fireworks AI Configuration ---
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
print (FIREWORKS_API_KEY)
FIREWORKS_API_URL = "https://api.fireworks.ai/inference/v1/chat/completions"
FIREWORKS_MODEL = os.getenv("FIREWORKS_MODEL", "accounts/fireworks/models/deepseek-r1-basic")

# Fixed URLs for Fireworks AI
FIREWORKS_STATIC_URLS = [
    "https://d3isj3hu8683a4.cloudfront.net/test/img/test-img-1.jpg",
    "https://d3isj3hu8683a4.cloudfront.net/test/img/test-img-2.jpg",
    "https://d3isj3hu8683a4.cloudfront.net/test/img/test-img-3.jpg",
    "https://d3isj3hu8683a4.cloudfront.net/test/img/test-img-4.jpg",
]

# --- Provider Detection ---
def get_provider_type() -> str:
    """Determines which AI provider to use based on environment variable."""
    provider = os.getenv("AI_PROVIDER", "gemini").lower()
    if provider not in ["gemini", "fireworks"]:
        logger.error(f"Invalid AI_PROVIDER: {provider}. Must be 'gemini' or 'fireworks'")
        sys.exit(1)
    return provider

# --- Fireworks AI Message Preparation Functions ---
def prepare_fireworks_text_message(text_string: str, role: str = "user") -> Dict[str, Any]:
    """Formats a text string into Fireworks/OpenAI message structure."""
    return {"role": role, "content": text_string}

def prepare_fireworks_mixed_content_message(content_list: List[Dict[str, Any]], role: str = "user") -> Dict[str, Any]:
    """Formats mixed content (text + images/files) into Fireworks/OpenAI message structure."""
    return {"role": role, "content": content_list}

def prepare_fireworks_text_content(text: str) -> Dict[str, Any]:
    """Prepares text content block for Fireworks messages."""
    return {"type": "text", "text": text}

def prepare_fireworks_image_url_content(url: str) -> Dict[str, Any]:
    """Prepares image URL content block for Fireworks messages."""
    return {
        "type": "image_url",
        "image_url": {"url": url}
    }

def prepare_fireworks_file_url_content(url: str) -> Dict[str, Any]:
    """Prepares file URL content block for Fireworks messages."""
    return {
        "type": "image_url",  # Fireworks uses image_url type for all URL content
        "image_url": {"url": url}
    }

# --- Fireworks AI Client Functions ---
def validate_fireworks_api_key() -> bool:
    """Validates that the Fireworks API key is set."""

    if not FIREWORKS_API_KEY:
        logger.error("FATAL: FIREWORKS_API_KEY environment variable not set.")
        return False
    logger.info("Fireworks.ai API key configured successfully.")
    return True

def generate_fireworks_contentv1(
    messages: List[Dict[str, Any]], 
    max_tokens: int = 8192,
    model: str = None
) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """
    Sends messages to Fireworks AI API and returns response text and usage info.
    Returns (response_text, usage_info) or (None, None) on error.
    """
    if not validate_fireworks_api_key():
        return None, None
        
    if model is None:
        model = FIREWORKS_MODEL
        
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FIREWORKS_API_KEY}"
    }
    
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages
    }
    
    logger.debug(f"Fireworks request payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(FIREWORKS_API_URL, headers=headers, data=json.dumps(payload), timeout=180)
        response.raise_for_status()
        response_data = response.json()
        
        input_tokens = response_data.get("usage", {}).get("prompt_tokens", 0)
        output_tokens = response_data.get("usage", {}).get("completion_tokens", 0)
        total_tokens = input_tokens + output_tokens
        
        usage_info = {
            "prompt_token_count": input_tokens,
            "candidates_token_count": output_tokens,
            "total_token_count": total_tokens
        }
        
        response_text = response_data["choices"][0]["message"]["content"]
        
        logger.info(f"Fireworks API call successful. Input: {input_tokens}, Output: {output_tokens}")
        return response_text, usage_info



    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        
        try:
            # Try to parse JSON error response
            error_data = e.response.json()
            if 'error' in error_data:
                code_string = error_data['error'].get('code', 'UNKNOWN')
                message = error_data['error'].get('message', 'No message provided')
            else:
                code_string = 'HTTP_ERROR'
                message = str(e)
        except (json.JSONDecodeError, AttributeError):
            # Fallback if response isn't JSON or doesn't have expected structure
            code_string = 'HTTP_ERROR'
            message = str(e)
        
        logger.error (f"HTTP Error - Code: {status_code}, Type: {code_string}, Message: {message}")

    except requests.exceptions.RequestException as e:
        # Handle other request exceptions (connection errors, timeouts, etc.)
        logger.error (f"Request Error - Code: 0, Type: REQUEST_EXCEPTION, Message: {str(e)}")






    except (KeyError, IndexError) as e:
        logger.error(f"Failed to parse Fireworks API response: {e}")
        return None, None
    except Exception as e:
        logger.error(f"Unexpected error in Fireworks API call: {e}")
        return None, None


def generate_fireworks_contentv2(
    messages: List[Dict[str, Any]], 
    max_tokens: int = 8192,
    model: str = None
) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """
    Sends messages to Fireworks AI API and returns response text and usage info.
    Returns (response_text, usage_info) or (None, None) on error.
    """
    if not validate_fireworks_api_key():
        return None, None
        
    if model is None:
        model = FIREWORKS_MODEL
        
    headers = {
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FIREWORKS_API_KEY}"
    }
    
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
        "stream": True
    }
    
    logger.debug(f"Fireworks request payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(FIREWORKS_API_URL, headers=headers, data=json.dumps(payload), timeout=600, stream=True)
        response.raise_for_status()
        
        response_text = ""
        usage_info = None
        """
        for line in response.iter_lines(decode_unicode=True):
            if not line or not line.strip():
                continue  # Skip empty lines

            if line.startswith("data: "):
                data_content = line[6:]  # Remove "data: " prefix
                
                if data_content == "[DONE]":
                    break
                
                try:
                    chunk_data = json.loads(data_content)
                    
                    # Extract content from delta
                                        # Extract content from delta
                    if "choices" in chunk_data and len(chunk_data["choices"]) > 0:
                        delta = chunk_data["choices"][0].get("delta", {})
                        content = delta.get("content")
                        if content is not None:
                            response_text += content
                    
                    # Extract usage info from final chunk
                    if "usage" in chunk_data and chunk_data["usage"]:
                        input_tokens = chunk_data["usage"].get("prompt_tokens", 0)
                        output_tokens = chunk_data["usage"].get("completion_tokens", 0)
                        total_tokens = input_tokens + output_tokens
                        
                        usage_info = {
                            "prompt_token_count": input_tokens,
                            "candidates_token_count": output_tokens,
                            "total_token_count": total_tokens
                        }
                        
                except json.JSONDecodeError:
                    continue  # Skip malformed JSON chunks
        """
        # Handle the response content whether it's truly streaming or not
        response_content = response.text
        lines = response_content.split('\n')


        for line in lines:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
                
            if line.startswith("data: "):
                data_content = line[6:]  # Remove "data: " prefix
                
                if data_content.strip() == "[DONE]":
                    break
                
                try:
                    chunk_data = json.loads(data_content)
                    
                    # Extract content from delta
                    if "choices" in chunk_data and len(chunk_data["choices"]) > 0:
                        delta = chunk_data["choices"][0].get("delta", {})
                        content = delta.get("content")
                        if content is not None:
                            response_text += content
                    
                    # Extract usage info from final chunk
                    if "usage" in chunk_data and chunk_data["usage"]:
                        input_tokens = chunk_data["usage"].get("prompt_tokens", 0)
                        output_tokens = chunk_data["usage"].get("completion_tokens", 0)
                        total_tokens = input_tokens + output_tokens
                        
                        usage_info = {
                            "prompt_token_count": input_tokens,
                            "candidates_token_count": output_tokens,
                            "total_token_count": total_tokens
                        }
                        
                except json.JSONDecodeError:
                    continue  # Skip malformed JSON chunks


        
        logger.info(f"Fireworks API call successful. Input: {usage_info['prompt_token_count'] if usage_info else 0}, Output: {usage_info['candidates_token_count'] if usage_info else 0}")
        return response_text, usage_info
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        
        try:
            # Try to parse JSON error response
            error_data = e.response.json()
            if 'error' in error_data:
                code_string = error_data['error'].get('code', 'UNKNOWN')
                message = error_data['error'].get('message', 'No message provided')
            else:
                code_string = 'HTTP_ERROR'
                message = str(e)
        except (json.JSONDecodeError, AttributeError):
            # Fallback if response isn't JSON or doesn't have expected structure
            code_string = 'HTTP_ERROR'
            message = str(e)
        
        logger.error (f"HTTP Error - Code: {status_code}, Type: {code_string}, Message: {message}")
    except requests.exceptions.RequestException as e:
        # Handle other request exceptions (connection errors, timeouts, etc.)
        logger.error (f"Request Error - Code: 0, Type: REQUEST_EXCEPTION, Message: {str(e)}")
    except (KeyError, IndexError) as e:
        logger.error(f"Failed to parse Fireworks API response: {e}")
        return None, None
    except Exception as e:
        logger.error(f"Unexpected error in Fireworks API call: {e}")
        return None, None





def generate_fireworks_content(
    messages: List[Dict[str, Any]], 
    max_tokens: int = 8192,
    model: str = None
) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """
    Sends messages to Fireworks AI API and returns response text and usage info.
    Returns (response_text, usage_info) or (None, None) on error.
    """
    if not validate_fireworks_api_key():
        return None, None
        
    if model is None:
        model = FIREWORKS_MODEL
    
    try:
        from fireworks import LLM
        
        llm = LLM(
            model=model,
            deployment_type="serverless",
            api_key=FIREWORKS_API_KEY
        )
        
        response_generator = llm.chat.completions.create(
            messages=messages,
            max_tokens=max_tokens,
            stream=True
        )
        
        response_text = ""
        usage_info = None
        
        for chunk in response_generator:
            if chunk.choices[0].delta.content:
                response_text += chunk.choices[0].delta.content
            
            # Get usage info from the final chunk
            if hasattr(chunk, 'usage') and chunk.usage:
                input_tokens = chunk.usage.prompt_tokens
                output_tokens = chunk.usage.completion_tokens
                total_tokens = input_tokens + output_tokens
                
                usage_info = {
                    "prompt_token_count": input_tokens,
                    "candidates_token_count": output_tokens,
                    "total_token_count": total_tokens
                }
        
        logger.info(f"Fireworks API call successful. Input: {usage_info['prompt_token_count'] if usage_info else 0}, Output: {usage_info['candidates_token_count'] if usage_info else 0}")
        return response_text, usage_info
        
    except ImportError:
        logger.error("Fireworks package not installed")
        return None, None
    except Exception as e:
        logger.error(f"Unexpected error in Fireworks API call: {e}")
        return None, None






# --- Input Loading (Modified for Fireworks) ---
def load_input_records(input_source: str, provider_type: str) -> List[Union[str, types.Part]]:
    """Loads input records from files/dir or lines/file, provider-aware."""
    if provider_type == "fireworks":
        # For Fireworks, we use static URLs instead of loading files
        logger.info("Using Fireworks AI - static URLs will be used instead of local files")
        return FIREWORKS_STATIC_URLS
    
    # Original Gemini logic for file loading
    records = []
    source_path = pathlib.Path(input_source)
    if source_path.is_dir():
        logger.info(f"Loading files from directory: {source_path}")
        if not source_path.exists(): return []
        for f in os.listdir(source_path):
            file_path = source_path / f
            try:
                if f.endswith((".txt", ".md", ".json", ".html", ".xml")):
                    with open(file_path, 'r', encoding="utf-8") as file: records.append(file.read())
                elif f.endswith(".pdf"): records.append(types.Part.from_bytes(data=file_path.read_bytes(), mime_type='application/pdf'))
                elif f.endswith((".jpeg", ".jpg", ".png", ".webp", ".gif")):
                     mime_map = {'.jpeg': 'image/jpeg', '.jpg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.gif': 'image/gif'}
                     records.append(types.Part.from_bytes(data=file_path.read_bytes(), mime_type=mime_map.get(file_path.suffix.lower(), 'application/octet-stream')))
                else: logger.warning(f"Skipping unsupported file in dir: {f}")
            except Exception as e: logger.error(f"Error processing file {file_path}: {e}", exc_info=True)
    elif source_path.is_file():
        logger.info(f"Loading lines from file: {source_path}")
        try:
            with open(source_path, 'r', encoding='utf-8') as f: records = [line.strip() for line in f if line.strip()]
        except Exception as e: logger.error(f"Error reading lines file {source_path}: {e}", exc_info=True)
    else: logger.error(f"Input source '{input_source}' not valid file/dir.")
    logger.info(f"Loaded {len(records)} input records.")
    return records

def load_prompt_from_file(prompt_file_path: str) -> Optional[str]:
    """Loads prompt string from file."""
    path = pathlib.Path(prompt_file_path)
    if not path.is_file(): logger.error(f"Prompt file not found: {path}"); return None
    try:
        with open(path, "r", encoding='utf-8') as prompt_file: return prompt_file.read()
    except Exception as e: logger.error(f"Error reading prompt file {path}: {e}", exc_info=True); return None

# --- Aggregation Function (Provider-aware) ---
def aggregate_responses(
    base_responses: List[str],
    aggregation_prompt: str,
    provider_type: str,
    model_type: str,
    api_key_type: str,
    is_structured_mode: bool,
    schema_name: Optional[str]
) -> List[str]:
    """Performs an aggregation step on the initial responses, provider-aware."""
    if not base_responses:
        logger.warning("No base responses to aggregate.")
        return []
    if not aggregation_prompt:
        logger.warning("No aggregation prompt provided.")
        return base_responses

    logger.info("Performing aggregation step...")
    
    if provider_type == "fireworks":
        # Fireworks aggregation
        messages = []
        for response in base_responses:
            messages.append(prepare_fireworks_text_message(response, "assistant"))
        messages.append(prepare_fireworks_text_message(aggregation_prompt, "user"))
        
        response_text, _ = generate_fireworks_content(messages, max_tokens=8192)
        if response_text:
            logger.info("Fireworks aggregation call successful.")
            return [response_text]
        else:
            logger.error("Fireworks aggregation step failed")
            return [f"Error during Fireworks aggregation"]
    
    else:
        # Original Gemini aggregation logic
        try:
            client, model_name = gemini_utils.configure_gemini(model_type, api_key_type)
        except Exception as e:
            logger.error(f"Failed to configure Gemini client for aggregation: {e}")
            return [f"Error configuring Gemini client: {e}"]
            
        sys_instructions = gemini_utils.load_system_instructions(is_structured_mode)
        
        resolved_schema_class: Optional[type] = None
        if is_structured_mode:
            if schema_name:
                resolved_schema_class = gemini_utils.resolve_schema_class(schema_name)
                if not resolved_schema_class:
                    logger.warning(
                        f"Aggregation schema '{schema_name}' not found or invalid. "
                        "Aggregation will use model-inferred JSON structure if applicable."
                    )

        gen_config_args: Dict[str, Any] = {
            "system_instruction": sys_instructions,
            "max_output_tokens": 8192,
        }

        if is_structured_mode:
            gen_config_args["response_mime_type"] = "application/json"
            if resolved_schema_class:
                gen_config_args["response_schema"] = resolved_schema_class
                logger.info(f"Aggregation step will use schema: {schema_name}")
            else:
                logger.info("Aggregation step will use model-inferred JSON structure.")
        
        agg_generation_config = types.GenerateContentConfig(**gen_config_args)
        history = base_responses + [aggregation_prompt]

        try:
            agg_response = gemini_utils.generate_gemini_content(
                genai_client=client,
                model_name=model_name,
                contents=history,
                generation_config=agg_generation_config,
                is_structured_mode=is_structured_mode
            )
            logger.info("Gemini aggregation call successful.")
            return [agg_response.text]
        except Exception as e:
            logger.error(f"Gemini aggregation step failed: {e}", exc_info=True)
            return [f"Error during Gemini aggregation: {e}"]

# --- Single Shot Processing (Provider-aware) ---
def process_all_at_once(
    records: List[Union[str, types.Part]], 
    prompt: str, 
    provider_type: str,
    model_type: str, 
    api_key_type: str,
    is_structured_mode: bool, 
    schema_name: Optional[str]
) -> Tuple[List[str], List[Dict[str, Any]]]:
    """Processes all records in a single API call, provider-aware."""
    if not records:
        return [], []
    logger.info(f"Starting single-shot processing for {len(records)} records using {provider_type}")
    
    if provider_type == "fireworks":
        # Fireworks processing
        try:
            # Prepare mixed content message
            content_blocks = []
            
            # Add file URLs
            for url in records:
                if isinstance(url, str):
                    content_blocks.append(prepare_fireworks_file_url_content(url))
            
            # Add text prompt
            content_blocks.append(prepare_fireworks_text_content(prompt))
            
            # Create message with mixed content
            messages = [prepare_fireworks_mixed_content_message(content_blocks, "user")]
            
            logger.info("Calling Fireworks API with all records...")

            responsetuple = generate_fireworks_content(
                messages=messages,
                max_tokens=121000
            )

            if responsetuple is None:
                raise Exception("Fireworks API returned None response")

            response_text, usage_info = responsetuple
            
            logger.info("Fireworks API call successful.")
            return [response_text], [usage_info] if usage_info else []
            
        except Exception as e:
            logger.error(f"Error during Fireworks single-shot processing: {e}", exc_info=True)
            error_response = f"Error: Fireworks processing failed: {e}"
            return [error_response], []
    
    else:
        # Original Gemini processing logic
        try:
            client, model_name = gemini_utils.configure_gemini(model_type, api_key_type)
            
            resolved_schema_class = None
            if is_structured_mode and schema_name:
                resolved_schema_class = gemini_utils.resolve_schema_class(schema_name)
                if not resolved_schema_class:
                    logger.warning(f"Schema '{schema_name}' not found. Model will infer JSON structure.")

            sys_instructions = gemini_utils.load_system_instructions(is_structured_mode)
            gen_config_args = {
                "system_instruction": sys_instructions,
                "max_output_tokens": 65536,
            }
            if is_structured_mode:
                gen_config_args["response_mime_type"] = "application/json"
                if resolved_schema_class:
                    gen_config_args["response_schema"] = resolved_schema_class
                    logger.info(f"Requesting JSON output with schema: {schema_name}")
                else:
                    logger.info("Requesting JSON output with model-inferred schema.")
            
            gen_config_args["thinking_config"] = types.ThinkingConfig(thinking_budget=20000)
            generation_config = types.GenerateContentConfig(**gen_config_args)
            
            contents = records + [prompt]
            logger.info("Calling Gemini API with all records...")

            response = gemini_utils.generate_gemini_content(
                genai_client=client,
                model_name=model_name,
                contents=contents,
                generation_config=generation_config,
                is_structured_mode=is_structured_mode
            )

            if response is None:
                raise errors.UnexpectedNoneError("response", "Response was None/empty")

            if is_structured_mode and resolved_schema_class:
                gemini_utils.validate_json_string_against_model(
                    json_string=response.text, model_class=resolved_schema_class
                )

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
            error_response = f"Error: Gemini processing failed: {e}"
            return [error_response], []

# --- Main CLI Execution ---
def main_cli():
    """Main function for the CLI tool."""
    parser = argparse.ArgumentParser(description="Process documents using Gemini API or Fireworks AI via CLI (Single Call).")
    parser.add_argument("model_type", choices=['pro', 'flash'], help="Gemini model type (ignored for Fireworks).")
    parser.add_argument("api_key_type", choices=['free', 'paid'], help="API key type (ignored for Fireworks).")
    parser.add_argument("prompt_file", help="Path to the file containing the main prompt.")
    parser.add_argument("-i", "--input-source", type=str, default=None, help="Path to input file (lines) or directory (files). If omitted, runs with dummy input. For Fireworks, static URLs are used instead.")
    
    # Schema and JSON output arguments
    parser.add_argument("-s", "--schema", type=str, default=None, help="Name of Pydantic schema for specific JSON output. If used, implies --json-output. (Gemini only)")
    parser.add_argument("--json-output", action="store_true", help="Request generic JSON output (model-inferred schema if --schema is not provided or found). (Gemini only)")
    
    parser.add_argument("-o", "--output-config", type=str, default="./output_version.json", help="Path to output version config JSON.")
    parser.add_argument("-u", "--usage-file", type=str, default=None, help="Path to JSON file for tracking token usage.")
    parser.add_argument("--aggregate", action="store_true", help="Perform an aggregation step on the results.")
    parser.add_argument("--agg-prompt", type=str, default="Summarize the preceding responses.", help="Prompt to use for the aggregation step.")
    parser.add_argument("--listv", action="store_true", help="List all available schemas, verbose view (Gemini only)")
    parser.add_argument("--list", action="store_true", help="List all available schemas, summary view (Gemini only)")

    args = parser.parse_args()

    # --- Determine Provider ---
    provider_type = get_provider_type()
    logger.info(f"Using AI provider: {provider_type}")

    # --- Load Inputs ---
    logger.info("Loading inputs...")
    prompt = load_prompt_from_file(args.prompt_file)
    if prompt is None: sys.exit(1)

    records = []
    if args.input_source:
        records = load_input_records(args.input_source, provider_type)
        if not records: 
            logger.error("Input source specified, but no records loaded.")
            sys.exit(1)
    else:
        if provider_type == "fireworks":
            logger.info("No input source specified for Fireworks. Using static URLs.")
            records = FIREWORKS_STATIC_URLS
        else:
            logger.warning("No input source specified. Running in 'dummy input' mode with a single placeholder.")
            records = ["Placeholder dummy input record."]

    # --- Determine Mode (Gemini only) ---
    is_structured_mode = False
    if provider_type == "gemini":
        is_structured_mode = args.json_output or bool(args.schema)
        
        if is_structured_mode:
            if args.schema:
                logger.info(f"Structured JSON output mode enabled (schema: {args.schema}).")
            else:
                logger.info("Structured JSON output mode enabled (model-inferred schema).")
        else:
            logger.info("Text output mode enabled.")

        if args.listv:
            gemini_utils.print_all_schemas()
            sys.exit(0)

        if args.list:
            gemini_utils.print_schema_summary()
            sys.exit(0)
    else:
        if args.schema or args.json_output:
            logger.warning("Schema and JSON output options are ignored when using Fireworks AI.")
        if args.listv or args.list:
            logger.warning("Schema listing is not available for Fireworks AI.")
            sys.exit(0)
    
    # --- Process all records in a single API call ---
    all_responses, all_usage_dicts = process_all_at_once(
        records=records, 
        prompt=prompt, 
        provider_type=provider_type,
        model_type=args.model_type, 
        api_key_type=args.api_key_type, 
        is_structured_mode=is_structured_mode,
        schema_name=args.schema
    )

    # --- Optional Aggregation Step ---
    final_responses = all_responses
    if args.aggregate:
        if not all_responses:
             logger.warning("Aggregation requested, but no initial responses to aggregate.")
        else:
            logger.info("Performing aggregation...")
            try:
                final_responses = aggregate_responses(
                    base_responses=all_responses,
                    aggregation_prompt=args.agg_prompt,
                    provider_type=provider_type,
                    model_type=args.model_type,
                    api_key_type=args.api_key_type,
                    is_structured_mode=is_structured_mode, 
                    schema_name=args.schema
                )
            except Exception as agg_err:
                logger.error(f"Aggregation failed: {agg_err}", exc_info=True)
                final_responses.append(f"Error: Aggregation step could not be completed due to: {agg_err}")

    # --- Write Output ---
    logger.info("Writing output files...")
    if provider_type == "gemini":
        gemini_utils.write_output_files(final_responses, args.output_config, is_structured_mode)
    else:
        # Simple output writing for Fireworks (since we don't have gemini_utils for structured mode)
        try:
            with open("fireworks_output.txt", "w", encoding="utf-8") as f:
                for i, response in enumerate(final_responses):
                    f.write(f"=== Response {i+1} ===\n")
                    f.write(response)
                    f.write("\n\n")
            logger.info(f"Fireworks output written to: fireworks_output.txt")
        except Exception as e:
            logger.error(f"Error writing Fireworks output: {e}")

    # --- Update Token Usage (from main processing step only) ---
    if provider_type == "gemini":
        usage_file_path = args.usage_file
        if not usage_file_path: 
             usage_file_path = f"./gemini_tokens_usage_{args.api_key_type}.json"

        if all_usage_dicts:
            logger.info("Updating token usage...")
            class MockUsageMetadata: 
                def __init__(self, data):
                    self.prompt_token_count = data.get('prompt_token_count')
                    self.candidates_token_count = data.get('candidates_token_count')
                    self.total_token_count = data.get('total_token_count')
            usage_metadata_objects = [MockUsageMetadata(d) for d in all_usage_dicts if d]
            gemini_utils.update_gemini_token_usage(usage_metadata_objects, usage_file_path)
    else:
        # Simple usage tracking for Fireworks
        if all_usage_dicts:
            usage_file_path = args.usage_file or "./fireworks_tokens_usage.json"
            try:
                # Load existing usage
                if os.path.exists(usage_file_path):
                    with open(usage_file_path, 'r') as f:
                        existing_usage = json.load(f)
                else:
                    existing_usage = {"total_prompt_tokens": 0, "total_completion_tokens": 0, "total_tokens": 0}
                
                # Add new usage
                for usage_dict in all_usage_dicts:
                    if usage_dict:
                        existing_usage["total_prompt_tokens"] += usage_dict.get("prompt_token_count", 0)
                        existing_usage["total_completion_tokens"] += usage_dict.get("candidates_token_count", 0)
                        existing_usage["total_tokens"] += usage_dict.get("total_token_count", 0)
                
                # Save updated usage
                with open(usage_file_path, 'w') as f:
                    json.dump(existing_usage, f, indent=2)
                logger.info(f"Fireworks token usage updated in: {usage_file_path}")
            except Exception as e:
                logger.error(f"Error updating Fireworks token usage: {e}")

    logger.info("CLI processing complete.")


if __name__ == "__main__":
    try:
        main_cli()
    except KeyboardInterrupt: logger.info("User interrupted."); sys.exit(0)
    except EOFError: logger.info("User interrupted."); sys.exit(0)
    except Exception as e: logger.critical(f"CLI Error: {e}", exc_info=True); sys.exit(1)
