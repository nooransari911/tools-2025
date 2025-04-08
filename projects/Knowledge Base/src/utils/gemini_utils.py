import os, sys, json
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union, Type # Ensure Type is imported

from google.genai import types
from google import genai



SCHEMA_REGISTRY: Dict [str, Type[BaseModel]] = {}
SCHEMA_ENV_VAR = "STRUCTURED_OUTPUT_JSON_SCHEMA"
# DEFAULT_SCHEMA_NAME = "LabelledDataMapValidated"
DEFAULT_SCHEMA_NAME = "StructuredListOutput"
SELECTED_SCHEMA_CLASS: Optional [Type[BaseModel]] = None
SYS_INS = ""
OUTPUT_JSON_PATH = "OUTPUT_JSON_PATH"
MODEL_NAME = "GEMINI_20_FL"
PRO_MODEL_NAME = "GEMINI_20_PRO"
FLASH_MODEL_NAME = "GEMINI_20_FL"
API_KEY_PAID_STR = "API_KEY_PAID"
API_KEY_FREE_STR = "API_KEY_FREE"

def resolve_and_set_schema_class():
    """
    Reads the schema name from the environment variable, looks it up in the
    registry, and sets the global SELECTED_SCHEMA_CLASS. Falls back to default.
    """
    global SELECTED_SCHEMA_CLASS # To modify the global variable

    # Ensure registry and default name are available
    if not SCHEMA_REGISTRY or DEFAULT_SCHEMA_NAME not in SCHEMA_REGISTRY:
         log_msg = f"Error: Schema registry empty or default schema '{DEFAULT_SCHEMA_NAME}' not found."
         # Use logger if available, otherwise print and exit
         try:
             logger.error(log_msg)
         except NameError:
             print(log_msg, file=sys.stderr)
         sys.exit(1) # Cannot proceed without a default

    default_class = SCHEMA_REGISTRY[DEFAULT_SCHEMA_NAME]
    chosen_class = default_class # Start with default
    schema_source = f"default ('{DEFAULT_SCHEMA_NAME}')" # For logging

    # Get schema name from environment variable
    env_schema_name = os.getenv(SCHEMA_ENV_VAR)

    if env_schema_name and env_schema_name.strip():
        env_schema_name = env_schema_name.strip()

        # Look up the class in the registry
        found_class = SCHEMA_REGISTRY.get(env_schema_name)
        if found_class:
            chosen_class = found_class
            schema_source = f"environment variable ('{env_schema_name}')"
        else:
            pass
    else:
        pass
        # chosen_class remains default_class

    SELECTED_SCHEMA_CLASS = chosen_class
    return SELECTED_SCHEMA_CLASS.__name__

    # Optional: Check if the selected class is actually a BaseModel
    if not issubclass(SELECTED_SCHEMA_CLASS, BaseModel):
        log_msg = f"Error: Resolved schema '{SELECTED_SCHEMA_CLASS.__name__}' is not a Pydantic BaseModel."
        try: logger.error(log_msg)
        except NameError: print(log_msg, file=sys.stderr)
        sys.exit(1)


def register_schema(cls: Type[BaseModel]):
    """Decorator to automatically register a schema class using its own name as the key."""
    # Ensure the input is actually a class derived from BaseModel
    if not isinstance(cls, type) or not issubclass(cls, BaseModel):
        raise TypeError(f"Object passed to register_schema must be a Pydantic BaseModel subclass, not {type(cls)}")

    schema_name = cls.__name__
    # print (f"Registering {cls.__name__}")
    if schema_name in SCHEMA_REGISTRY:
        # Use logger if available, otherwise print warning
        log_msg = f"Warning: Schema name '{schema_name}' already registered. Overwriting."
        try:
            # Check if logger is defined and configured
            if 'logger' in globals() and isinstance(logger, logging.Logger):
                logger.warning(log_msg)
            else:
                print(log_msg)
        except NameError: # logger might not be defined globally yet
            print(log_msg)

    SCHEMA_REGISTRY[schema_name] = cls
    # Optional print for debugging registration:
    # print(f"DEBUG: Registered schema '{schema_name}' -> {cls}")
    return cls


