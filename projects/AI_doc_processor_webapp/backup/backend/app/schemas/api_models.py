# ai_doc_processor_webapp/backend/app/schemas/api_models.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# --- Model for Overall Usage --- 
class UsageMetadata(BaseModel):
    """ Structure for aggregated token usage information. """
    prompt_token_count: int = 0
    candidates_token_count: int = 0
    total_token_count: int = 0

# --- Model for a Single File's Result --- 
# ** ADDED MISSING MODEL DEFINITION **
class SingleFileResult(BaseModel):
    """ Structure for the result of processing a single file. """
    file_name: str
    status: str = "success" # 'success' or 'error'
    raw_output: Optional[str] = None
    structured_output: Optional[Any] = None
    error_message: Optional[str] = None
    # Per-file usage could be added here if needed later
    # usage_metadata: Optional[UsageMetadata] = None 

# --- Model for the Overall API Response (for Multi-File) --- 
class ProcessResponse(BaseModel):
    """ Structure for the final response from the /process endpoint. """
    status: str = "success" # 'success', 'error', 'partial_success'
    overall_error_message: Optional[str] = None
    results: List[SingleFileResult] = [] # List of results for each file
    schema_used: Optional[str] = None
    overall_usage_metadata: Optional[UsageMetadata] = None

# --- Model for Schema List Response --- 
class SchemaListResponse(BaseModel):
    """ Response structure for the /schemas endpoint. """
    schemas: List[str]

# --- Model for Form Fields (Explicit Form() usage) ---
# This model is still useful for structuring the data passed to the processor
class ProcessForm(BaseModel):
    """ Defines the expected form fields (used internally now). """
    prompt: str = Field(..., description="Instructions for processing.")
    schema_name: str = Field(..., description="Schema name or '(No Schema - Plain Text)'.")
    model_type: str = Field(..., description="Model type ('pro' or 'flash').")
    api_key_type: str = Field(..., description="API key type ('free' or 'paid').")
