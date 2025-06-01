import io, os, sys
from pathlib import Path

import json
from pydantic import BaseModel, Field
from pydantic_core import PydanticCustomError
from typing import Optional, List, Dict, Any


import data.CF_KVS_Model as KVS
import py_practice.structured_input as iputils


def init_CF_KVS_Pair (k=iputils.DEFAULT_KV_KEY, v=iputils.DEFAULT_KV_VALUE) -> KVS.CF_KVS_KV_Pair:
    kv_pair: KVS.CF_KVS_KV_Pair = KVS.CF_KVS_KV_Pair (key=k, value=v)
    return kv_pair


def init_CF_KVS_Schema (k=iputils.DEFAULT_KV_KEY, v=iputils.DEFAULT_KV_VALUE) -> KVS.CF_KVS_Schema:
    kv_pair: KVS.CF_KVS_KV_Pair = KVS.CF_KVS_KV_Pair (key=k, value=v)
    new_sch: KVS.CF_KVS_Schema = KVS.CF_KVS_Schema (data=[kv_pair])

    return new_sch



def add_to_existing_CF_KVS_Schema (data: dict, sch: KVS.CF_KVS_Schema) -> KVS.CF_KVS_Schema:

    for key in data.keys ():
        new_kv_pair: KVS.CF_KVS_KV_Pair = KVS.CF_KVS_KV_Pair (key=key, value=data.get (key))
        sch.data.append (new_kv_pair)

    return sch




def structured_CF_KV_Pairs_input (KV_List: List [KVS.CF_KVS_KV_Pair]) -> List [KVS.CF_KVS_KV_Pair] :
    loop_bool: bool = True

    while loop_bool:
        try:
            for i in range (100):
                print ("\n")
                ip_key_str = iputils.input_single (f"Enter value for key no. {i}:")
                ip_val_str = iputils.input_single (f"Enter value for val no. {i}:")
                new_kv_pair = init_CF_KVS_Pair (k=ip_key_str, v=ip_val_str)
                KV_List.append (new_kv_pair)

        except KeyboardInterrupt:
            loop_bool = False

    return KV_List






def main ():
    newsch = init_CF_KVS_Schema ()
    newsch.data.append (init_CF_KVS_Pair (k="XS", v="LT"))
    print ("init")
    iputils.print_ser (newsch)
    iputils.print_dashed_header ()

    fields_list = [
        KVS.Input_Field (key="1"),
        KVS.Input_Field (key="2"),
        KVS.Input_Field (key="3"),
        KVS.Input_Field (key="4")
    ]

    input_model = KVS.Input_Model (data=fields_list)
    input_data = {}

    print ("Taking structured input, aribtrary key;")
    input_data = iputils.structured_dict_input_any_key (input_data)
    iputils.print_ser (input_data)
    print ("\n")

    print ("Adding them to existing schema;")
    add_to_existing_CF_KVS_Schema (input_data, newsch)
    iputils.print_ser (newsch)
    iputils.print_dashed_header ()
    input_data = {}


    print ("Taking structured input, fixed key;")
    input_data = iputils.structured_dict_input_fixed_key (input_data, input_model)
    iputils.print_ser (input_data)
    print ("\n")

    print ("Adding them to existing schema;")
    add_to_existing_CF_KVS_Schema (input_data, newsch)
    iputils.print_ser (newsch)
    iputils.print_dashed_header ()


    print ("Testing native KV Pairs input")
    structured_CF_KV_Pairs_input (newsch.data)
    iputils.print_ser (newsch)
    iputils.print_dashed_header ()













if __name__ == "__main__":
    
    try:
        main ()

    # except KeyboardInterrupt:
    #     print ("^C")
    #     sys.exit (0)
    except EOFError:
        print ("^D")
        sys.exit (0)







