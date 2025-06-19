






import os
import sys
import json
import logging
import pathlib
from multiprocessing import Manager
from typing import Optional, List, Dict, Any, Union, Type, Tuple, TypeVar
from pydantic import BaseModel, ValidationError as PydanticValidationError, Field
from google.genai import types
from google import genai
import google.api_core.exceptions
from dotenv import load_dotenv
from src.utils.errors import JSONValidationError




# --- Configuration Constants ---
SCHEMA_ENV_VAR = "STRUCTURED_OUTPUT_JSON_SCHEMA"
DEFAULT_SCHEMA_NAME = "StructuredListOutput"
OUTPUT_JSON_PATH_ENV_VAR = "OUTPUT_JSON_PATH"
MODEL_NAME_PRO_ENV_VAR = "GEMINI_20_PRO"
MODEL_NAME_PRO_EXP_ENV_VAR = "GEMINI_20_PRO_EXP" # ** ADDED for free pro model **
MODEL_NAME_FLASH_ENV_VAR = "GEMINI_20_FL"
API_KEY_PAID_ENV_VAR = "API_KEY_PAID"
API_KEY_FREE_ENV_VAR = "API_KEY_FREE"
SYS_INS_PATH_ENV_VAR = "SYSTEM_INSTRUCTIONS_PATH"
SYS_INS_STRUCT_PATH_ENV_VAR = "SYSTEM_INSTRUCTIONS_STRUCTURED_PATH"
MAX_TIMEOUT = 600 * 1000
# --- Global State ---
SCHEMA_REGISTRY: Dict[str, Type[BaseModel]] = {}
SCHEMA_DEFINITIONS: Dict[str, Dict[str, Any]] = {} # Value is a schema dict


try:
    _manager = Manager()
    CLI_USAGE_METADATA_PROXY = _manager.list()
except Exception as e:
    print(f"Warning: Could not init Manager: {e}. CLI parallel usage broken.", file=sys.stderr)
    CLI_USAGE_METADATA_PROXY = None # type: ignore

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

# --- Helper Function ---
def format_number(num: Optional[int]) -> str:
    """Formats an integer with commas, handles None."""
    # (Implementation same as before)
    if num is None: return "N/A"
    try: return f"{int(num):,}"
    except (ValueError, TypeError): return str(num)


ModelType = TypeVar('ModelType', bound=BaseModel)





# --- Schema Registration ---


def register_schema(cls: Type[BaseModel]):
    """
    Decorator to register a Pydantic BaseModel schema and its JSON definition.
    """
    global SCHEMA_REGISTRY, SCHEMA_DEFINITIONS # Declare use of globals

    if not isinstance(cls, type) or not issubclass(cls, BaseModel):
        raise TypeError(f"Decorated class '{cls.__name__ if hasattr(cls, '__name__') else cls}' must be a Pydantic BaseModel subclass.")

    schema_name = cls.__name__

    if schema_name in SCHEMA_REGISTRY:
        logger.warning(f"Schema class '{schema_name}' is being overwritten in SCHEMA_REGISTRY.")
    if schema_name in SCHEMA_DEFINITIONS:
        logger.warning(f"Schema definition for '{schema_name}' is being overwritten in SCHEMA_DEFINITIONS.")

    SCHEMA_REGISTRY[schema_name] = cls

    # Generate and store the JSON schema definition (as a dict)
    try:
        if hasattr(cls, 'model_json_schema'): # Pydantic v2+
            schema_dict = cls.model_json_schema()
        elif hasattr(cls, 'schema'): # Pydantic v1
            schema_dict = cls.schema()
        else:
            logger.error(
                f"Could not generate JSON schema for '{schema_name}'. "
                "Class does not have 'model_json_schema()' or 'schema()' method."
            )
            # Optionally, you might want to remove it from SCHEMA_REGISTRY too or handle this error differently
            # For now, we'll just not add it to SCHEMA_DEFINITIONS
            return cls
        SCHEMA_DEFINITIONS[schema_name] = schema_dict
        logger.debug(f"Registered schema class '{schema_name}' and its JSON definition.")
    except Exception as e:
        logger.error(f"Error generating JSON schema for '{schema_name}': {e}")
        # Decide if you want to proceed without its definition or raise the error
        # If it's critical, you might: del SCHEMA_REGISTRY[schema_name]; raise

    return cls





