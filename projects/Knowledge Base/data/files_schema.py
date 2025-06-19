from src.utils.gemini_utils import register_schema
from pydantic import BaseModel, Field # Added for schema definition
from typing import Optional, List # Added for strong typing in schema

class FileData(BaseModel):
    """
    Represents a file, storing its relative path and its textual contents.

    This model is used to encapsulate the data associated with a single file,
    making it easy to pass around and validate.
    """
    file: str = Field(..., description="The relative path to the file.")
    contents: str = Field(..., description="The textual content of the file.")


@register_schema
class FileDataList(BaseModel):
    """
    A collection of FileData objects.

    This model represents a list of files, each described by its
    relative path and content.
    """
    items: List[FileData] = Field(..., description="A list of FileData objects.")