# --- File I/O operations ---
def load_output_file_version_json ():
    global OUTPUT_JSON_PATH
    output_json_path = os.environ.get (OUTPUT_JSON_PATH)
    try:
        with open(output_json_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def save_output_file_version_json ():
    global OUTPUT_JSON_PATH
    output_json_path = os.environ.get (OUTPUT_JSON_PATH)
    old_data = load_output_file_version_json ()
    new_data = {}

    if not old_data:
        old_data = {
            "version": 0,
            "filename": "./output files/output response v0.json"
        }
    new_data ["version"]   = old_data ["version"]   +  1
    new_data ["filepath"]  = f"./output files/output response v{new_data ["version"]}.json"
    with open(output_json_path, 'w') as f:
        json.dump(
            obj=new_data, 
            fp=f, 
            indent=4
        )
    return new_data ["filepath"]

def reset_output_file_version ():
    global OUTPUT_JSON_PATH
    output_json_path = os.environ.get (OUTPUT_JSON_PATH)
    old_data = {
        "version": 0,
        "filename": "./output files/output response v0.json"
    }
    with open(output_json_path, 'w') as f:
        json.dump(old_data, f, indent=4)



def JSON_responses_parse_write (all_responses: List [str]):
    # --- Initialization ---
    parsed_objects_list = [] # To store successfully parsed Python objects
    other_items_list = []    # To store ALL other original items
    start_marker = "```json\n"
    end_marker = "\n```"

    print(f"Processing {len(all_responses)} input items...")

    # --- Main Processing Loop ---
    for i, original_item in enumerate(all_responses):
        was_parsed_successfully = False
        parsed_object = None
        processed_via_markers = False # Flag to indicate if marker logic was attempted

        try:
            # --- Check 1: Is it a usable string? ---
            if isinstance(original_item, str):
                stripped_item = original_item.strip()
                if stripped_item: # Proceed only if string is not empty after stripping

                    # --- Check 2: Attempt Marker-Based Parsing ---
                    start_index = original_item.find(start_marker)
                    if start_index != -1:
                        processed_via_markers = True # Marker logic path taken
                        json_start_pos = start_index + len(start_marker)
                        end_index = original_item.find(end_marker, json_start_pos)

                        if end_index != -1:
                            content_between_markers = original_item[json_start_pos:end_index].strip()
                            if content_between_markers:
                                try:
                                    parsed_object = json.loads(content_between_markers)
                                    was_parsed_successfully = True # SUCCESS via markers
                                    # print(f"Debug: Index {i}: Parsed successfully via markers.")
                                except json.JSONDecodeError as e:
                                    print(f"Info: Index {i}: Content between markers is invalid JSON ({e}).")
                                    # Keep was_parsed_successfully = False
                            else:
                                print(f"Info: Index {i}: Markers found, but content between them is empty.")
                                # Keep was_parsed_successfully = False
                        else:
                            print(f"Info: Index {i}: Start marker found, but no subsequent end marker.")
                            # Keep was_parsed_successfully = False

                    # --- Check 3: Attempt Raw Parsing (if not processed via markers) ---
                    # Only attempt raw parse if marker logic was NOT attempted (no start marker found)
                    if not processed_via_markers:
                        try:
                            parsed_object = json.loads(stripped_item)
                            was_parsed_successfully = True # SUCCESS via raw parse
                            # print(f"Debug: Index {i}: Parsed successfully via raw string.")
                        except json.JSONDecodeError:
                            # Failed raw parse, it's likely just text
                            # Optional: print(f"Info: Index {i}: Not raw JSON.")
                            pass # Keep was_parsed_successfully = False

            # --- If not a string or empty after strip, was_parsed_successfully remains False ---

        except Exception as e:
            # Catch any unexpected errors during the processing of THIS specific item
            print(f"Error: Index {i}: Unexpected error processing item: {e}")
            was_parsed_successfully = False # Ensure it goes to the 'other' list

        # --- Final Assignment: Preserve Everything ---
        if was_parsed_successfully:
            parsed_objects_list.append(parsed_object)
        else:
            # Add the ORIGINAL item to the 'other' list if it wasn't parsed
            # This includes non-strings, empty strings, parse failures, and errors
            other_items_list.append(original_item)


    print(f"\nProcessing complete.")
    print(f"- Parsed {len(parsed_objects_list)} items as JSON.")
    print(f"- Collected {len(other_items_list)} other items.")
    # Verification: The counts should sum to the original number of items
    total_processed = len(parsed_objects_list) + len(other_items_list)
    print(f"- Total items accounted for: {total_processed} (Original: {len(all_responses)})")
    if total_processed != len(all_responses):
        print("!!! WARNING: Item count mismatch. Not all items were preserved.")


    # --- Write Parsed JSON Output File ---
    if parsed_objects_list:
        json_output_file_path = save_output_file_version_json ()
        print(f"\nWriting {len(parsed_objects_list)} parsed JSON objects to: {json_output_file_path}")
        try:
            with open(file=json_output_file_path, mode="w", encoding='utf-8') as f:
                json.dump(obj=parsed_objects_list, fp=f, indent=4)
            print(f"Successfully wrote JSON data to {json_output_file_path}.")
        except IOError as e:
            print(f"Error: Could not write JSON file '{json_output_file_path}'. Error: {e}")
        except Exception as e:
            print(f"Error: An unexpected error occurred during JSON file writing: {e}")
    else:
        print("\nNo valid JSON objects were parsed. JSON output file will not be created.")

    # --- Write Other Items Output File ---
    if other_items_list:
        other_output_file_path = "./output files/non-json output response.json"
        print(f"\nWriting {len(other_items_list)} other items to: {other_output_file_path}")
        try:
            with open(file=other_output_file_path, mode="w", encoding='utf-8') as f:
                for item in other_items_list:
                    # Write the string representation of the item + newline
                    f.write(str(item) + '\n')
            print(f"Successfully wrote other items to {other_output_file_path}.")
        except IOError as e:
            print(f"Error: Could not write other items file '{other_output_file_path}'. Error: {e}")
        except Exception as e:
            print(f"Error: An unexpected error occurred during other items file writing: {e}")
    else:
        print("\nNo 'other' items were collected. Other items output file will not be created.")


# --- AI SDK Functions begin here ---
def load_system_instructions():
    global SYS_INS
    # Retrieve the file path from the environment variable
    instructions_file_path = os.getenv('SYSTEM_INSTRUCTIONS_STRUCTURED_PATH')

    if instructions_file_path:
        try:
            # Open and read the system instructions file
            with open(instructions_file_path, 'r') as file:
                SYS_INS = file.read()
            # print (SYS_INS)
            # print ("sys_ins L70: ", sys_ins, "\n")
        except Exception as e:
            print(f"Error reading system instructions file: {e}")
    else:
        print("Environment variable 'SYSTEM_INSTRUCTIONS_PATH' not set.")



def configure_genai():
    global SYS_INS, PRO_MODEL_NAME, FLASH_MODEL_NAME, API_KEY_PAID_STR, API_KEY_FREE_STR

    if len(sys.argv) < 3:
        raise ValueError("Model type (pro/flash) and API key type (free/paid) must be provided.")

    # SYS_INS = load_system_instructions ()
    # print (f"sys ins {SYS_INS}")
    model_type = sys.argv[1].lower()
    api_key_type = sys.argv[2].lower()

    if model_type == "pro":
        model_name = os.environ.get(PRO_MODEL_NAME)
    elif model_type == "flash":
        model_name = os.environ.get(FLASH_MODEL_NAME)
    else:
        raise ValueError("Invalid model_type. Must be 'pro' or 'flash'.")

    if api_key_type == "free":
        api_key = os.environ.get(API_KEY_FREE_STR)
        if not api_key:
             raise ValueError(f"The {API_KEY_FREE_STR} environment variable is not set.")
    elif api_key_type == "paid":
        api_key = os.environ.get(API_KEY_PAID_STR)
        if not api_key:
            raise ValueError(f"The {API_KEY_PAID_STR} environment variable is not set.")
    else:
        raise ValueError("Invalid api_key_type. Must be 'free' or 'paid'.")

    client = genai.Client(api_key=api_key)
    return client, model_name

