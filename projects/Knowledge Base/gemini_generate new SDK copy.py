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
    from src.utils import gemini_utils
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
                if f.endswith((".txt", ".md", ".json")):
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
    client: genai.client.Client, # Needs configured client
    model_name: str,             # Needs model name
    is_structured_mode: bool,    # Needs mode for sys instructions
    schema_name: Optional[str]   # Needs schema name for sys instructions / config
) -> List[str]:
    """Performs an aggregation step on the initial responses."""
    if not base_responses:
        logger.warning("No base responses to aggregate.")
        return []
    if not aggregation_prompt:
        logger.warning("No aggregation prompt provided.")
        return base_responses # Return original if no prompt

    logger.info("Performing aggregation step...")
    # Use the *same* mode (structured/text) for the aggregation step?
    # Or should aggregation always be text? Let's assume same mode for now.
    sys_instructions = gemini_utils.load_system_instructions(is_structured_mode)
    schema_class = None
    if is_structured_mode and schema_name:
        schema_class = gemini_utils.resolve_schema_class(schema_name)

    gen_config_args = {
        "system_instruction": sys_instructions, "max_output_tokens": 8192,
    }
    if is_structured_mode and schema_class:
        gen_config_args["response_mime_type"] = "application/json"
        gen_config_args["response_schema"] = schema_class
    agg_generation_config = types.GenerateContentConfig(**gen_config_args)

    # Construct history for aggregation call
    # Combine base responses and the aggregation prompt
    # Ensure history doesn't get excessively long?
    history = base_responses + [aggregation_prompt]

    try:
        agg_response = gemini_utils.generate_gemini_content (
            genai_client=client,
            model_name=model_name,
            contents=history, # Send history as contents
            generation_config=agg_generation_config,
            is_structured_mode=is_structured_mode
        )
        logger.info("Aggregation call successful.")
        # Return the aggregation result as a single-item list
        return [agg_response.text]
    except Exception as e:
        logger.error(f"Aggregation step failed: {e}", exc_info=True)
        return [f"Error during aggregation: {e}"] # Return error message

