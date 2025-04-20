import os
import sys
import logging
import tempfile
import pathlib
import mimetypes
from typing import Optional, List, Dict, Any, Tuple

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import google.api_core.exceptions
from google.generativeai import types as genai_types # Use alias to avoid conflict

# --- Environment & Path Setup --- 

# Load environment variables from .env file in the backend directory
load_dotenv()

# Get the path to the original project from .env
ORIGINAL_PROJECT_ROOT = os.getenv("ORIGINAL_PROJECT_PATH")
if not ORIGINAL_PROJECT_ROOT or not os.path.isdir(ORIGINAL_PROJECT_ROOT):
    print(f"Error: ORIGINAL_PROJECT_PATH environment variable not set or invalid: {ORIGINAL_PROJECT_ROOT}", file=sys.stderr)
    sys.exit(1)

# Add the 'src' and 'data' directories from the original project to sys.path
SRC_PATH = os.path.join(ORIGINAL_PROJECT_ROOT, 'src')
DATA_PATH = os.path.join(ORIGINAL_PROJECT_ROOT, 'data')

if not os.path.isdir(SRC_PATH):
    print(f"Error: Cannot find 'src' directory at: {SRC_PATH}", file=sys.stderr)
    sys.exit(1)
# Data path might not be strictly necessary for imports but good practice if used directly
# if not os.path.isdir(DATA_PATH):
#     print(f"Warning: Cannot find 'data' directory at: {DATA_PATH}", file=sys.stderr)

sys.path.insert(0, ORIGINAL_PROJECT_ROOT) # Add project root first
sys.path.insert(1, SRC_PATH)              # Then src

# --- Import from Original Project --- 
try:
    from utils import gemini_utils
    # Schemas are registered when gemini_utils imports data modules
    # Ensure the schema files exist and are importable relative to src_path
except ImportError as e:
    print(f"Error importing modules from '{SRC_PATH}'. Check paths and dependencies. Error: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred during initial imports: {e}", file=sys.stderr)
    sys.exit(1)

# --- Logging Setup --- 
LOG_FILE = os.getenv("LOG_FILE", "./backend_app.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout) # Also log to console
    ]
)
logger = logging.getLogger(__name__)

# --- Backend Configuration --- 
BACKEND_API_KEY_TYPE = os.getenv("BACKEND_API_KEY_TYPE", "free").lower()
if BACKEND_API_KEY_TYPE not in ['free', 'paid']:
    logger.warning(f"Invalid BACKEND_API_KEY_TYPE '{BACKEND_API_KEY_TYPE}'. Defaulting to 'free'.")
    BACKEND_API_KEY_TYPE = 'free'
logger.info(f"Backend configured to use API Key Type: {BACKEND_API_KEY_TYPE}")

# --- FastAPI App Setup --- 
app = FastAPI(title="AI Document Processor API")