def resolve_schema_class(schema_name_override: Optional[str] = None) -> Optional[Type[BaseModel]]:
    """
    Resolves schema class via param, env var, or default.
    Returns None if the schema is not found, not a Pydantic BaseModel,
    or if the default schema is targeted but unavailable/invalid.
    """
    if not SCHEMA_REGISTRY:
        logger.warning("No schemas registered. Cannot resolve any schema.")
        return None

    # Determine the target schema name and source
    target_name: str
    source: str
    is_default_target = False # Flag to know if we are trying to resolve the default schema

    if schema_name_override:
        target_name = schema_name_override.strip()
        source = "param"
    elif os.getenv(SCHEMA_ENV_VAR):
        env_schema_name = os.getenv(SCHEMA_ENV_VAR)
        if not env_schema_name or not env_schema_name.strip():
            logger.warning(f"Environment variable '{SCHEMA_ENV_VAR}' is set but empty. Falling back to default schema.")
            target_name = DEFAULT_SCHEMA_NAME
            source = "default_after_empty_env"
            is_default_target = True
        else:
            target_name = env_schema_name.strip()
            source = "env"
    else:
        # Fallback to default schema name
        target_name = DEFAULT_SCHEMA_NAME
        source = "default"
        is_default_target = True

    # Try to get the chosen class from the registry
    chosen_class = SCHEMA_REGISTRY.get(target_name)

    if chosen_class:
        if not issubclass(chosen_class, BaseModel):
            logger.error(
                f"Resolved schema '{target_name}' (source: {source}) is not a Pydantic BaseModel subclass. "
                "Cannot use this schema."
            )
            # If the problematic schema is the default one, this is more critical.
            if is_default_target:
                logger.error(
                    f"The default schema '{DEFAULT_SCHEMA_NAME}' is invalid (not a BaseModel). "
                    "JSON output requiring a default schema might fail."
                )
            return None # Do not use an invalid schema
        logger.info(f"Resolved schema '{target_name}' using {source}.")
        return chosen_class
    else:
        # Schema not found in registry
        logger.warning(f"Schema '{target_name}' (source: {source}) not found in SCHEMA_REGISTRY.")
        # If the default schema was targeted and not found, it's a notable warning.
        if is_default_target: # This implies target_name == DEFAULT_SCHEMA_NAME
             logger.warning(
                f"Default schema '{DEFAULT_SCHEMA_NAME}' is not registered. "
                "Operations relying on it may not function as expected or "
                "structured output will be model-inferred if no other schema is specified."
            )
        return None # Simply return None if any schema (including default if it was the target) is not found.


# --- New print_all_schemas function ---
def print_all_schemas():
    """
    Prints all registered schema definitions (from SCHEMA_DEFINITIONS) as a single JSON object.
    """
    global SCHEMA_DEFINITIONS # Access the global dictionary

    if not SCHEMA_DEFINITIONS:
        print("No schema definitions are currently registered or generated.")
        return

    try:
        # SCHEMA_DEFINITIONS already contains dictionaries, so json.dumps will format them correctly
        schemas_json_str = json.dumps(SCHEMA_DEFINITIONS, indent=4)
        print(schemas_json_str)
    except TypeError as e:
        # This might happen if a schema definition itself contains non-serializable types,
        # though less likely if generated by Pydantic's methods.
        logger.error(f"Error serializing schema definitions to JSON: {e}")
        print(f"Error: Could not serialize schema definitions. Details: {e}")
        # For debugging, you could print the problematic dictionary:
        # import pprint


