# watch_combined.py
# A new script to orchestrate a two-step AI process:
# 1. Use Google Gemini for OCR on local images.
# 2. Use Fireworks AI for analysis on the extracted text.

# =====================================================================================
# MONKEY-PATCH FOR PROTOBUF (Still required as both libraries are used)
# =====================================================================================
import os
import sys
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import google.protobuf.descriptor_pool
from google.protobuf.internal import api_implementation

if api_implementation.Type() != 'python':
    print("Warning: Protobuf C++ backend is active. Patch may be ineffective.", file=sys.stderr)

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

# --- Regular Imports ---
import argparse
import pathlib
import logging
import json
from typing import List, Optional, Tuple, Dict

# Local/Project specific imports
try:
    from src.utils import gemini_utils, errors
except ImportError as e:
     print(f"Error importing local modules. Run from project root. Error: {e}", file=sys.stderr)
     sys.exit(1)

# Third-party imports
from google.genai import types as genai_types
from fireworks import LLM
from dotenv import load_dotenv

# --- Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("combined_cli")
load_dotenv("/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/.env")

# --- Fireworks AI Configuration ---
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
FIREWORKS_MODEL = os.getenv("FIREWORKS_MODEL", "accounts/fireworks/models/deepseek-r1-basic")


# --- Core Functions ---

def load_local_image_files(input_dir: str) -> List[genai_types.Part]:
    """Loads all supported image files from a directory into Gemini Part objects."""
    records = []
    source_path = pathlib.Path(input_dir)
    if not source_path.is_dir():
        logger.error(f"Input directory not found: {source_path}")
        return []

    logger.info(f"Loading image files for OCR from: {source_path}")
    mime_map = {'.jpeg': 'image/jpeg', '.jpg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.gif': 'image/gif'}
    
    for f in os.listdir(source_path):
        file_path = source_path / f
        if file_path.suffix.lower() in mime_map:
            try:
                mime_type = mime_map[file_path.suffix.lower()]
                part = genai_types.Part.from_bytes(data=file_path.read_bytes(), mime_type=mime_type)
                records.append(part)
                logger.info(f"  - Loaded {f} ({mime_type})")
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}", exc_info=True)
        else:
            logger.warning(f"Skipping unsupported file in dir: {f}")
            
    logger.info(f"Loaded {len(records)} image files.")
    return records

def perform_ocr_with_gemini(
    image_parts: List[genai_types.Part], 
    api_key_type: str
) -> Tuple[Optional[str], Optional[Dict]]:
    """Uses Gemini Flash to perform OCR on a list of image parts."""
    if not image_parts:
        logger.warning("No image parts provided for OCR.")
        return None, None
    
    logger.info(f"Starting OCR process with Gemini Flash for {len(image_parts)} images...")
    
    try:
        # We always use 'flash' for this task as requested
        client, model_name = gemini_utils.configure_gemini('flash', api_key_type)
    except Exception as e:
        logger.error(f"Failed to configure Gemini client for OCR: {e}")
        return None, None

    # Simple, direct prompt for OCR
    ocr_prompt = "Perform OCR on the provided image(s). Extract all text content accurately. Present the full extracted text without any additional commentary or formatting."
    
    contents = image_parts + [ocr_prompt]
    
    generation_config = genai_types.GenerateContentConfig(
        max_output_tokens=8192,  # Generous token limit for OCR
        temperature=0.0 # Low temperature for factual extraction
    )

    try:
        response = gemini_utils.generate_gemini_content(
            genai_client=client,
            model_name=model_name,
            contents=contents,
            generation_config=generation_config,
            is_structured_mode=False
        )

        if not response or not response.text:
            raise errors.UnexpectedNoneError("response.text", "Gemini OCR returned no text.")

        usage_info = None
        if response.usage_metadata:
            usage_info = {
                "prompt_token_count": response.usage_metadata.prompt_token_count,
                "candidates_token_count": response.usage_metadata.candidates_token_count,
                "total_token_count": response.usage_metadata.total_token_count
            }
        
        logger.info("Gemini OCR successful.")
        return response.text, usage_info

    except Exception as e:
        logger.error(f"Error during Gemini OCR API call: {e}", exc_info=True)
        return None, None

