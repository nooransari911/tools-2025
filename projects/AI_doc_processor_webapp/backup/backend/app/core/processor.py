# ai_doc_processor_webapp/backend/app/core/processor.py
import os
import json
import logging
import asyncio
from typing import Optional, Dict, Any, List, Union, Tuple

# Third-party imports
from google.genai import types
import google.api_core.exceptions
from pydantic import BaseModel

# Import schemas and utils
from ..schemas.api_models import SingleFileResult, UsageMetadata, ProcessForm # Import ProcessForm
# Assumes main.py added original project root to sys.path
try:
    from src.utils import gemini_utils
    logger = logging.getLogger("api_processor")
    logger.info("Processor: Imported refactored gemini_utils.")
except ImportError as e:
    print(f"FATAL Processor Import Error: Check sys.path. Error: {e}", file=sys.stderr)
    raise

async def process_document_web_multi(
    files_data: List[Tuple[str, bytes, str]], # List of (filename, content_bytes, mime_type)
    form_data: ProcessForm, # Expect the validated Pydantic model
) -> Dict[str, Any]:
    """
    Processes multiple documents for the web app using refactored gemini_utils.
    Loops through files, calls API for each, aggregates results.
    """
    # Initialize overall response structure
    overall_result = {
        "status": "success",
        "overall_error_message": None,
        "results": [],
        "schema_used": None,
        "overall_usage_metadata": {"prompt_token_count": 0, "candidates_token_count": 0, "total_token_count": 0}
    }
    all_succeeded = True
    any_succeeded = False

    logger.info(f"Processing {len(files_data)} files: schema='{form_data.schema_name}', model='{form_data.model_type}', key='{form_data.api_key_type}'")

    try:
        # --- 1. Determine Mode & Schema ONCE for the batch --- 
        effective_schema_name = form_data.schema_name if form_data.schema_name != "(No Schema - Plain Text)" else None
        selected_schema_class = None
        is_structured_mode = False
        if effective_schema_name:
            selected_schema_class = gemini_utils.resolve_schema_class(effective_schema_name)
            if selected_schema_class:
                resolved_name = selected_schema_class.__name__
                overall_result["schema_used"] = resolved_name
                is_structured_mode = True
                if resolved_name == gemini_utils.DEFAULT_SCHEMA_NAME and effective_schema_name != gemini_utils.DEFAULT_SCHEMA_NAME:
                    logger.warning(f"Schema fallback: '{effective_schema_name}' -> '{resolved_name}'.")
                    overall_result["schema_used"] = f"{effective_schema_name} (Not Found -> Default: {resolved_name})"
            else: is_structured_mode = False
        else: is_structured_mode = False
        logger.info(f"Batch Mode: Structured={is_structured_mode}, Schema='{overall_result['schema_used'] or 'None'}'")

        # --- 2. Configure Gemini Client & Model ONCE --- 
        client, model_name = gemini_utils.configure_gemini(form_data.model_type, form_data.api_key_type)

        # --- 3. Load System Instructions ONCE --- 
        sys_instructions_str = gemini_utils.load_system_instructions(is_structured_mode)

        # --- 4. Prepare Common Generation Config Args --- 
        gen_config_args = { "max_output_tokens": 8192 }
        if sys_instructions_str: gen_config_args["system_instruction"] = sys_instructions_str
        if is_structured_mode and selected_schema_class:
            gen_config_args["response_mime_type"] = "application/json"
            gen_config_args["response_schema"] = selected_schema_class
        try:
            # Use correct type: GenerateContentConfig
            base_generation_config = types.GenerateContentConfig(**gen_config_args)
            logger.debug("Created base GenerateContentConfig.")
        except Exception as config_err: raise ValueError(f"Internal config error: {config_err}") from config_err


        # --- 5. Loop Through Files and Process Each --- 
        total_prompt_tokens = 0
        total_candidates_tokens = 0
        total_tokens = 0

        for filename, file_content, file_mime_type in files_data:
            logger.info(f"Processing file: {filename} ({len(file_content)} bytes)")
            single_file_result = SingleFileResult(file_name=filename, status="processing") # Use Pydantic model
            
            try:
                # --- 5a. Prepare Input Content for this file --- 
                contents: List[Union[str, types.Part]] = []
                processed_mime_type = file_mime_type.lower() if file_mime_type else 'application/octet-stream'
                if processed_mime_type.startswith("text/") or processed_mime_type == "application/json":
                    try: contents = [file_content.decode("utf-8-sig"), form_data.prompt]
                    except UnicodeDecodeError: raise ValueError("Failed to decode text file as UTF-8.")
                elif processed_mime_type in ["application/pdf", "image/jpeg", "image/png", "image/webp", "image/gif", "image/jpg"]:
                    mime_map = {'image/jpg': 'image/jpeg'}; final_mime = mime_map.get(processed_mime_type, processed_mime_type)
                    contents = [types.Part.from_bytes(data=file_content, mime_type=final_mime), form_data.prompt]
                else: raise ValueError(f"Unsupported file type: {processed_mime_type}")

                # --- 5b. Call Gemini API (using asyncio.to_thread) --- 
                logger.debug(f"Calling API for {filename}...")
                gemini_response = await asyncio.to_thread(
                    gemini_utils.generate_gemini_content, # Sync function
                    genai_client=client, model_name=model_name, contents=contents,
                    generation_config=base_generation_config, is_structured_mode=is_structured_mode
                )
                logger.debug(f"API call completed for {filename}.")

                # --- 5c. Process Response for this file --- 
                single_file_result.raw_output = gemini_response.text
                if gemini_response.usage_metadata:
                    prompt_tokens = gemini_response.usage_metadata.prompt_token_count or 0
                    candidates_tokens = gemini_response.usage_metadata.candidates_token_count or 0
                    total_prompt_tokens += prompt_tokens
                    total_candidates_tokens += candidates_tokens
                    total_tokens += gemini_response.usage_metadata.total_token_count or (prompt_tokens + candidates_tokens)
                    # Maybe store per-file usage if needed: 
                    # single_file_result.usage_metadata = UsageMetadata(...) 

                if is_structured_mode:
                    parsed_obj = gemini_utils.parse_json_from_response_text(gemini_response.text)
                    if parsed_obj is not None: 
                        single_file_result.structured_output = parsed_obj
                    else: 
                        logger.warning(f"JSON parse failed for file: {filename}")
                        single_file_result.error_message = "Model response not valid JSON."
                        # Keep status success, but note the parsing issue
                
                single_file_result.status = "success"
                any_succeeded = True

            # --- 5d. Handle Errors for this specific file --- 
            except (google.api_core.exceptions.GoogleAPIError, ValueError, Exception) as file_e:
                logger.error(f"Error processing file {filename}: {type(file_e).__name__}: {file_e}", exc_info=False) # Log less verbosely in loop
                single_file_result.status = "error"
                error_prefix = "API Error" if isinstance(file_e, google.api_core.exceptions.GoogleAPIError) else \
                               "Input Error" if isinstance(file_e, ValueError) else \
                               "Processing Error"
                single_file_result.error_message = f"{error_prefix}: {str(file_e)[:200]}"
                all_succeeded = False # Mark overall status as partial
            
            overall_result["results"].append(single_file_result.model_dump()) # Append result dict

        # --- 6. Finalize Overall Status and Usage --- 
        if not any_succeeded and files_data: # Check if list wasn't empty
            overall_result["status"] = "error"
            overall_result["overall_error_message"] = "Processing failed for all files."
        elif not all_succeeded:
            overall_result["status"] = "partial_success"
        # Else status remains "success"

        overall_result["overall_usage_metadata"] = {
            "prompt_token_count": total_prompt_tokens,
            "candidates_token_count": total_candidates_tokens,
            "total_token_count": total_tokens
        }
        logger.info(f"Overall Usage: {overall_result['overall_usage_metadata']}")

    # --- Handle Errors occurring before the loop --- 
    except (ValueError, ImportError, Exception) as setup_e:
        logger.error(f"Error during setup before processing files: {type(setup_e).__name__}: {setup_e}", exc_info=True)
        overall_result["status"] = "error"
        overall_result["overall_error_message"] = f"Setup Error: {str(setup_e)[:250]}"
        overall_result["results"] = [] # No individual results if setup failed
        overall_result["overall_usage_metadata"] = None

    logger.info(f"Processor finished. Overall Status: {overall_result['status']}")
    return overall_result
