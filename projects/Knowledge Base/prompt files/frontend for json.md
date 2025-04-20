Build a beautiful frontend HTML page to the render the provided JSON schema. Use only pure HTML, JS, CSS. It should be very beautiful, modern and attractive. Use dark mode and black (#000000) color.

Your output will go directly into a single HTML file, so don't use markdown code block backticks.

First the HTML page would dynamically fetch the data from json file "sample generic response.json" and then render it. So content in HTML would all be dynamic and strictly do not include content, provided example or otherwise, within the HTML file.

Title of HTML page and topmost H1 heading of the page should be "Dummy AI Response".


The JSON Schema below is a generic schema I use to get structured output from AI models. It is quite structured while being felxible enough to suit most situations.



JSON Schema [the `StructuredListOutput` class here]:
```
import enum
import types
from src.utils.gemini_utils import register_schema
from pydantic import BaseModel, RootModel, Field, model_validator
from typing import Optional, List, Dict, Any, Union, Type # Ensure Type is imported


# --- Ensure schema_config and register_schema are defined as before ---
# from schema_config import register_schema, DEFAULT_SCHEMA_NAME

# --- Enum defining common Python type names (as strings) ---
# (Same as before)
class PythonBasicTypeName(str, enum.Enum):
    STR = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    LIST_STR = "list_str"
    DICT_STR_ITEMS = "dict_str_items"
    DICT_INT_ITEMS = "dict_int_items"
    NONE = "None"



PYTHON_TYPE_MAP: Dict[PythonBasicTypeName, Type] = {
    PythonBasicTypeName.STR: str,
    PythonBasicTypeName.INT: int,
    PythonBasicTypeName.FLOAT: float,
    PythonBasicTypeName.BOOL: bool,
    PythonBasicTypeName.LIST_STR: list, # Base type is list
    PythonBasicTypeName.DICT_STR_ITEMS: list, # Base type is list (of key-value items)
    PythonBasicTypeName.DICT_INT_ITEMS: list, # Base type is list (of key-value items)
    PythonBasicTypeName.NONE: types.NoneType,
}



class KeyValuePairStrStr (BaseModel):
    key: str = Field (..., description="Key for key-value pair")
    value: str = Field (..., description="Value (str) for the key-value pair")


class KeyValuePairStrInt (BaseModel):
    key: str = Field (..., description="Key for key-value pair")
    value: int = Field (..., description="Value (int) for the key-value pair")






# --- Define the structure for each item in the list ---
class ListDataItem(BaseModel):
    """
    Represents a single data item within a list, designed for maximum schema
    compatibility by avoiding Union/Any in field types. Exactly one '..._content'
    field should be non-None, matching the 'type' field (unless type is NONE).
    """
    # --- Mandatory Type Indicator ---
    type: PythonBasicTypeName = Field(
        ...,
        description="Indicates which specific content field holds the actual data for this item."
    )

    # --- Optional Content Fields (One per Type) ---
    # Basic Types
    string_content: Optional[str] = Field(None, description="Content if type is 'str'.")
    integer_content: Optional[int] = Field(None, description="Content if type is 'int'.")
    float_content: Optional[float] = Field(None, description="Content if type is 'float'.")
    boolean_content: Optional[bool] = Field(None, description="Content if type is 'bool'.")

    # Collection Types (Using basic, common structures for schema compatibility)
    # Note: For lists/dicts containing complex objects, you might need nested models.
    list_str_content: Optional[List[str]] = Field(
        None,
        description="Content if type is 'list'. Assumes a list of string."
    )
    dict_str_content: Optional[KeyValuePairStrStr] = Field(
        None,
        description="Content if type is 'dict'. Assumes string keys and string values."
    )
    dict_int_content: Optional[KeyValuePairStrInt] = Field(
        None,
        description="Content if type is 'dict'. Assumes str keys and int values."
    )
    # Note: No specific content field is needed for type 'None'. Its presence is indicated
    # by type='None' and all other content fields being None.

    # --- Optional Metadata Fields ---
    description: Optional[str] = Field(
        None,
        description="Optional description or context."
    )
    source: Optional[str] = Field(
        None,
        description="Optional source information."
    )
    label: Optional[str] = Field(
        None,
        description="Optional label or key associated with this item."
    )

    @model_validator(mode='after')
    def check_correct_content_field_populated(self) -> 'ListDataItem':
        """
        Ensures exactly one content field is populated and matches the declared 'type',
        or none are populated if type is 'None'.
        """
        # Map the type enum to the corresponding content field name
        type_to_field_map: Dict[PythonBasicTypeName, Optional[str]] = {
            PythonBasicTypeName.STR: 'string_content',
            PythonBasicTypeName.INT: 'integer_content',
            PythonBasicTypeName.FLOAT: 'float_content',
            PythonBasicTypeName.BOOL: 'boolean_content',
            PythonBasicTypeName.LIST_STR: 'list_str_content',
            PythonBasicTypeName.DICT_INT_ITEMS: 'dict_int_content',
            PythonBasicTypeName.DICT_STR_ITEMS: 'dict_str_content',
            PythonBasicTypeName.NONE: None # None type has no dedicated content field
        }

        expected_field_name = type_to_field_map.get(self.type)

        populated_fields = []
        for field_name in type_to_field_map.values():
            # Check fields that are supposed to hold content
            if field_name is not None and getattr(self, field_name) is not None:
                 # Need special check for boolean_content == False, it *is* populated
                 if field_name == 'boolean_content' or getattr(self, field_name):
                     populated_fields.append(field_name)

        # --- Validation Logic ---
        if self.type == PythonBasicTypeName.NONE:
            # If type is None, NO content field should be populated
            if populated_fields:
                raise ValueError(
                    f"Type is '{self.type.value}', but unexpected content field(s) "
                    f"are populated: {populated_fields}"
                )
        else:
            # If type is NOT None, expected_field_name should be non-None
            if expected_field_name is None:
                 # This indicates an internal configuration error (Enum vs map mismatch)
                 raise ValueError(f"Internal error: No content field mapped for type '{self.type.value}'")

            # Exactly one content field must be populated
            if len(populated_fields) == 0:
                 raise ValueError(
                    f"Type is '{self.type.value}', but no corresponding content field "
                    f"('{expected_field_name}') is populated."
                 )
            if len(populated_fields) > 1:
                raise ValueError(
                    f"Type is '{self.type.value}', but multiple content fields are populated: "
                    f"{populated_fields}. Only '{expected_field_name}' should be populated."
                )
            # The single populated field must be the correct one
            if populated_fields[0] != expected_field_name:
                 raise ValueError(
                    f"Type is '{self.type.value}', which requires field '{expected_field_name}', "
                    f"but field '{populated_fields[0]}' was populated instead."
                )


            # --- SNIPPET TO ADD: Value Type Validation ---
            expected_python_type = PYTHON_TYPE_MAP.get(self.type)
            if expected_python_type is None:
                raise ValueError(f"Internal config error: No Python type mapping for '{self.type.value}'")

            actual_value = getattr(self, expected_field_name)

            type_match = False
            if expected_python_type is float and isinstance(actual_value, int):
                type_match = True
            elif expected_python_type is types.NoneType: # Should only happen if type is NONE, handled above, but safe check
                 type_match = (actual_value is None)
            elif isinstance(actual_value, expected_python_type):
                type_match = True

            if not type_match:
                raise ValueError(
                    f"Value Type Mismatch: Field '{expected_field_name}' is populated, "
                    f"but its value's Python type ('{type(actual_value).__name__}') "
                    f"does not match the expected type ('{expected_python_type.__name__}') "
                    f"implied by the declared item type '{self.type.value}'. "
                    f"Value: {repr(actual_value)}"
                )
            # --- END OF SNIPPET ---


        # If all checks pass
        return self








@register_schema
class StructuredListOutput (BaseModel):
    """
    This is the main schema.
    Response Schema with a list of typed data items;
    Presents structured and typed data in a list form;
    """

    structured_list: List [ListDataItem] = Field (..., description="The primary output structured as a list of data items, each with a declared type, content, and optional metadata.")

    notes: Optional [str] = Field (..., description="Optional notes about the generated response")

    summary: Optional [str] = Field (..., description="Optional summary about response")
```