def analyze_text_with_fireworks(
    ocr_text: str, 
    analysis_prompt: str
) -> Tuple[Optional[str], Optional[Dict]]:
    """Sends extracted text and an analysis prompt to Fireworks AI."""
    logger.info("Starting analysis of OCR'd text with Fireworks AI...")
    if not FIREWORKS_API_KEY:
        logger.error("FATAL: FIREWORKS_API_KEY environment variable not set.")
        return None, None

    # Combine the OCR'd text and the user's prompt into a single message
    combined_prompt = f"""CONTEXT: The following text was extracted from a series of images using OCR.

--- OCR TEXT START ---
{ocr_text}
--- OCR TEXT END ---

TASK: Now, please perform the following task based on the text provided above.

--- TASK START ---
{analysis_prompt}
--- TASK END ---
"""

    messages = [{"role": "user", "content": combined_prompt}]
    
    try:
        llm = LLM(model=FIREWORKS_MODEL, api_key=FIREWORKS_API_KEY)
        response_generator = llm.chat.completions.create(
            messages=messages,
            max_tokens=8192,
            stream=True,
            temperature=0.1
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
        
        logger.info("Fireworks AI analysis successful.")
        return response_text, usage_info
    except Exception as e:
        logger.error(f"Error during Fireworks AI API call: {e}", exc_info=True)
        return None, None

# --- Main CLI Execution ---
def main_cli():
    parser = argparse.ArgumentParser(description="Process images via Gemini OCR and Fireworks AI analysis.")
    parser.add_argument("api_key_type", choices=['free', 'paid'], help="API key type for Gemini OCR step.")
    parser.add_argument("prompt_file", help="Path to the file containing the main analysis prompt for Fireworks.")
    parser.add_argument("-i", "--input-source", required=True, type=str, help="Path to input directory containing image files.")
    parser.add_argument("-o", "--output-config", type=str, default="./output_version.json", help="Path to output version config JSON.")
    parser.add_argument("-u", "--usage-file", type=str, default="./combined_tokens_usage.json", help="Path to JSON file for tracking total token usage.")
    args = parser.parse_args()

    # --- Step 1: Load local image files ---
    image_parts = load_local_image_files(args.input_source)
    if not image_parts:
        logger.error("No valid images found in input source. Aborting.")
        sys.exit(1)

    # --- Step 2: Perform OCR with Gemini Flash ---
    ocr_text, gemini_usage = perform_ocr_with_gemini(image_parts, args.api_key_type)
    if not ocr_text:
        logger.error("OCR step failed. Aborting.")
        sys.exit(1)
        
    # --- Step 3: Load the main analysis prompt ---
    analysis_prompt = gemini_utils.load_prompt_from_file(args.prompt_file)
    if not analysis_prompt:
        logger.error(f"Could not load analysis prompt from {args.prompt_file}. Aborting.")
        sys.exit(1)

    # --- Step 4: Analyze extracted text with Fireworks ---
    final_response, fireworks_usage = analyze_text_with_fireworks(ocr_text, analysis_prompt)
    if not final_response:
        logger.error("Fireworks analysis step failed. Aborting.")
        sys.exit(1)

    # --- Step 5: Write Output ---
    logger.info("Writing final output...")
    # Using gemini_utils.write_output_files as it's a generic text writer
    gemini_utils.write_output_files([final_response], args.output_config, is_structured_mode=False)

    # --- Step 6: Update Combined Token Usage ---
    logger.info("Updating token usage log...")
    total_usage = {
        "gemini_ocr_usage": gemini_usage or {},
        "fireworks_analysis_usage": fireworks_usage or {},
        "total_prompt_tokens": (gemini_usage or {}).get("prompt_token_count", 0) + (fireworks_usage or {}).get("prompt_token_count", 0),
        "total_completion_tokens": (gemini_usage or {}).get("candidates_token_count", 0) + (fireworks_usage or {}).get("candidates_token_count", 0),
    }
    total_usage["total_tokens"] = total_usage["total_prompt_tokens"] + total_usage["total_completion_tokens"]

    try:
        # We'll just overwrite the file each time with the latest run's details
        # A more robust system would append to a list in the JSON file.
        with open(args.usage_file, 'w') as f:
            json.dump(total_usage, f, indent=2)
        logger.info(f"Token usage for this run saved to: {args.usage_file}")
    except Exception as e:
        logger.error(f"Failed to write token usage file: {e}")

    logger.info("CLI processing complete.")

if __name__ == "__main__":
    try:
        main_cli()
    except KeyboardInterrupt:
        logger.info("User interrupted.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"A critical error occurred: {e}", exc_info=True)
        sys.exit(1)