def print_schema_summary():
    """
    Prints a summary of all registered schemas: their names and descriptions.
    """
    global SCHEMA_REGISTRY # We need the model classes for docstrings and schema attributes

    if not SCHEMA_REGISTRY:
        print("No schemas are currently registered.")
        return

    print("Available Schemas:\n" + ("-" * 20))

    for name, model_class in sorted(SCHEMA_REGISTRY.items()): # Sort for consistent output
        title = name # Default title is the class name
        description = "No description available." # Default description

        # Attempt to get title and description from the Pydantic model's schema definition
        # This requires generating the schema on-the-fly if not already stored,
        # or accessing it from SCHEMA_DEFINITIONS if populated.
        # For simplicity here, let's try to generate it if needed or fetch from SCHEMA_DEFINITIONS.

        schema_def = SCHEMA_DEFINITIONS.get(name) # Check if pre-generated
        if not schema_def and hasattr(model_class, 'model_json_schema'): # Pydantic V2
            try:
                schema_def = model_class.model_json_schema()
            except Exception as e:
                logger.warning(f"Could not generate schema for {name} to get summary: {e}")
        elif not schema_def and hasattr(model_class, 'schema'): # Pydantic V1
             try:
                schema_def = model_class.schema()
             except Exception as e:
                logger.warning(f"Could not generate schema for {name} to get summary: {e}")


        if schema_def:
            title_from_schema = schema_def.get('title', name) # Use schema 'title' if present
            description_from_schema = schema_def.get('description')

            if title_from_schema and title_from_schema != name: # Only use if different and not empty
                title = title_from_schema
            if description_from_schema:
                description = description_from_schema.split('\n')[0] # First line of schema description
        
        # Fallback or supplement with class docstring if schema description is missing/generic
        if (not description_from_schema or description == "No description available.") and model_class.__doc__:
            class_docstring = model_class.__doc__.strip()
            first_line_of_docstring = class_docstring.split('\n')[0]
            if first_line_of_docstring: # Check if not empty after stripping
                description = first_line_of_docstring


        print(f"  {title}:") # Use the potentially overridden title
        print(f"    Name: {name}") # Always show the actual class name / registry key
        print(f"    Description: {description}")
        print("-" * 20)




# --- System Instructions ---
def load_system_instructions(is_structured_mode: bool) -> str:
    """Loads system instructions from file path in env vars."""
    # (Implementation same as before)
    env_var = SYS_INS_STRUCT_PATH_ENV_VAR if is_structured_mode else SYS_INS_PATH_ENV_VAR
    path_str = os.getenv(env_var)
    sys_ins = ""
    if path_str:
        try:
            path = pathlib.Path(path_str).resolve()
            if path.is_file():
                with open(path, 'r', encoding='utf-8') as f: sys_ins = f.read()
                logger.info(f"Loaded sys instructions: {path} (Structured: {is_structured_mode})")
            else: logger.warning(f"Sys instructions file not found: {path} (from {env_var})")
        except Exception as e: logger.error(f"Err reading sys ins file '{path_str}': {e}", exc_info=True)
    else: logger.warning(f"Env var '{env_var}' not set for sys instructions.")
    return sys_ins

# --- Gemini Client Configuration ---
def configure_gemini(
    model_type: str,
    api_key_type: str
) -> Tuple[genai.client.Client, str]:
    """Configures Gemini client and model name based on params and env vars. **Handles free/pro model name.**"""
    model_type_lc = model_type.lower()
    api_key_type_lc = api_key_type.lower()
    model_name = ""
    api_key = ""

    # Determine Model Name
    if model_type_lc == "pro":
        # ** CORRECTED LOGIC for free/pro model **
        if api_key_type_lc == "free":
            model_name = os.getenv(MODEL_NAME_PRO_EXP_ENV_VAR) # Use EXP model for free pro
            if not model_name: raise ValueError(f"Env var '{MODEL_NAME_PRO_EXP_ENV_VAR}' for free Pro model not set.")
            logger.info(f"Using Pro model (Free Tier Experimental): {model_name}")
        else: # Paid tier pro
            model_name = os.getenv(MODEL_NAME_PRO_ENV_VAR)
            if not model_name: raise ValueError(f"Env var '{MODEL_NAME_PRO_ENV_VAR}' for paid Pro model not set.")
            logger.info(f"Using Pro model (Paid Tier): {model_name}")
    elif model_type_lc == "flash":
        model_name = os.getenv(MODEL_NAME_FLASH_ENV_VAR)
        if not model_name: raise ValueError(f"Env var '{MODEL_NAME_FLASH_ENV_VAR}' for Flash model not set.")
        logger.info(f"Using Flash model: {model_name}")
    else:
        raise ValueError(f"Invalid model_type '{model_type}'. Must be 'pro' or 'flash'.")

    # Determine API Key
    if api_key_type_lc == "free":
        api_key = os.getenv(API_KEY_FREE_ENV_VAR)
        if not api_key: raise ValueError(f"Env var '{API_KEY_FREE_ENV_VAR}' not set.")
        logger.info("Using FREE tier API key.")
    elif api_key_type_lc == "paid":
        api_key = os.getenv(API_KEY_PAID_ENV_VAR)
        if not api_key: raise ValueError(f"Env var '{API_KEY_PAID_ENV_VAR}' not set.")
        logger.info("Using PAID tier API key.")
    else:
        raise ValueError(f"Invalid api_key_type '{api_key_type}'. Must be 'free' or 'paid'.")

    # Configure Client
    try:
        client = genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=MAX_TIMEOUT))
        logger.info(f"Gemini client configured successfully.")
        return client, model_name
    except Exception as e:
        logger.critical(f"Failed to initialize Gemini client: {e}", exc_info=True)
        raise ValueError(f"Failed to initialize Gemini client: {e}")