# --- Parallel Processing ---
# Worker function remains the same as the previous corrected version
def process_record_sync_wrapper(
    record: Union[str, types.Part], prompt: str, model_type: str, api_key_type: str,
    is_structured_mode: bool, schema_name: Optional[str],
    results_queue: MpQueue, usage_queue: MpQueue
    ) -> None:
    # (Implementation identical to the previous corrected version)
    # It configures client, loads instructions, calls async generate, puts results in queues
    worker_logger = logging.getLogger(f"worker_{os.getpid()}")
    worker_logger.info(f"Worker started.")
    response_text = f"Error: Worker init failed"
    usage_info = None
    try:
        # 1. Configure client IN WORKER
        client_in_worker, model_name_in_worker = gemini_utils.configure_gemini(model_type, api_key_type)
        # 2. Resolve schema IN WORKER
        schema_class = None
        if is_structured_mode and schema_name:
             # Assumes schemas are importable/registered in worker context
             schema_class = gemini_utils.resolve_schema_class(schema_name)
        # 3. Load sys ins IN WORKER
        sys_instructions = gemini_utils.load_system_instructions(is_structured_mode)
        # 4. Prepare Gen Config IN WORKER
        gen_config_args = {"system_instruction": sys_instructions, "max_output_tokens": 65536}
        if is_structured_mode and schema_class:
            gen_config_args["response_mime_type"] = "application/json"
            gen_config_args["response_schema"] = schema_class
        generation_config = types.GenerateContentConfig(**gen_config_args)
        # 5. Prepare Contents
        contents = [record, prompt]
        # 6. Run async API call synchronously
        worker_logger.info("Calling Gemini API...")

        response:types.GenerateContentResponse = gemini_utils.generate_gemini_content( # ** Use sync function **
            genai_client=client_in_worker,
            model_name=model_name_in_worker,
            contents=contents,
            generation_config=generation_config,
            is_structured_mode=is_structured_mode
        )
        response_text = response.text
        if response.usage_metadata:
             usage_info = { "prompt_token_count": response.usage_metadata.prompt_token_count,
                            "candidates_token_count": response.usage_metadata.candidates_token_count,
                            "total_token_count": response.usage_metadata.total_token_count }
        worker_logger.info("API call successful.")

    except Exception as e:
        worker_logger.error(f"Error in worker: {e}", exc_info=True)
        response_text = f"Error: Worker failed: {e}"
        usage_info = None
    # Put results into queues
    try: results_queue.put(response_text); usage_queue.put(usage_info)
    except Exception as q_err: worker_logger.error(f"Queue put error: {q_err}")

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
    parser = argparse.ArgumentParser(description="Process documents using Gemini API via CLI (Parallel).")
    parser.add_argument("model_type", choices=['pro', 'flash'], help="Gemini model type.")
    parser.add_argument("api_key_type", choices=['free', 'paid'], help="API key type.")
    parser.add_argument("prompt_file", help="Path to the file containing the main prompt.")
    parser.add_argument("-i", "--input-source", type=str, default=None, help="Path to input file (lines) or directory (files). If omitted, runs with dummy input.")
    parser.add_argument("-s", "--schema", type=str, default=None, help="Name of Pydantic schema for JSON output.")
    parser.add_argument("-o", "--output-config", type=str, default="./output_version.json", help="Path to output version config JSON.")
    parser.add_argument("-u", "--usage-file", type=str, default=None, help="Path to JSON file for tracking token usage.")
    parser.add_argument("--aggregate", action="store_true", help="Perform an aggregation step on the results.")
    parser.add_argument("--agg-prompt", type=str, default="Summarize the preceding responses.", help="Prompt to use for the aggregation step.")

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
        # ** CORRECTED: Handle dummy input mode **
        logger.warning("No input source specified. Running in 'dummy input' mode with a single placeholder.")
        records = ["Placeholder dummy input record."] # Provide one dummy record

    # --- Determine Mode ---
    is_structured_mode = bool(args.schema)

    # --- Parallel Processing ---
    all_responses, all_usage_dicts = parallelize_processing(
        records=records, prompt=prompt, model_type=args.model_type,
        api_key_type=args.api_key_type, is_structured_mode=is_structured_mode,
        schema_name=args.schema
    )

    # --- Optional Aggregation Step ---
    final_responses = all_responses
    if args.aggregate:
        if not all_responses:
             logger.warning("Aggregation requested, but no initial responses to aggregate.")
        else:
            logger.info("Performing aggregation...")
            # Need to configure a client again for the main thread aggregation call
            try:
                agg_client, agg_model_name = gemini_utils.configure_gemini(args.model_type, args.api_key_type)
                # Run aggregation async
                final_responses = await aggregate_responses(
                    base_responses=all_responses,
                    aggregation_prompt=args.agg_prompt,
                    client=agg_client,
                    model_name=agg_model_name,
                    is_structured_mode=is_structured_mode, # Use same mode for agg
                    schema_name=args.schema
                )
                # Note: Aggregation currently doesn't track token usage easily
            except Exception as agg_err:
                logger.error(f"Failed to configure client for aggregation: {agg_err}")
                final_responses.append(f"Error: Could not configure client for aggregation step.")


    # --- Write Output ---
    logger.info("Writing output files...")
    # Write final_responses (which might be aggregated or original)
    gemini_utils.write_output_files(final_responses, args.output_config, is_structured_mode)

    # --- Update Token Usage (from parallel step only) ---
    usage_file_path = args.usage_file
    if not usage_file_path: # Default based on key type
         usage_file_path = f"./gemini_tokens_usage_{args.api_key_type}.json"

    if all_usage_dicts:
        logger.info("Updating token usage...")
        class MockUsageMetadata: # Helper to mimic UsageMetadata structure
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
