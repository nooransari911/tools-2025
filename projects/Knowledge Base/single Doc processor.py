# your_original_project/gemini_generate_cli.py

import os
import sys
import argparse
import pathlib
import logging
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
from google import genai, generativeai
from dotenv import load_dotenv # Used in __main__

# Setup logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("gemini_cli")

# --- Input Loading ---
def load_input_records(input_source: str) -> List[Union[str, types.Part]]:
    """Loads input records from files/dir or lines/file."""
    # (Implementation same as before)
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
    # (Implementation same as before)
    path = pathlib.Path(prompt_file_path)
    if not path.is_file(): logger.error(f"Prompt file not found: {path}"); return None
    try:
        with open(path, "r", encoding='utf-8') as prompt_file: return prompt_file.read()
    except Exception as e: logger.error(f"Error reading prompt file {path}: {e}", exc_info=True); return None

# --- Aggregation Function ---
def aggregate_responses(
    base_responses: List[str],
    aggregation_prompt: str,
    client: genai.client.Client,
    model_name: str,
    is_structured_mode: bool,
    schema_name: Optional[str] # schema_name can be None
) -> List[str]:
    """Performs an aggregation step on the initial responses."""
    if not base_responses:
        logger.warning("No base responses to aggregate.")
        return []
    if not aggregation_prompt:
        logger.warning("No aggregation prompt provided.")
        return base_responses

    logger.info("Performing aggregation step...")
    sys_instructions = gemini_utils.load_system_instructions(is_structured_mode)
    
    resolved_schema_class: Optional[type] = None
    if is_structured_mode:
        if schema_name: # If a specific schema name was provided for aggregation
            resolved_schema_class = gemini_utils.resolve_schema_class(schema_name)
            if not resolved_schema_class:
                logger.warning(
                    f"Aggregation schema '{schema_name}' not found or invalid. "
                    "Aggregation will use model-inferred JSON structure if applicable."
                )
        # If no schema_name, resolved_schema_class remains None; model infers structure.

    gen_config_args: Dict[str, Any] = {
        "system_instruction": sys_instructions,
        "max_output_tokens": 8192, # Consider making this configurable
    }

    if is_structured_mode:
        gen_config_args["response_mime_type"] = "application/json"
        if resolved_schema_class: # Only add schema if one was successfully resolved
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
            is_structured_mode=is_structured_mode # Pass mode for logging in generate_gemini_content
        )
        logger.info("Aggregation call successful.")
        # Ensure usage metadata for aggregation is handled if needed (currently not)
        return [agg_response.text]
    except Exception as e:
        logger.error(f"Aggregation step failed: {e}", exc_info=True)
        return [f"Error during aggregation: {e}"]

# --- Single Shot Processing ---
def process_all_at_once(
    records: List[Union[str, types.Part]], prompt: str, model_type: str, api_key_type: str,
    is_structured_mode: bool, schema_name: Optional[str]
) -> Tuple[List[str], List[Dict[str, Any]]]:
    """Processes all records in a single API call."""
    if not records:
        return [], []
    logger.info(f"Starting single-shot processing for {len(records)} records.")
    
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
        
        # Combine all records and the prompt into a single list for the API call
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
        
        logger.info("API call successful.")
        # Return response and usage info wrapped in lists to maintain original data structure
        return [response.text], [usage_info] if usage_info else []

    except Exception as e:
        logger.error(f"Error during single-shot processing: {e}", exc_info=True)
        error_response = f"Error: Processing failed: {e}"
        return [error_response], []