# --- Core Gemini Content Generation ---
def generate_gemini_content(
    genai_client: genai.client.Client,
    model_name: str,
    contents: List[Union[str, types.Part]],
    generation_config: types.GenerateContentConfig,
    is_structured_mode: bool
) -> types.GenerateContentResponse:
    """Generates content using the Gemini API asynchronously."""
    # (Implementation same as before)
    logger.info(f"Sending request to Gemini model '{model_name}' (Structured: {is_structured_mode})...")
    try:
        response = genai_client.models.generate_content (
            model=model_name, contents=contents, config=generation_config,
        )
        logger.info("Received response from Gemini.")
        if response.usage_metadata:
             logger.info(f"Tokens - Prompt: {format_number(response.usage_metadata.prompt_token_count)}, "
                         f"Candidates: {format_number(response.usage_metadata.candidates_token_count)}, "
                         f"Total: {format_number(response.usage_metadata.total_token_count)}")
        return response
    except google.api_core.exceptions.GoogleAPIError as e:
        logger.error(f"Gemini API Error: {e}", exc_info=False); raise # Re-raise specific error

    except genai.errors.ClientError as e:
        # err_str  = json.dumps (e, indent=4)
        err_mess = json.dumps (e.details, indent=4)
        err_code = e.code

        # print (f"complete error: {err_str}\n\n\n\n")
        # print (f"code: {err_code}\n\nerror message: {err_mess}\n\n\n\n")
        print (f"code: {err_code}\n\n")

        print("--- Quota Violation Details ---")
        found_and_displayed_quota_info = False

        if isinstance(e.details, dict) and \
           'error' in e.details and \
           isinstance(e.details.get('error'), dict) and \
           'details' in e.details['error'] and \
           isinstance(e.details['error'].get('details'), list):
        
            error_details_list = e.details['error']['details']
        
            for detail_item in error_details_list:
                if isinstance(detail_item, dict) and \
                   detail_item.get('@type') == 'type.googleapis.com/google.rpc.QuotaFailure':
                
                    violations = detail_item.get('violations')
                    if isinstance(violations, list) and violations:
                        print("Quota(s) Exceeded (from QuotaFailure):")
                        for violation in violations:
                            if isinstance(violation, dict):
                                found_and_displayed_quota_info = True # Mark that we found and are displaying info
                                print(f"  - Quota Metric: {violation.get('quotaMetric', 'N/A')}")
                                print(f"    Quota ID: {violation.get('quotaId', 'N/A')}")
                            
                                dimensions = violation.get('quotaDimensions')
                                if isinstance(dimensions, dict) and dimensions:
                                    print(f"    Dimensions:")
                                    for dim_key, dim_value in dimensions.items():
                                        print(f"      {dim_key.capitalize()}: {dim_value}")
                                elif dimensions is not None: # It exists but isn't a dict or is empty
                                    print(f"    Dimensions: {dimensions} (Note: not a populated dictionary)")
                                else: # dimensions key is not present or is None
                                    print(f"    Dimensions: Not specified")
                                print("    --------------------") # Separator for each violation
                        print("-" * 30) # Separator for the end of a QuotaFailure block processing
                    elif violations is None:
                        print("QuotaFailure detail found, but no 'violations' key present.")
                    elif not isinstance(violations, list):
                        print(f"QuotaFailure detail found, but 'violations' is not a list (type: {type(violations)}).")
                    else: # violations is an empty list
                        print("QuotaFailure detail found, but the 'violations' list is empty.")
    
        if not found_and_displayed_quota_info:
            print("No specific quota violation details were found or 'e.details' was not in the expected format to extract them.")
            # For debugging, you might want to see the structure if it failed:
            # print("\nDebug information: Structure of e.details:")
            # if isinstance(e.details, (dict, list)):
            #     try:
            #         print(json.dumps(e.details, indent=2))
            #     except Exception as dump_error:
            #         print(f"Could not dump e.details as JSON: {dump_error}")
            #         print(f"Raw e.details: {e.details}")
            # elif e.details is not None:
            #     print(str(e.details))
            # else:
            #     print("e.details is None.")



    except Exception as e:
        logger.error(f"Unexpected Gemini generation error: {e}", exc_info=True); raise



