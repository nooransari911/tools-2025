import io, os, sys
from pathlib import Path
from urllib.parse import urlparse
import json
from pydantic import BaseModel, Field
from pydantic_core import PydanticCustomError
from typing import Optional, List, Dict, Any


import data.CF_KVS_Model as KVS
# from ..data import CF_KVS_Model as KVS

# print (sys.path)



JSON_EXT = ".json"
DEFAULT_KV_KEY = "hi"
DEFAULT_KV_VALUE = "hello"
S3_KVS_FILE = "./data/ssg_redirect.json"




def print_dashed_header (count: int=20):
    header_delimited = "-"
    print (header_delimited * count + "\n\n")




def read_file_validation (path_str: str, ext: str=JSON_EXT) -> Path:
    path_obj = Path (path_str)
    if not path_str.endswith (ext):
        raise ValueError (f"Expected {JSON_EXT}, got {path_str}")
    if not path_obj.exists ():
        raise FileNotFoundError (f"File {path_str} not found")
    if not path_obj.is_file (): # This is the key check for a file
        raise ValueError (f"Expected a file, but {path_str} is not a file (e.g., it's a directory).")
    return path_obj




def read_json_file (path: Path):
    if not isinstance (path, Path):
        raise TypeError (f"Expected type Path, got {type (path)}")

    with open (path, "r") as f:
        json_obj = json.load (f)

    return json_obj


def print_ser (obj: BaseModel):
    if isinstance (obj, BaseModel):
        objstr = obj.model_dump_json (indent=4)

    elif isinstance (obj, dict):
        objstr = json.dumps (obj, indent=4)

    print ("\n\n")
    print (objstr)



def interactive_input_single (prompt: str) -> str:
    while_loop_bool: bool = True

    while while_loop_bool:
        try:
            ip_str: str = input (prompt.ljust (40))
            while_loop_bool = False
        except KeyboardInterrupt:
            print ("^C")

    return ip_str



def input_single (prompt: str) -> str:
    ip_str: str = input (prompt.ljust (40))

    return ip_str


def extract_and_normalize_path(url_string: str) -> str:
    """
    Extracts the path from a full or partial URL and normalizes it.

    This function is designed to:
    1.  Reliably extract the path component from various input formats.
    2.  Ensure directory paths always end with a single trailing slash.
    3.  Leave paths pointing to a file (e.g., /path/image.jpg) as-is.
    4.  Handle the root path correctly, returning "/".

    Args:
        url_string: The string to process, e.g., "https://example.com/about",
                    "example.com/products/", "/path/to/file.html", or "/about".

    Returns:
        A normalized path string, e.g., "/about/", "/products/", or "/path/to/file.html".
    """
    # Guard against empty or whitespace-only input
    if not url_string or not url_string.strip():
        return "/"

    # urlparse is robust. It can handle full URLs, partials like "example.com/path",
    # and raw paths like "/path".
    parsed_url = urlparse(url_string)
    path = parsed_url.path

    # If parsing results in an empty path (e.g., from "https://example.com"),
    # it represents the root of the domain.
    if not path:
        return "/"

    # Determine if the path points to a file by checking for an extension
    # in the last component of the path. os.path.splitext is the most
    # reliable way to do this.
    # e.g., os.path.splitext("file.tar.gz") returns ('file.tar', '.gz')
    basename = os.path.basename(path)
    is_file = bool(os.path.splitext(basename)[1])

    if is_file:
        # It's a file, so we return the path exactly as it is.
        return path
    else:
        # It's a directory, so we MUST ensure it has a trailing slash.
        if not path.endswith('/'):
            return path + '/'
        else:
            return path



def structured_dict_input_fixed_key (generated_data: Dict [Any, Any], keys: KVS.Input_Model) -> dict:
    list_keys = list (keys.data) if keys.data else []
    loop_bool: bool = True

    if not KVS.Input_Model.model_validate (keys, strict=True):
        raise PydanticCustomError ("Validation failed for Input_Model")

    for var in list_keys:
        key = var.key
        if not var.prompt:
            ip_val_str = interactive_input_single (f"\nEnter value for field {key}")

        else:
            ip_val_str = interactive_input_single (f"{var.prompt}")

        generated_data [key] = ip_val_str


    return generated_data



