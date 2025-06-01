import io, os, sys
from pathlib import Path

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
                
                generated_data [ip_key_str] = ip_val_str
        except KeyboardInterrupt:
            loop_bool = False

    return generated_data











