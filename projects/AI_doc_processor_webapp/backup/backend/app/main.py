# ai_doc_processor_webapp/backend/app/main.py
import os
import sys
import pathlib
import logging
from typing import Optional, List # Import List

# Third-party imports
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# --- Setup logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
main_logger = logging.getLogger("api_main")

# --- Path setup and sys.path modification ---
try:
	backend_dir = pathlib.Path(__file__).resolve().parent.parent
	webapp_root = backend_dir.parent
	original_project_root = webapp_root.parent / "Knowledge Base" # ** ADJUST IF NEEDED **
	main_logger.info(f"Original project root: {original_project_root}")
	if not original_project_root.is_dir(): main_logger.warning("Original project root not found!")
	original_project_root_str = str(original_project_root)
	if original_project_root_str not in sys.path:
		sys.path.insert(0, original_project_root_str)
		main_logger.info(f"Added to sys.path: {original_project_root_str}")
except Exception as path_e: main_logger.critical(f"Path error: {path_e}", exc_info=True); sys.exit(1)

# --- Load .env ---
dotenv_path = backend_dir / ".env"
if dotenv_path.is_file(): load_dotenv(dotenv_path=dotenv_path, override=True); main_logger.info(f"Loaded .env: {dotenv_path}")
else: main_logger.warning(f"Backend .env not found: {dotenv_path}")

# --- Imports ---
try:
	from src.utils import gemini_utils
	# ** NOTE: ProcessForm is still imported but no longer used via Depends() in the endpoint **
	from .schemas.api_models import ProcessResponse, SchemaListResponse, ProcessForm
	from .core.processor import process_document_web_multi # Import new multi processor
	main_logger.info("Imports successful.")
except ImportError as e: main_logger.critical(f"Import failed: {e}", exc_info=True); sys.exit(1)
except Exception as import_e: main_logger.critical(f"Unexpected Import Error: {import_e}", exc_info=True); sys.exit(1)

# --- FastAPI App & CORS ---
app = FastAPI(title="AI Document Processor API", version="1.7.1 MULTI-FIX") # Version bump
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
app.add_middleware(CORSMiddleware, allow_origins=[frontend_origin], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
main_logger.info(f"CORS for: {frontend_origin}")

# --- API Endpoints ---

@app.get("/api/schemas", response_model=SchemaListResponse, summary="Get Schemas")
async def get_available_schemas():
	"""Retrieves the list of registered schema names."""
	try:
		schema_names = list(gemini_utils.SCHEMA_REGISTRY.keys()); schema_names.insert(0, "(No Schema - Plain Text)")
		return SchemaListResponse(schemas=schema_names)
	except Exception as e: main_logger.error(f"Schema registry error: {e}", exc_info=True); raise HTTPException(status_code=500, detail="Schema load error.")

# --- REWRITTEN /api/process endpoint for MULTIPLE FILES (Using explicit Form fields) --- 
@app.post("/api/process", response_model=ProcessResponse, summary="Process Uploaded Documents")
async def process_files_endpoint(
	# ** Expect a LIST of files under the key 'files' **
	files: List[UploadFile] = File(..., description="One or more document files to process."),
	# ** Explicitly define form fields using Form() instead of Depends() **
	prompt: str = Form(..., description="Instructions for processing."),
	schema_name: str = Form(..., description="Schema name or '(No Schema - Plain Text)'."),
	model_type: str = Form(..., description="Model type ('pro' or 'flash')."),
	api_key_type: str = Form(..., description="API key type ('free' or 'paid').")
):
	"""Handles multiple file uploads and triggers batch processing."""
	main_logger.info(f"Processing request for {len(files)} file(s): schema='{schema_name}', model='{model_type}', key='{api_key_type}'")
	
	if not files:
		 raise HTTPException(status_code=400, detail="No files were uploaded.")

	# --- Manually create the ProcessForm object --- 
	# This is needed because the processor function expects it.
	try:
		form_data_obj = ProcessForm(
			prompt=prompt,
			schema_name=schema_name,
			model_type=model_type,
			api_key_type=api_key_type
		)
	except Exception as pydantic_e: # Catch potential validation errors during manual creation
		main_logger.error(f"Pydantic validation error for form fields: {pydantic_e}", exc_info=False)
		raise HTTPException(status_code=422, detail=f"Invalid form field data: {pydantic_e}")

	files_data_to_process = []
	processed_filenames = set()

	try:
		# --- Read all files first --- 
		for file in files:
			if not file.filename:
				main_logger.warning("Skipping upload with no filename.")
				continue # Skip files without names
			# Prevent duplicate filenames in the same request if needed
			if file.filename in processed_filenames:
				main_logger.warning(f"Duplicate filename '{file.filename}' in request, skipping second instance.")
				continue
			
			content = await file.read()
			if not content:
				main_logger.warning(f"Skipping empty file: {file.filename}")
				continue # Skip empty files
			
			files_data_to_process.append((file.filename, content, file.content_type or 'application/octet-stream'))
			processed_filenames.add(file.filename)
			await file.close() # Close file after reading
		
		if not files_data_to_process:
			 raise HTTPException(status_code=400, detail="No valid files found to process after initial checks.")

		main_logger.info(f"Prepared {len(files_data_to_process)} files for processing.")

		# --- Call Core Logic for MULTIPLE files --- 
		result_data = await process_document_web_multi(
			files_data=files_data_to_process,
			form_data=form_data_obj # Pass the manually created form data model
		)
		main_logger.info(f"Multi-file processor completed with status: {result_data.get('status')}")
		return ProcessResponse(**result_data)

	except HTTPException as http_exc:
		main_logger.warning(f"HTTPException: {http_exc.status_code} - {http_exc.detail}")
		raise http_exc # Re-raise validation/early errors
	except Exception as e:
		main_logger.error(f"!!! UNEXPECTED Endpoint Error: {type(e).__name__}: {e}", exc_info=True)
		# Return a structured error response even for unexpected errors
		return ProcessResponse(
			status="error",
			overall_error_message=f"Internal Server Error: {type(e).__name__}",
			results=[]
		)


# --- Health Check & Root Endpoints ---
@app.get("/api/health", summary="Health Check")
async def health_check(): return {"status": "ok"}
@app.get("/", summary="API Root")
async def read_root(): return {"message": "API running"}
