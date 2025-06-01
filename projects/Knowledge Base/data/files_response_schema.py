import enum
import types
from src.utils.gemini_utils import register_schema
from pydantic import BaseModel, RootModel, Field, model_validator
from typing import Optional, List, Dict, Any, Union, Type # Ensure Type is imported

@register_schema
class FileListDataItem(BaseModel):
    """
    Represents a single data item within a list, designed to represent a file with its path and contents.

    JSON Representation:
    {
        "file": "File path relative to base dir",
        "content": "Content of the file"
    }

    """
    file: str = Field(None, description="File path relative to base dir")
    content: str = Field (None, description="Content of the file")


class StructuredFileListOutput (BaseModel):
    """
    Response Schema with a list of data items (files in this context);
    Presents files in a structured and list form;
    """

    structured_list: List [FileListDataItem] = Field (..., description="The primary output structured as a list of data items, each with a path and contents")
