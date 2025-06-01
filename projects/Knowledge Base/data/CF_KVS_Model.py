from src.utils.gemini_utils import register_schema
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any



class Generic_Key_Value_Pair (BaseModel):
    key: Any



class CF_KVS_KV_Pair (BaseModel):
    key: Any = Field (..., description="key")
    value: Any = Field (..., description="value")



class CF_KVS_Schema (BaseModel):
    data: List [CF_KVS_KV_Pair] = Field (..., description="Represents the root of CF KVS data")


class Input_Field (BaseModel):
    """
        Represents any input field
    """
    key: Any = Field (..., description="Represents the key in structured output")
    prompt: Optional [str] = Field (None, description="Respresents the str the user is prompted with")


class Input_Model (BaseModel):
    data: List [Input_Field] = Field (..., description="List of generic key-value pairs")



