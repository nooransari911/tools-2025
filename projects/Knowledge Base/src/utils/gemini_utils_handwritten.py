import os, sys, json
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union, Type # Ensure Type is imported

from google.genai import types
from google import genai

from multiprocessing import Manager



SCHEMA_REGISTRY: Dict [str, Type[BaseModel]] = {}
SCHEMA_ENV_VAR = "STRUCTURED_OUTPUT_JSON_SCHEMA"
# DEFAULT_SCHEMA_NAME = "LabelledDataMapValidated"
DEFAULT_SCHEMA_NAME = "StructuredListOutput"
SELECTED_SCHEMA_CLASS: Optional [Type[BaseModel]] = None
SYS_INS = ""
OUTPUT_JSON_PATH = "OUTPUT_JSON_PATH"
MODEL_NAME = "GEMINI_20_FL"
PRO_MODEL_NAME = "GEMINI_20_PRO"
PRO_MODEL_NAME_EXP = "GEMINI_20_PRO_EXP"
FLASH_MODEL_NAME = "GEMINI_20_FL"
API_KEY_PAID_STR = "API_KEY_PAID"
API_KEY_FREE_STR = "API_KEY_FREE"
IS_STRUCTURED_OP_MODE = False
manager = Manager ()
USAGE_METADATA = manager.list ()



# --- Helper Function for Formatting ---
def format_number(num: int) -> str:
    """Formats an integer with commas as thousands separators."""
    if num is None:
        return "N/A"
    try:
        return f"{int(num):,}"
    except (ValueError, TypeError):
        return str(num) # Fallback if not an integer


# --- Setting schema class for structured output mode ---
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
    pass
    base_filename = save_output_file_version ()
    json_filename = f"{base_filename}.json"
    return json_filename

def save_output_file_version ():
    global OUTPUT_JSON_PATH
    output_json_path = os.environ.get (OUTPUT_JSON_PATH)
    old_data = load_output_file_version_json ()
    new_data = {}

    if not old_data:
        old_data = {
            "version": 0,
            "filename": "./output files/output response v0"
        }
    new_data ["version"]   = old_data ["version"]   +  1
    new_data ["filepath"]  = f"./output files/output response v{new_data ["version"]}"
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
        "filename": "./output files/output response v0"
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




