# your_original_project/src/utils/gemini_utils.py

import os
import sys
import json
import logging
import pathlib
from multiprocessing import Manager
from typing import Optional, List, Dict, Any, Union, Type, Tuple

# Third-party imports
from pydantic import BaseModel, Field
from google.genai import types
from google import genai
import google.api_core.exceptions
from dotenv import load_dotenv

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

# --- Global State ---
SCHEMA_REGISTRY: Dict[str, Type[BaseModel]] = {}
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

# --- Schema Registration ---
def register_schema(cls: Type[BaseModel]):
    """Decorator to register a Pydantic BaseModel schema."""
    # (Implementation same as before)
    if not isinstance(cls, type) or not issubclass(cls, BaseModel): raise TypeError("Must be BaseModel subclass")
    schema_name = cls.__name__
    if schema_name in SCHEMA_REGISTRY: logger.warning(f"Schema '{schema_name}' overwritten.")
    SCHEMA_REGISTRY[schema_name] = cls
    logger.debug(f"Registered schema '{schema_name}'")
    return cls

def resolve_schema_class(schema_name_override: Optional[str] = None) -> Optional[Type[BaseModel]]:
    """Resolves schema class via param, env var, or default."""
    # (Implementation same as before)
    if not SCHEMA_REGISTRY or DEFAULT_SCHEMA_NAME not in SCHEMA_REGISTRY:
         logger.critical(f"Default schema '{DEFAULT_SCHEMA_NAME}' not in registry."); sys.exit(1)
    default_class = SCHEMA_REGISTRY[DEFAULT_SCHEMA_NAME]
    target_name = schema_name_override or os.getenv(SCHEMA_ENV_VAR) or DEFAULT_SCHEMA_NAME
    source = "param" if schema_name_override else "env" if os.getenv(SCHEMA_ENV_VAR) else "default"
    chosen_class = SCHEMA_REGISTRY.get(target_name.strip())
    if chosen_class:
        logger.info(f"Resolved schema '{target_name}' using {source}.")
        if not issubclass(chosen_class, BaseModel):
             logger.error(f"Resolved '{target_name}' not a BaseModel. Using default.")
             return default_class
        return chosen_class
    else:
        logger.warning(f"Schema '{target_name}' ({source}) not found. Using default '{DEFAULT_SCHEMA_NAME}'.")
        return default_class


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
        client = genai.Client(api_key=api_key)
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
    except Exception as e:
        logger.error(f"Unexpected Gemini generation error: {e}", exc_info=True); raise

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

    logger.info("Schema definition modules imported successfully for registration.")
except ImportError as e:
    logger.error(f"Could not import schema modules from 'data': {e}. Schemas may not be registered.")
    # Attempt relative import as fallback (might work depending on execution context)
    try:
        from ..data import generic_JSON_response_schema # noqa
        from ..data import PDF_page_JSON_schema # noqa
        from ..data import files_response_schema
        logger.info("Schema definition modules imported successfully using relative path.")
    except ImportError:
        logger.error(f"Relative import of schema modules also failed. Check structure and sys.path.")