# --- Main CLI Execution ---
def main_cli():
    """Main function for the CLI tool."""
    parser = argparse.ArgumentParser (description="Process documents using Gemini API via CLI (Single Call).")
    parser.add_argument("model_type", choices=['pro', 'flash'], help="Gemini model type.")
    parser.add_argument("api_key_type", choices=['free', 'paid'], help="API key type.")
    parser.add_argument("prompt_file", help="Path to the file containing the main prompt.")
    parser.add_argument("-i", "--input-source", type=str, default=None, help="Path to input file (lines) or directory (files). If omitted, runs with dummy input.")
    
    # Schema and JSON output arguments
    parser.add_argument("-s", "--schema", type=str, default=None, help="Name of Pydantic schema for specific JSON output. If used, implies --json-output.")
    parser.add_argument("--json-output", action="store_true", help="Request generic JSON output (model-inferred schema if --schema is not provided or found).")
    
    parser.add_argument("-o", "--output-config", type=str, default="./output_version.json", help="Path to output version config JSON.")
    parser.add_argument("-u", "--usage-file", type=str, default=None, help="Path to JSON file for tracking token usage.")
    parser.add_argument("--aggregate", action="store_true", help="Perform an aggregation step on the results.")
    parser.add_argument("--agg-prompt", type=str, default="Summarize the preceding responses.", help="Prompt to use for the aggregation step.")
    parser.add_argument ("--listv", action="store_true", help="List all available schemas, verbose view")
    parser.add_argument ("--list", action="store_true", help="List all available schemas, summary view")

    args = parser.parse_args()

    # --- Load Inputs ---
    logger.info("Loading inputs...")
    prompt = load_prompt_from_file(args.prompt_file)
    if prompt is None: sys.exit(1)

    records = []
    if args.input_source:
        records = load_input_records(args.input_source)
        if not records: logger.error("Input source specified, but no records loaded."); sys.exit(1)
    else:
        logger.warning("No input source specified. Running in 'dummy input' mode with a single placeholder.")
        records = ["Placeholder dummy input record."] 

    # --- Determine Mode ---
    # is_structured_mode is true if a specific schema is requested OR if generic JSON output is requested.
    is_structured_mode = args.json_output or bool(args.schema)
    
    if is_structured_mode:
        if args.schema:
            logger.info(f"Structured JSON output mode enabled (schema: {args.schema}).")
        else: # args.json_output must be true, args.schema is None
            logger.info("Structured JSON output mode enabled (model-inferred schema).")
    else:
        logger.info("Text output mode enabled.")

    if args.listv:
        gemini_utils.print_all_schemas ()
        sys.exit (0)

    if args.list:
        gemini_utils.print_schema_summary ()
        sys.exit (0)
    
    # --- Process all records in a single API call ---
    all_responses, all_usage_dicts = process_all_at_once(
        records=records, prompt=prompt, model_type=args.model_type, 
        api_key_type=args.api_key_type, is_structured_mode=is_structured_mode,
        schema_name=args.schema # Pass args.schema (which can be None) as schema_name
    )

    # --- Optional Aggregation Step ---
    final_responses = all_responses
    if args.aggregate:
        if not all_responses:
             logger.warning("Aggregation requested, but no initial responses to aggregate.")
        else:
            logger.info("Performing aggregation...")
            try:
                agg_client, agg_model_name = gemini_utils.configure_gemini(args.model_type, args.api_key_type)
                final_responses = aggregate_responses(
                    base_responses=all_responses,
                    aggregation_prompt=args.agg_prompt,
                    client=agg_client,
                    model_name=agg_model_name,
                    is_structured_mode=is_structured_mode, 
                    schema_name=args.schema # Pass args.schema for aggregation too
                )
            except Exception as agg_err:
                logger.error(f"Failed to configure client for aggregation or aggregation failed: {agg_err}", exc_info=True)
                # Append error to final_responses to indicate aggregation failure
                final_responses.append(f"Error: Aggregation step could not be completed due to: {agg_err}")

    # --- Write Output ---
    logger.info("Writing output files...")
    gemini_utils.write_output_files(final_responses, args.output_config, is_structured_mode)

    # --- Update Token Usage (from main processing step only) ---
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

    logger.info("CLI processing complete.")


if __name__ == "__main__":
    load_dotenv() # Load .env from CWD (project root)
    try:
        main_cli()
    except KeyboardInterrupt: logger.info("User interrupted."); sys.exit(0)
    except EOFError: logger.info("User interrupted."); sys.exit(0)
    except Exception as e: logger.critical(f"CLI Error: {e}", exc_info=True); sys.exit(1)