def validate_json_string_against_model(
    json_string: str,
    model_class: Type[ModelType]
) -> ModelType:
    """
    Validates a JSON string against a given Pydantic BaseModel class.

    Args:
        json_string: The JSON string to validate.
        model_class: The Pydantic BaseModel class to validate against.

    Returns:
        An instance of the model_class populated with data from json_string.

    Raises:
        JSONValidationError: If the json_string is not valid JSON,
                             or if it does not conform to the model_class schema.
    """
    try:
        # Pydantic v2+ uses model_validate_json
        # For Pydantic v1, you would use: model_class.parse_raw(json_string)
        validated_model_instance = model_class.model_validate_json(json_string)
        return validated_model_instance
    except PydanticValidationError as e:
        # Catch Pydantic's specific validation error
        error_message = (
            f"JSON data failed validation against model '{model_class.__name__}'."
        )
        # Raise our custom exception, chaining the original Pydantic error
        raise JSONValidationError(error_message, pydantic_error=e) from e
    except json.JSONDecodeError as e:
        # This case is often caught by Pydantic's model_validate_json as well,
        # resulting in a PydanticValidationError. However, explicitly catching it
        # can be useful if pre-processing the string before Pydantic sees it,
        # or for extremely malformed JSON that Pydantic might not parse cleanly.
        # Pydantic's ValidationError for invalid JSON usually has type 'json_invalid'.
        error_message = f"Invalid JSON format: {e.msg}"
        # We don't have a pydantic_error here, but we could create a mock one or pass None
        # For simplicity, let's just pass the message.
        # To be more consistent, one could construct a minimal PydanticValidationError-like structure
        # if needed by the consumer of JSONValidationError.
        raise JSONValidationError(error_message) from e
    except Exception as e:
        # Catch any other unexpected errors during the process
        error_message = f"An unexpected error occurred during JSON validation: {str(e)}"
        raise JSONValidationError(error_message) from e








# --- Output File Handling (for CLI) ---
def load_json_file(file_path: Union[str, pathlib.Path]) -> Optional[Dict]:
    """Loads JSON data from a file."""
    # (Implementation same as before)
    path = pathlib.Path(file_path)
    if not path.is_file(): return None
    try:
        with open(path, 'r', encoding='utf-8') as f: return json.load(f)
    except Exception: return None

