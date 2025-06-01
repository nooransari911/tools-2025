import os, json
from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError as PydanticValidationError



class UnexpectedNoneError(ValueError):
    """
    Exception raised when a variable or object is None but was expected to be non-None.

    Attributes:
        variable_name (str): The name or description of the variable that was None.
        message (str): The error message.
    """
    def __init__(self, variable_name: str, message: str = None):
        self.variable_name = variable_name
        if message is None:
            self.message = f"Expected '{self.variable_name}' to be a non-None object, but it was None."
        else:
            self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message



class JSONValidationError(Exception):
    """Custom exception for JSON validation errors against a Pydantic model."""

    def __init__(self, message: str, pydantic_error: PydanticValidationError | None = None):
        """
        Initialize the JSONValidationError.

        Args:
            message: A human-readable error message.
            pydantic_error: The original PydanticValidationError, if available.
        """
        super().__init__(message)
        self.pydantic_error = pydantic_error
        self.errors = pydantic_error.errors() if pydantic_error else []

    def __str__(self) -> str:
        """String representation of the exception."""
        base_message = super().__str__()
        if self.pydantic_error:
            # Provide a more detailed message if the Pydantic error is available
            error_details = "\n".join(
                f"  - Location: {'.'.join(map(str, err['loc'])) if err['loc'] else 'N/A'}, "
                f"Type: {err['type']}, Message: {err['msg']}"
                for err in self.errors
            )
            return f"{base_message}\nPydantic Validation Errors:\n{error_details}"
        return base_message



