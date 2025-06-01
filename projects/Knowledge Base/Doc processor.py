# your_original_project/gemini_generate_cli.py

import os
import sys
import argparse
import asyncio
import pathlib
import logging
import time
import concurrent.futures
from multiprocessing import cpu_count, Manager, Queue as MpQueue
from queue import Empty as QueueEmpty
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
from dotenv import load_dotenv

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
async def aggregate_responses(
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
    
    resolved_schema_class: Optional[Type[BaseModel]] = None
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

# --- Parallel Processing ---
# Worker function remains the same as the previous corrected version

def process_record_sync_wrapper(
    record: Union[str, types.Part], prompt: str, model_type: str, api_key_type: str,
    is_structured_mode: bool, schema_name: Optional[str], # schema_name can be None
    results_queue: MpQueue, usage_queue: MpQueue
    ) -> None:
    worker_logger = logging.getLogger(f"worker_{os.getpid()}")
    worker_logger.info("Worker started.")
    response_text = "Error: Worker initialization failed"
    usage_info = None
    try:
        client_in_worker, model_name_in_worker = gemini_utils.configure_gemini(model_type, api_key_type)
        
        resolved_schema_class: Optional[Type[BaseModel]] = None
        if is_structured_mode:
            if schema_name: # A specific schema name was provided
                resolved_schema_class = gemini_utils.resolve_schema_class(schema_name)
                if not resolved_schema_class:
                    worker_logger.warning(
                        f"Schema '{schema_name}' not found or invalid. "
                        "Worker will use model-inferred JSON structure if applicable."
                    )
            # If no schema_name, resolved_schema_class remains None; model infers structure.

        sys_instructions = gemini_utils.load_system_instructions(is_structured_mode)
        
        gen_config_args: Dict[str, Any] = {
            "system_instruction": sys_instructions,
            "max_output_tokens": 65536, # Consider making this configurable
        }

        if is_structured_mode:
            gen_config_args["response_mime_type"] = "application/json"
            if resolved_schema_class: # Only add schema if one was successfully resolved
                gen_config_args["response_schema"] = resolved_schema_class
                worker_logger.info(f"Worker will use schema: {schema_name}")
            else:
                worker_logger.info("Worker will use model-inferred JSON structure.")

        gen_config_args ["thinking_config"] = types.ThinkingConfig (thinking_budget=20000)

        generation_config = types.GenerateContentConfig(**gen_config_args)
        
        contents = [record, prompt]
        worker_logger.info("Calling Gemini API...")

        response: types.GenerateContentResponse = gemini_utils.generate_gemini_content(
            genai_client=client_in_worker,
            model_name=model_name_in_worker,
            contents=contents,
            generation_config=generation_config,
            is_structured_mode=is_structured_mode # Pass mode for logging
        )

        if response is None:
            raise errors.UnexpectedNoneError ("response", "Response was None/empty")


        if is_structured_mode:
            if resolved_schema_class:
                gemini_utils.validate_json_string_against_model (json_string=response.text, model_class=resolved_schema_class)


        if response.usage_metadata:
             usage_info = { "prompt_token_count": response.usage_metadata.prompt_token_count,
                            "candidates_token_count": response.usage_metadata.candidates_token_count,
                            "total_token_count": response.usage_metadata.total_token_count }

        response_text = response.text
        worker_logger.info("API call successful.")


    except Exception as e:
        worker_logger.error(f"Error in worker: {e}", exc_info=True)
        response_text = f"Error: Worker failed: {e}"
        usage_info = None
    
    try:
        results_queue.put(response_text)
        usage_queue.put(usage_info)
    except Exception as q_err:
        worker_logger.error(f"Queue put error: {q_err}")



# Main parallel execution logic remains the same as previous corrected version
def parallelize_processing(
    records: List[Union[str, types.Part]], prompt: str, model_type: str, api_key_type: str,
    is_structured_mode: bool, schema_name: Optional[str]
) -> Tuple[List[str], List[Dict[str, Any]]]:
    # (Implementation identical to the previous corrected version)
    # Uses Manager, ProcessPoolExecutor, submits wrapper, collects from queues
    num_workers = min(cpu_count(), len(records)) if records else 0
    if num_workers == 0: return [], []
    logger.info(f"Starting parallel processing: {num_workers} workers / {len(records)} records.")
    all_responses, all_usage_dicts = [], []
    with Manager() as manager:
        results_queue, usage_queue = manager.Queue(), manager.Queue()
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(process_record_sync_wrapper, r, prompt, model_type, api_key_type,
                                       is_structured_mode, schema_name, results_queue, usage_queue)
                       for r in records]
            processed_count = 0; start_time = time.time()
            while processed_count < len(records):
                 try:
                     response_text = results_queue.get(timeout=60) # Increased timeout
                     usage_info = usage_queue.get(timeout=60)
                     all_responses.append(response_text)
                     if usage_info: all_usage_dicts.append(usage_info)
                     processed_count += 1
                     if processed_count % 10 == 0 or processed_count == len(records):
                         logger.info(f"Collected {processed_count}/{len(records)} results... ({time.time() - start_time:.1f}s)")
                 except QueueEmpty:
                     logger.warning("Result queue empty after timeout. Checking futures...")
                     # Basic check if any futures failed (more robust error handling could be added)
                     done, not_done = concurrent.futures.wait(futures, timeout=0.1, return_when=concurrent.futures.FIRST_EXCEPTION)
                     if any(f.exception() for f in done): logger.error("At least one worker future raised an exception."); break
                     if time.time() - start_time > 600: logger.error("Timeout waiting > 10min for results."); break # Overall timeout
                     continue
                 except Exception as e: logger.error(f"Error collecting results: {e}"); break # Stop collecting on other errors
            # Check for mismatch
            if processed_count != len(records):
                 logger.warning(f"Result count mismatch: Expected {len(records)}, got {processed_count}. Appending errors.")
                 for _ in range(len(records) - processed_count): all_responses.append("Error: Result missing (timeout or worker failure)")
    logger.info(f"Parallel processing finished. Collected {len(all_responses)} responses.")
    return all_responses, all_usage_dicts

# --- Main CLI Execution ---
async def main_cli():
    """Main asynchronous function for the CLI tool."""
    parser = argparse.ArgumentParser (description="Process documents using Gemini API via CLI (Parallel).")
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
    start_total_time = time.time()

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
    
    # --- Parallel Processing ---
    # args.schema will be None if --schema flag was not used. This is the desired schema_name to pass.
    all_responses, all_usage_dicts = parallelize_processing(
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
                final_responses = await aggregate_responses(
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

    # --- Update Token Usage (from parallel step only) ---
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

    total_time = time.time() - start_total_time
    logger.info(f"CLI processing complete in {total_time:.2f} seconds.")


if __name__ == "__main__":
    load_dotenv() # Load .env from CWD (project root)
    try:
        asyncio.run(main_cli()) # main_cli needs async for potential aggregation step
    except KeyboardInterrupt: logger.info("User interrupted."); sys.exit(0)
    except EOFError: logger.info("User interrupted."); sys.exit(0)
    except Exception as e: logger.critical(f"CLI Error: {e}", exc_info=True); sys.exit(1)