def normal_response_write(file_path: str, content: List[str]) -> bool:
    """
    Writes a list of strings to a specified file, one string per line.

    If the file extension is not '.md', it attempts to strip leading/trailing
    Markdown code block delimiters (```) from the content list.

    Handles directory creation if it doesn't exist and manages file
    operations safely using a context manager.

    Args:
        file_path: The full path to the target file (including extension).
        content: A list of strings to write to the file.

    Returns:
        True if the file was written successfully, False otherwise.
    """
    if not isinstance(content, list):
        print(f"Error: Content must be a list of strings. Got: {type(content)}", file=sys.stderr)
        return False
    # Optional stricter check:
    # if not all(isinstance(item, str) for item in content):
    #     print(f"Error: All items in the content list must be strings.", file=sys.stderr)
    #     return False

    # Make a copy if you need to preserve the original list outside the function
    # content_to_write = list(content) # Use content_to_write below instead of content
    # Or modify content directly if that's acceptable

    try:
        # --- SNIPPET START: Check extension and strip delimiters ---
        _, file_extension = os.path.splitext(file_path)

        if file_extension.lower() != '.md':

            # 3. Check if there are enough lines to potentially strip (at least 2)
            #    AND check if the first/last lines actually look like delimiters
            if len(content) >= 2 and \
               content[0].strip().startswith('```') and \
               content[-1].strip() == '```':

                # --- THIS IS THE ACTUAL STRIPPING STEP ---
                # Re-assign 'content' to the slice excluding the first and last lines.
                # This modifies which list the 'content' variable points to *within this function*.
                content = content[1:-1]
                # print(f"Debug: Stripped delimiters for {os.path.basename(file_path)}") # Optional debug prin
        # --- SNIPPET END ---

        # --- Safely handle the path ---
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        # --- Safely handle file writing ---
        with open(file_path, 'w', encoding='utf-8') as f:
            # --- Write the potentially modified content ---
            # Handle the edge case where stripping delimiters made the list empty
            if not content:
                 # Optionally write nothing, or maybe a placeholder?
                 # f.write("# Content stripped\n") # Example placeholder
                 pass # Writes an empty file in this case
            else:
                for line in content:
                    f.write(str(line) + '\n')

        return True

    except (IOError, OSError, TypeError, ValueError) as e:
        print(f"Error writing to file '{file_path}': {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"An unexpected error occurred while writing to '{file_path}': {e}", file=sys.stderr)
        return False



def write_response_to_file (response_list: list):
    catch_all_file_path = f"{save_output_file_version ()}.md"


    if (len (sys.argv) >= 5) and (sys.argv [4] == "struct"):
        JSON_responses_parse_write (response_list)

    elif (len (sys.argv) >= 5):
        normal_response_write (sys.argv [4], response_list)

    else:
        print (f"written to {catch_all_file_path}")
        normal_response_write (catch_all_file_path, response_list)



# --- AI SDK Functions begin here ---
def load_prompt_string () -> str:
    prompt_file_path = sys.argv [3]

    # Validate prompt file
    if not os.path.isfile(prompt_file_path):
        print(f"No such file as {prompt_file_path}\n\n")
        sys.exit(1)

    # Load prompt file
    with open(prompt_file_path, "r") as prompt_file:
        prompt_file_string = prompt_file.read()
        prompt = prompt_file_string

    return prompt




def load_system_instructions():
    global SYS_INS, IS_STRUCTURED_OP_MODE
    # Retrieve the file path from the environment variable
    if IS_STRUCTURED_OP_MODE:
        instructions_file_path = os.getenv ('SYSTEM_INSTRUCTIONS_STRUCTURED_PATH')
    else:
        instructions_file_path = os.getenv ('SYSTEM_INSTRUCTIONS_PATH')

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
        if model_type == "pro":
            model_name = os.environ.get(PRO_MODEL_NAME_EXP)
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




# --- The Core Function ---

def update_gemini_token_usage(usage_metadata_list: list[Any]) -> None:
    """
    Updates the total API token usage stored in a JSON file with human-readable output.

    Reads the current usage from a JSON file (determined by sys.argv[2]),
    calculates the new tokens used from the input list, adds them to the
    totals, and writes the updated totals back to the file. Prints usage
    numbers with thousands separators.

    Args:
        usage_metadata_list: A list of objects, where each object is expected
                             to have 'prompt_token_count' (input) and
                             'candidates_token_count' (output) attributes.
                             Typically GenerateContentResponseUsageMetadata objects.
    """
    # --- 1. Determine the target JSON file ---
    # Default filename
    filename = "./data/gemini_tokens_usage.json"
    usage_type = "Standard"

    # Check sys.argv for the 'free' argument
    # Ensure there are enough arguments before accessing sys.argv[2]
    if len(sys.argv) > 2 and sys.argv[2].lower() == "free":
        filename = "./data/gemini_tokens_usage_free.json"
        usage_type = "Free Tier"

    # print(f"--- Updating {usage_type} Usage ({filename}) ---")

    # --- 2. Read current usage from the file ---
    current_usage: Dict[str, int] = {"input_tokens": 0, "output_tokens": 0}
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                try:
                    content = f.read()
                    if content: # Check if file is not empty
                        current_usage = json.loads(content)
                        # Ensure keys exist, default to 0 if missing
                        if "input_tokens" not in current_usage:
                            current_usage["input_tokens"] = 0
                        if "output_tokens" not in current_usage:
                             current_usage["output_tokens"] = 0
                    else:
                        print(f"Warning: File '{filename}' was empty. Initializing usage.")
                except json.JSONDecodeError:
                    print(f"Error: Could not decode JSON from '{filename}'. Initializing usage.")
                    current_usage = {"input_tokens": 0, "output_tokens": 0} # Reset
        else:
             print(f"File '{filename}' not found. Creating and initializing usage.")

    except IOError as e:
        print(f"Error reading file '{filename}': {e}. Initializing usage.")
        current_usage = {"input_tokens": 0, "output_tokens": 0} # Reset

    # Use formatted printing for current usage
    # print(f"Current usage loaded: input={current_usage.get('input_tokens', 0):,}, output={current_usage.get('output_tokens', 0):,}")

    # --- 3. Calculate new tokens from the input list ---
    new_input_tokens = 0
    new_output_tokens = 0

    for usage_item in usage_metadata_list:
        # Check if attributes exist and are not None before adding
        if hasattr(usage_item, 'prompt_token_count') and usage_item.prompt_token_count is not None:
            new_input_tokens += usage_item.prompt_token_count
        else:
            print(f"Warning: Missing or None 'prompt_token_count' in item: {usage_item}")

        if hasattr(usage_item, 'candidates_token_count') and usage_item.candidates_token_count is not None:
            new_output_tokens += usage_item.candidates_token_count
        else:
             print(f"Warning: Missing or None 'candidates_token_count' in item: {usage_item}")

    # Use formatted printing for new tokens
    print(f"New usage:   input={new_input_tokens:,}, output={new_output_tokens:,}")

    # --- 4. Update total usage ---
    updated_usage = {
        "input_tokens": current_usage.get("input_tokens", 0) + new_input_tokens,
        "output_tokens": current_usage.get("output_tokens", 0) + new_output_tokens
    }

    # --- 5. Write updated usage back to the file ---
    try:
        with open(filename, 'w') as f:
            # Use indent for pretty printing in the file
            json.dump(updated_usage, f, indent=4)
        # print(f"Successfully updated '{filename}'.")
        # Use formatted printing for the final total usage
        print(f"Total usage: input={updated_usage['input_tokens']:,}, output={updated_usage['output_tokens']:,}")
    except IOError as e:
        print(f"Error writing updated usage to file '{filename}': {e}")

    # print("-" * (len(f"--- Updating {usage_type} Usage ({filename}) ---")))