def structured_dict_input_any_key (generated_data: Dict [Any, Any]) -> dict:
    loop_bool: bool = True

    while loop_bool:
        try:
            for i in range (100):
                print ("\n")
                ip_key_str = input_single (f"Enter value for key no. {i}:")
                ip_val_str = input_single (f"Enter value for val no. {i}:")
                
                ip_key_str_path = extract_and_normalize_path (ip_key_str)
                ip_val_str_path = extract_and_normalize_path (ip_val_str)

                generated_data [ip_key_str_path] = ip_val_str_path
        except KeyboardInterrupt:
            loop_bool = False

    return generated_data






import json
import traceback

def main():
    """
    Main function to interactively add to or update an AWS CloudFront KVS file.
    This function reads an existing KVS file, allows adding new entries,
    and saves the combined result, overwriting old entries if keys match.
    """
    try:
        # --- 1. Load Existing Data ---
        existing_kvs_data = None
        existing_redirects = {}
        output_file_path = Path(S3_KVS_FILE)

        if output_file_path.exists() and output_file_path.is_file():
            try:
                with open(output_file_path, "r") as f:
                    json_obj = json.load(f)
                # Validate and parse the existing data using the Pydantic model
                existing_kvs_data = KVS.CF_KVS_Schema.model_validate(json_obj)
                # Convert the list to a dictionary for easy lookups and merging
                for item in existing_kvs_data.data:
                    existing_redirects[item.key] = item.value
                print(f"Successfully loaded {len(existing_redirects)} existing redirects from {S3_KVS_FILE}\n")
            except (json.JSONDecodeError, Exception) as e:
                print(f"Warning: Could not parse existing file at {S3_KVS_FILE}. Starting fresh.")
                print(f"Error details: {e}")
                traceback.print_exc()

        print_dashed_header()
        print("AWS CloudFront KVS File Updater")
        print("Enter new key-value pairs. New entries will overwrite existing ones with the same key.")
        print("Press Ctrl+C when you are finished entering data.")
        print_dashed_header()

        # --- 2. Collect New Data from User ---
        new_data_dict = {}
        structured_dict_input_any_key(new_data_dict) # This function populates the dictionary

        if not new_data_dict:
            print("\nNo new data entered. Exiting without changes.")
            return

        print(f"\nAdding/updating {len(new_data_dict)} redirects.")

        # --- 3. Merge Existing and New Data ---
        # The new dictionary's items will overwrite any matching keys in the existing one.
        merged_redirects = existing_redirects.copy()
        merged_redirects.update(new_data_dict)

        # --- 4. Prepare Data for Pydantic Validation and Serialization ---
        final_kvs_list: List[KVS.CF_KVS_KV_Pair] = []
        for key, value in sorted(merged_redirects.items()): # Sort keys for consistent output
            pair = KVS.CF_KVS_KV_Pair(key=key, value=value)
            final_kvs_list.append(pair)
        
        final_kvs_data = KVS.CF_KVS_Schema(data=final_kvs_list)

        # --- 5. Display Preview and Save ---
        print("\n\n--- Combined KVS Data (Preview) ---")
        print_ser(final_kvs_data)
        print("-----------------------------------")

        # The output path is already defined, but we can re-confirm if needed.
        # For simplicity, we will always write back to the default file.
        output_path = Path(S3_KVS_FILE)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w") as f:
            f.write(final_kvs_data.model_dump_json(indent=4))

        print(f"\nSuccessfully saved {len(final_kvs_data.data)} total redirects to {output_path}")
        print_dashed_header()

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Exiting.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        traceback.print_exc()



# This block ensures the main function is called only when the script is executed directly
if __name__ == "__main__":
    main()