# --- CORS Middleware --- 
# Allow requests from your frontend development server and production domain
# Adjust origins as needed for your deployment
origins = [
    "http://localhost:3000", # Default React dev server port
    "http://127.0.0.1:3000",
    # Add your production frontend URL here if deploying
    # "https://your-frontend-domain.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

# --- Pydantic Models for API --- 
class SchemaListResponse(BaseModel):
    schemas: List[str]

class UsageMetadata(BaseModel):
    prompt_token_count: Optional[int] = None
    candidates_token_count: Optional[int] = None
    total_token_count: Optional[int] = None

class ProcessResponse(BaseModel):
    status: str = Field(..., description="'success' or 'error'")
    raw_output: Optional[str] = Field(None, description="The raw text output from the AI model.")
    structured_output: Optional[Any] = Field(None, description="Parsed JSON output if a schema was used and parsing succeeded.")
    schema_used: Optional[str] = Field(None, description="Name of the schema requested, or indication if none was used.")
    usage_metadata: Optional[UsageMetadata] = Field(None, description="Token usage information.")
    error_message: Optional[str] = Field(None, description="Details if status is 'error' or for non-fatal warnings.")

# --- Helper Function for Processing (Synchronous) --- 
def run_single_processing(
    input_file_path: str,
    prompt: str,
    schema_name: Optional[str],
    model_type: str, # 'pro' or 'flash' from frontend
    api_key_type: str # Determined by backend (e.g., from env)
) -> Dict[str, Any]:
    """Synchronously processes a single document using Gemini utils."""
    result = {
        "status": "error",
        "raw_output": None,
        "structured_output": None,
        "schema_used": schema_name if schema_name else "(No Schema - Plain Text)",
        "usage_metadata": None,
        "error_message": None,
    }
    try:
        logger.info(f"Starting processing for file: {os.path.basename(input_file_path)}, model: {model_type}, schema: {schema_name}")

        # 1. Configure Gemini Client (using imported function)
        client, model_name_resolved = gemini_utils.configure_gemini(model_type, api_key_type)
        logger.info(f"Using Gemini Model: {model_name_resolved}")

        # 2. Load Input Content (Handling different types)
        input_part = None
        p_file_path = pathlib.Path(input_file_path)
        file_size = p_file_path.stat().st_size
        logger.info(f"Input file size: {file_size} bytes")

        # Add more robust mime type guessing if needed
        mime_type, _ = mimetypes.guess_type(input_file_path)
        logger.info(f"Guessed MIME type: {mime_type}")

        # Define explicitly supported text-based extensions
        text_extensions = ['.txt', '.md', '.json', '.html', '.css', '.js', '.py', '.java', '.c', '.cpp', '.h', '.hpp', '.xml', '.csv', '.log']

        if mime_type == 'application/pdf':
            input_part = genai_types.Part.from_bytes(data=p_file_path.read_bytes(), mime_type='application/pdf')
        elif mime_type and mime_type.startswith('image/'):
            input_part = genai_types.Part.from_bytes(data=p_file_path.read_bytes(), mime_type=mime_type)
        elif (mime_type and mime_type.startswith('text/')) or \
             mime_type in ['application/json', 'application/markdown'] or \
             p_file_path.suffix.lower() in text_extensions:
            try:
                input_part = p_file_path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                logger.warning(f"UTF-8 decoding failed for {input_file_path}. Trying latin-1.")
                try:
                    input_part = p_file_path.read_text(encoding='latin-1')
                except Exception as enc_err:
                     logger.error(f"Failed to read text file {input_file_path} with fallback encoding: {enc_err}")
                     raise ValueError(f"Could not read text file: {os.path.basename(input_file_path)}")
            except Exception as read_err:
                 logger.error(f"Error reading text file {input_file_path}: {read_err}")
                 raise ValueError(f"Error reading file: {os.path.basename(input_file_path)}")
        else:
            logger.warning(f"Unsupported file type based on MIME '{mime_type}' or extension '{p_file_path.suffix}'. Rejecting.")
            raise ValueError(f"Unsupported file type: {mime_type or p_file_path.suffix}")

        if not input_part:
            raise ValueError("Could not read or load input file content after processing type.")

        contents = [input_part, prompt]
        logger.info(f"Prepared content for Gemini: type={type(input_part)}, prompt length={len(prompt)}")

        # 3. Determine Structured Mode & Schema Class
        is_structured_mode = bool(schema_name)
        schema_class = None
        if is_structured_mode:
            schema_class = gemini_utils.resolve_schema_class(schema_name)
            if not schema_class:
                logger.warning(f"Schema '{schema_name}' selected but not resolved by gemini_utils. Proceeding without structure.")
                is_structured_mode = False
                result["schema_used"] = f"{schema_name} (Not Found)"
                # Add a non-fatal warning to the response message
                result["error_message"] = f"Warning: Schema '{schema_name}' could not be loaded. Output is raw text."

        # 4. Load System Instructions
        sys_instructions = gemini_utils.load_system_instructions(is_structured_mode)
        logger.info(f"System instructions loaded (length: {len(sys_instructions)}). Structured Mode: {is_structured_mode}")

        # 5. Prepare Generation Config
        gen_config_args = {"system_instruction": sys_instructions, "max_output_tokens": 8192}
        if is_structured_mode and schema_class:
            gen_config_args["response_mime_type"] = "application/json"
            gen_config_args["response_schema"] = schema_class
            logger.info(f"Requesting JSON output with schema: {schema_class.__name__}")
        else:
            logger.info("Requesting plain text output.")

        generation_config = genai_types.GenerateContentConfig(**gen_config_args)

        # 6. Call Gemini API (Synchronously via the utility function)
        logger.info("Sending request to Gemini API...")
        start_time = time.time()
        response = gemini_utils.generate_gemini_content(
            genai_client=client,
            model_name=model_name_resolved,
            contents=contents,
            generation_config=generation_config,
            is_structured_mode=is_structured_mode
        )
        end_time = time.time()
        logger.info(f"Gemini API call finished in {end_time - start_time:.2f} seconds.")

        # 7. Process Response
        result["status"] = "success"
        result["raw_output"] = response.text

        if response.usage_metadata:
            result["usage_metadata"] = {
                "prompt_token_count": response.usage_metadata.prompt_token_count,
                "candidates_token_count": response.usage_metadata.candidates_token_count,
                "total_token_count": response.usage_metadata.total_token_count,
            }
            logger.info(f"Usage - In: {result['usage_metadata']['prompt_token_count']}, Out: {result['usage_metadata']['candidates_token_count']}, Total: {result['usage_metadata']['total_token_count']}")
        else:
            logger.warning("No usage metadata received from Gemini API.")

        # 8. Attempt to parse structured output if applicable
        if is_structured_mode:
            logger.info("Attempting to parse structured JSON from response.")
            parsed_json = gemini_utils.parse_json_from_response_text(response.text)
            if parsed_json is not None:
                result["structured_output"] = parsed_json
                logger.info("Successfully parsed structured JSON.")
            else:
                logger.warning("Failed to parse structured JSON from the response text.")
                # Append warning if structure was expected but not parsed
                existing_warning = result["error_message"] or ""
                result["error_message"] = (existing_warning + " Warning: Failed to parse structured JSON from the AI response.").strip()

        logger.info("Processing successful.")

    except google.api_core.exceptions.GoogleAPIError as e:
        logger.error(f"Gemini API Error during processing: {e}", exc_info=False) # Log full trace if needed
        result["status"] = "error"
        # Provide a slightly more user-friendly message
        error_detail = str(e)
        if hasattr(e, 'message'):
             error_detail = e.message
        result["error_message"] = f"Gemini API Error: {error_detail}" # e.g., Resource exhausted, Invalid API Key
    except ValueError as e:
        logger.error(f"Value Error during processing step: {e}", exc_info=True)
        result["status"] = "error"
        result["error_message"] = f"Processing Error: {e}" # e.g., Unsupported file type
    except FileNotFoundError as e:
         logger.error(f"File Not Found Error: {e}", exc_info=True)
         result["status"] = "error"
         result["error_message"] = f"Server Error: Could not find temporary file."
    except PermissionError as e:
         logger.error(f"Permission Error accessing file: {e}", exc_info=True)
         result["status"] = "error"
         result["error_message"] = f"Server Error: File permission issue."
    except Exception as e:
        logger.exception("An unexpected error occurred during processing.") # Log full trace for unexpected errors
        result["status"] = "error"
        result["error_message"] = f"An unexpected server error occurred. Please check server logs." # Keep it generic for user

    return result

# --- API Endpoints --- 

@app.get("/api/schemas", response_model=SchemaListResponse)
async def get_schemas():
    """Returns a list of available schema names."""
    logger.info("Request received for /api/schemas")
    try:
        # Access the registry populated by gemini_utils imports
        schema_names = list(gemini_utils.SCHEMA_REGISTRY.keys())
        logger.info(f"Found schemas: {schema_names}")
        # Ensure the default schema is listed if registry isn't empty
        if schema_names and gemini_utils.DEFAULT_SCHEMA_NAME not in schema_names:
             logger.warning(f"Default schema '{gemini_utils.DEFAULT_SCHEMA_NAME}' missing from registry keys.")
        # You might want to always ensure the default schema is present or handle its absence
        return SchemaListResponse(schemas=schema_names)
    except Exception as e:
        logger.exception("Error fetching schemas from registry.")
        raise HTTPException(status_code=500, detail="Failed to load available schemas.")

@app.post("/api/process", response_model=ProcessResponse)
def process_document(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    schema_name: Optional[str] = Form(None), # Allow schema to be optional
    model_type: str = Form(...) # 'pro' or 'flash'
):
    """Receives a document, prompt, schema, and model type, processes it, and returns results."""
    logger.info(f"Request received for /api/process: filename='{file.filename}', schema='{schema_name}', model='{model_type}'")

    # Input validation
    if not file.filename:
         logger.error("File upload missing filename.")
         raise HTTPException(status_code=400, detail="No file name provided.")
    if model_type not in ['pro', 'flash']:
         logger.error(f"Invalid model_type received: {model_type}")
         raise HTTPException(status_code=400, detail="Invalid model type specified. Must be 'pro' or 'flash'.")
    if not prompt.strip():
        logger.error("Empty prompt received.")
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    # Use a temporary file to store the upload
    temp_file_path = None
    try:
        # Create a temporary directory if it doesn't exist
        temp_dir = pathlib.Path("./temp_uploads")
        temp_dir.mkdir(exist_ok=True)

        # Sanitize filename slightly (more robust sanitization might be needed)
        safe_filename = pathlib.Path(file.filename).name
        temp_file_path = temp_dir / safe_filename

        logger.info(f"Saving uploaded file to temporary path: {temp_file_path}")
        with open(temp_file_path, "wb") as buffer:
            buffer.write(file.file.read())
        logger.info(f"Temporary file saved successfully.")

        # Call the synchronous processing function
        # The API endpoint remains synchronous ('def' not 'async def')
        # FastAPI handles running this in a thread pool
        import time # Import time inside function if not already global
        processing_start_time = time.time()
        result_dict = run_single_processing(
            input_file_path=str(temp_file_path),
            prompt=prompt,
            schema_name=schema_name if schema_name else None, # Pass None if empty string
            model_type=model_type,
            api_key_type=BACKEND_API_KEY_TYPE # Use backend-configured key type
        )
        processing_end_time = time.time()
        logger.info(f"run_single_processing completed in {processing_end_time - processing_start_time:.2f} seconds.")

        # Return the result using the Pydantic model for validation and serialization
        # If result_dict structure matches ProcessResponse, this works directly
        # Handle potential internal server errors during processing explicitly
        if result_dict['status'] == 'error' and not result_dict.get('error_message'):
             result_dict['error_message'] = 'An internal server error occurred during processing.'

        # Return the result dictionary directly, FastAPI will serialize it based on response_model
        # Use JSONResponse only if you need custom status codes based on result['status']
        status_code = 200 if result_dict['status'] == 'success' else 500 # Or 4xx for specific client errors caught inside
        # If using specific HTTP status codes based on processing outcome:
        # return JSONResponse(content=result_dict, status_code=status_code)
        # Otherwise, letting FastAPI handle it with response_model is cleaner:
        return result_dict

    except HTTPException as http_exc:
        # Re-raise client-side errors (4xx)
        raise http_exc
    except Exception as e:
        logger.exception("Unhandled error in /api/process endpoint wrapper.")
        # Return a generic 500 error response
        return JSONResponse(
             content=ProcessResponse(
                 status="error",
                 error_message="An unexpected error occurred on the server while handling the request."
             ).model_dump(), # Use model_dump() for Pydantic v2
             status_code=500
         )
    finally:
        # --- Cleanup: Remove the temporary file --- 
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.info(f"Successfully removed temporary file: {temp_file_path}")
            except OSError as e:
                logger.error(f"Error removing temporary file {temp_file_path}: {e}")
        # Clean up the temporary file object if needed
        if file:
            try:
                 file.file.close()
            except Exception: pass # Ignore errors during close


# --- Root Endpoint (Optional) --- 
@app.get("/")
async def read_root():
    return {"message": "AI Document Processor API is running."}

# --- Run with Uvicorn (for local development) --- 
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server for local development...")
    # Ensure necessary env vars are loaded before configure_gemini is potentially called
    # (already done by load_dotenv() at the top)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)