def save_json_file(data: Any, file_path: Union[str, pathlib.Path], indent: int = 4) -> bool:
    """Saves data as JSON to a file, creating directories."""
    # (Implementation same as before)
    path = pathlib.Path(file_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f: json.dump(data, f, indent=indent)
        logger.info(f"Saved JSON data to {path}")
        return True
    except Exception as e: logger.error(f"Write JSON failed {path}: {e}", exc_info=True); return False

def get_next_output_version(output_config_path: Union[str, pathlib.Path]) -> Tuple[int, pathlib.Path]:
    """Reads/updates version config file and returns new version/path."""
    # (Implementation same as before)
    config_path = pathlib.Path(output_config_path)
    default_pattern = "./output files/output_v{version}" # Relative to CWD
    data = load_json_file(config_path)
    current_version = data.get("version", -1) if isinstance(data, dict) else -1
    pattern = data.get("base_filepath_pattern", default_pattern) if isinstance(data, dict) else default_pattern
    if current_version == -1: logger.warning(f"Output config invalid/missing: {config_path}. Using defaults.")
    new_version = current_version + 1
    new_base_filepath = pathlib.Path(pattern.format(version=new_version))
    if not save_json_file({"version": new_version, "base_filepath_pattern": pattern}, config_path):
         logger.error("Failed to save updated output version config!")
    return new_version, new_base_filepath

# --- Response Parsing and Writing (Refactored for single or multiple responses) ---
def parse_json_from_response_text(response_text: str) -> Optional[Any]:
    """Attempts to parse JSON from a string, handling markdown code blocks."""
    # (Implementation same as before)
    if not isinstance(response_text, str): return None
    stripped = response_text.strip()
    if not stripped: return None
    start, end = "```json\n", "\n```"
    if stripped.startswith(start) and stripped.endswith(end):
        json_str = stripped[len(start):-len(end)].strip()
        if not json_str: return None
        try: return json.loads(json_str)
        except json.JSONDecodeError: return None # Fall through to parse whole string
    try: return json.loads(stripped)
    except json.JSONDecodeError: return None



def write_output_files(
    responses: List[str],
    output_config_path: str,
    is_structured_mode: bool
) -> None:
    """
    Parses responses and writes them to versioned output files.
    If structured_mode is True, attempts to parse responses as JSON.
    Successfully parsed JSON objects are aggregated:
    - Single-element lists are unwrapped.
    - All processed objects are collected into a list for the JSON file.
    If JSON parsing/aggregation is successful, writes to a .json file.
    Responses that are not parsed as JSON, or if JSON writing fails,
    are written to a .md file.
    """
    try:
        _ver, base_path = get_next_output_version(output_config_path)
        json_path = base_path.with_suffix(".json")
        other_path = base_path.with_suffix(".md")
        
        # Ensure the parent directory for outputs exists
        # This might be redundant if get_next_output_version or save_json_file already do this
        base_path.parent.mkdir(parents=True, exist_ok=True)

        original_parsed_json_objects: List[Any] = []
        other_content_items: List[str] = []

        for resp_text in responses:
            parsed_obj = None
            if is_structured_mode:
                try:
                    # parse_json_from_response_text should return None if resp_text is not valid JSON
                    parsed_obj = parse_json_from_response_text(resp_text)
                except Exception as e:
                    logger.error(f"Error during call to parse_json_from_response_text: {e}", exc_info=True)
                    # Treat as unparsable, parsed_obj remains None
            
            if parsed_obj is not None:
                original_parsed_json_objects.append(parsed_obj)
            else:
                # This includes:
                # 1. Not in structured mode.
                # 2. In structured mode, but resp_text was not valid JSON (parse_json_from_response_text returned None).
                # 3. In structured mode, but parse_json_from_response_text raised an error.
                other_content_items.append(resp_text)

        if original_parsed_json_objects:
            # Aggregate the parsed JSON objects according to the specified rules
            aggregated_json_payload: List[Any] = []
            for item in original_parsed_json_objects:
                if isinstance(item, list) and len(item) == 1:
                    aggregated_json_payload.append(item[0])  # Unwrap single-element lists
                else:
                    aggregated_json_payload.append(item)
            
            if save_json_file(aggregated_json_payload, json_path):
                logger.info(f"Aggregated JSON data successfully written to {json_path}")
            else:
                logger.error(f"Failed to write aggregated JSON data to {json_path}.")
                # Add original parsed JSON objects (before aggregation) to other_content_items
                # so they are included in the .md file.
                failed_json_strings = [
                    f"--- FAILED JSON WRITE (original parsed object shown below) ---\n{str(obj)[:1000]}\n--- END ---"
                    for obj in original_parsed_json_objects
                ]
                other_content_items.extend(failed_json_strings)
        
        elif is_structured_mode: # No JSON objects were parsed, but we were in structured mode.
            logger.warning("Structured mode was enabled, but no JSON content was successfully parsed from responses.")

        if other_content_items:
            try:
                # Ensure parent directory exists (might be redundant if done earlier, but safe)
                other_path.parent.mkdir(parents=True, exist_ok=True)
                with open(other_path, 'w', encoding='utf-8') as f:
                    for i, item_text in enumerate(other_content_items):
                        f.write(str(item_text))
                        # Add separator between items, and ensure last item ends with a newline
                        if len(other_content_items) > 1 and i < len(other_content_items) - 1:
                            f.write(f"\n\n{'='*20} Response Separator {'='*20}\n\n")
                        elif not str(item_text).endswith('\n'):
                            f.write('\n')
                logger.info(f"Wrote {len(other_content_items)} non-JSON/raw items to {other_path}")
            except Exception as e:
                logger.error(f"Failed to write to non-JSON/raw output file {other_path}: {e}", exc_info=True)
                
    except Exception as e:
        # Catch-all for errors in the output writing process itself (e.g., path issues, permissions)
        logger.error(f"An unexpected error occurred in write_output_files: {e}", exc_info=True)




def write_output_files_obs(
    responses: List[str],
    output_config_path: str,
    is_structured_mode: bool
) -> None:
    """Parses responses and writes them to versioned output files (.json, .md)."""
    # (Implementation same as before)
    try:
        _ver, base_path = get_next_output_version(output_config_path)
        json_path, other_path = base_path.with_suffix(".json"), base_path.with_suffix(".md")
        json_objs, others = [], []
        for resp in responses:
            parsed = parse_json_from_response_text(resp) if is_structured_mode else None
            if parsed is not None: json_objs.append(parsed)
            else: others.append(resp)
        if json_objs:
            if not save_json_file(json_objs, json_path):
                 logger.error(f"JSON write failed: {json_path}")
                 others.extend([f"--- FAILED JSON OBJ ---\n{str(o)[:1000]}\n--- END ---" for o in json_objs])
        elif is_structured_mode: logger.warning("Structured mode, but no JSON parsed.")
        if others:
            try:
                other_path.parent.mkdir(parents=True, exist_ok=True)
                with open(other_path, 'w', encoding='utf-8') as f:
                    for i, item in enumerate(others):
                        f.write(str(item))
                        if len(others) > 1 and i < len(others) - 1: f.write(f"\n\n{'='*20} Response Separator {'='*20}\n\n")
                        elif not str(item).endswith('\n'): f.write('\n')
                logger.info(f"Wrote {len(others)} non-JSON/raw items to {other_path}")
            except Exception as e: logger.error(f"Write TXT failed {other_path}: {e}", exc_info=True)
    except Exception as e: logger.error(f"Output file writing error: {e}", exc_info=True)

# --- Token Usage Update (for CLI) ---
def update_gemini_token_usage(
    usage_metadata_list: List[types.GenerateContentResponseUsageMetadata],
    usage_file_path: Union[str, pathlib.Path]
) -> None:
    """Updates the total API token usage stored in a JSON file."""
    # (Implementation same as before)
    if not usage_metadata_list: return
    path = pathlib.Path(usage_file_path)
    logger.info(f"Updating token usage: {path}")
    current = load_json_file(path) or {"input_tokens": 0, "output_tokens": 0}
    if not isinstance(current.get("input_tokens"), int): current["input_tokens"] = 0
    if not isinstance(current.get("output_tokens"), int): current["output_tokens"] = 0
    new_in = sum(md.prompt_token_count for md in usage_metadata_list if md and md.prompt_token_count is not None)
    new_out = sum(md.candidates_token_count for md in usage_metadata_list if md and md.candidates_token_count is not None)
    updated = {"input_tokens": current["input_tokens"] + new_in, "output_tokens": current["output_tokens"] + new_out}
    logger.info(f"Usage: Current={format_number(current['input_tokens'])}/{format_number(current['output_tokens'])} + New={format_number(new_in)}/{format_number(new_out)} -> Total={format_number(updated['input_tokens'])}/{format_number(updated['output_tokens'])}")
    if not save_json_file(updated, path): logger.error(f"Failed to save token usage: {path}")


# --- Import local schemas to register them ---
# ** CORRECTED IMPORT ** Assuming this utils.py is in src/utils/
# and schema files are in src/data/. We import relative to src/.
try:
    # This works if the script running the import can find the 'src' package
    # (e.g., running from project root, or sys.path includes project root)
    from data import generic_JSON_response_schema
    from data import PDF_page_JSON_schema
    from data import files_response_schema
    from data import files_schema
    from data import front_matter_schema

    logger.info("Schema definition modules imported successfully for registration.")
except ImportError as e:
    logger.error(f"Could not import schema modules from 'data': {e}. Schemas may not be registered.")
    # Attempt relative import as fallback (might work depending on execution context)
    try:
        from ..data import generic_JSON_response_schema # noqa
        from ..data import PDF_page_JSON_schema # noqa
        from ..data import files_response_schema
        from data import files_schema
        logger.info("Schema definition modules imported successfully using relative path.")
    except ImportError:
        logger.error(f"Relative import of schema modules also failed. Check structure and sys.path.")
