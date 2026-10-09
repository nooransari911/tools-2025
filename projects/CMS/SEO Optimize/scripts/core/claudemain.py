#!/usr/bin/env python3
"""
File Processing with AI Optimization
====================================

This script processes a list of file paths, generates relevant queries using AI,
and optimizes each file's content for those queries. It works in configurable
batches with parallel processing within each batch.

Usage:
    python file_processor.py <path_to_file_list> [--batch-size K] [--model-id MODEL]
"""

import logging, uuid
import os, sys, json
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import re
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()
# --- AI Configuration ---
# It's highly recommended to use environment variables for sensitive data
load_dotenv("/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/.env")

# Create formatters
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_formatter = logging.Formatter(
    '%(levelname)s - %(message)s'
)

# Create file logger
file_logger = logging.getLogger('file_logger')
file_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('queries.log')
file_handler.setFormatter(file_formatter)
file_logger.addHandler(file_handler)
file_logger.propagate = False  # Prevent propagation to root logger



# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler (sys.stdout)
console_handler.setFormatter (file_formatter)
logger.addHandler (console_handler)
logger.propagate = False





# Configuration constants
DEFAULT_BATCH_SIZE = 4
DEFAULT_MODEL_ID = "accounts/fireworks/models/qwen3-235b-a22b"

AWS_API_GW_API_KEY = os.getenv("AWS_API_GW_API_KEY").strip()
API_KEY = os.getenv("FIREWORKS_API_KEY").strip()
AWS_API_GW = "https://z8sw7kg1o2.execute-api.us-west-2.amazonaws.com/v1-initial/api/AI/logs"
API_URL = "https://api.fireworks.ai/inference/v1/chat/completions"
#API_URL = "https://webhook.site/c39f67cc-7bc7-46d1-ab68-dca68eba4dac"
# --- Application Configuration (Unchanged) ---
TOKENS_STORE_JSON_FILE_NAME = os.getenv("CLAUDE_TOKENS_STORE_JSON_FILE_NAME")
SESSION_ID = str(uuid.uuid4())
logger.info(f"SESSION ID: {SESSION_ID}")


QUERIES_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "type": "object",
        "properties": {
            "queries": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["queries"],
        "additionalProperties": False

    }
}


QUERIES_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "QueryResponse",
        "schema": {
            "type": "object",
            "properties": {
                "queries": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["queries"],
            "additionalProperties": False
        }
    }
}


GENERAL_CONTENT_GENERATION_INSTRUCTIONS = """
- Avoid improper use of bullets. Paragraph style is better suited for some content, don't use bullets for them. Use paragraph/long from style for content; bullets must be used only where needed
- use simple natural human-like language (but no conversational tone); i expect it to be sharp, comprehensive, highly detailed and "technical" (in a sense)
- Where depth appears too little, add depth as well.
- Avoid excess use of bold.
- Use simple natural human-like language (but no conversational tone); i expect it to be sharp, comprehensive, highly detailed and "technical" (in a sense). Avoid using "....,....,...." sentence structure. use flat, simple, direct, active sentences

"""






# AI Generation Function (provided by user)
def generate_response(
    model_id: str,
    messages: list,
    max_op_tokens=8192,
    system_prompts: str | None = None,
    response_schema: Dict | None = None
):
    """
    Sends messages to the Fireworks.ai API using the Fireworks Python SDK and returns the response.
    """
    logger.info("Generating response from Fireworks.ai (via SDK)...")
    think_content = None
    try:
        from fireworks import LLM
        llm = LLM(
            model=model_id,
            deployment_type="serverless",
            api_key=API_KEY
        )
        reqid = None
        reqtime = datetime.now().astimezone().isoformat()
        response_generator = llm.chat.completions.create(
            messages=messages,
            max_tokens=max_op_tokens,
            stream=True,
            response_format=response_schema
        )
        response_text = ""
        usage_info = None
        for chunk in response_generator:
            # Append token content
            if chunk.choices and chunk.choices[0].delta.content:
                response_text += chunk.choices[0].delta.content
            if hasattr (chunk, "id") and chunk.id:
                reqid = chunk.id
                
            # Capture usage info from the final chunk if available
            if hasattr (chunk, "usage") and chunk.usage:
                input_tokens = chunk.usage.prompt_tokens
                output_tokens = chunk.usage.completion_tokens
                stop_reason = chunk.choices[0].finish_reason if chunk.choices else "unknown"
                usage_info = {
                    "prompt_token_count": input_tokens,
                    "completion_token_count": output_tokens,
                    "total_token_count": input_tokens + output_tokens,
                    "stop_reason": stop_reason
                }
        if usage_info:
            logger.info("\n" + "-" * 40)
            logger.info(f"{'Input tokens':<15}: {usage_info['prompt_token_count']}")
            logger.info(f"{'Output tokens':<15}: {usage_info['completion_token_count']}")
            logger.info(f"{'Stop reason':<15}: {usage_info['stop_reason']}")
            logger.info("-" * 40)
        if reqid:
            reqlogbody = {
                "timestamp": reqtime,
                "request_id": reqid,
                "model_id": model_id,
                "session_id": SESSION_ID
            }
            headers = {
                "Content-Type": "application/json",
                "x-api-key": AWS_API_GW_API_KEY
            }
            awsapigwreq = requests.post (AWS_API_GW, json=reqlogbody, headers=headers)
            
            logger.info (f"Timestamp: {reqtime}")
            logger.info (f"Request Id: {reqid}")
        match = re.search(r'<think>(.*?)</think>', response_text, re.DOTALL)
        if match:
            think_content = match.group(1)
            response_text = re.sub (r"<think>.*?</think>", "", response_text, flags=re.DOTALL).strip ()
        else:
            print("No <think> block found.")
        logger.info(f"Size of response: {sys.getsizeof(response_text)} bytes")
        return (think_content, response_text)
    except ImportError:
        logger.error("Fireworks SDK not installed. Please install it via `pip install fireworks-ai`.")
        return (None, "Fireworks SDK not installed.")
    except Exception as e:
        logger.error(f"An unexpected error occurred in generate_response: {e}")
        return (None, "An unexpected error occurred.")

# File Operations
def read_file_paths(file_list_path: str) -> List[str]:
    """
    Read file paths from a text file.
    
    Args:
        file_list_path: Path to the file containing list of file paths
        
    Returns:
        List of file paths
    """
    try:
        with open(file_list_path, 'r', encoding='utf-8') as f:
            paths = [line.strip() for line in f if line.strip()]
        logger.info(f"Read {len(paths)} file paths from {file_list_path}")
        return paths
    except FileNotFoundError:
        logger.error(f"File list not found: {file_list_path}")
        return []
    except Exception as e:
        logger.error(f"Error reading file list: {e}")
        return []

def read_file_content(file_path: str) -> Optional[str]:
    """
    Read content from a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        File content or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.debug(f"Read content from {file_path}")
        return content
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None

def write_file_content(file_path: str, content: str) -> bool:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file to write
        content: Content to write
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.debug(f"Written content to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error writing file {file_path}: {e}")
        return False

def backup_file(file_path: str) -> bool:
    """
    Create a backup of the original file.
    
    Args:
        file_path: Path to the file to backup
        
    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(file_path)
        backup_path = path.with_name(f"{path.stem} original{path.suffix}")
        shutil.copy2(file_path, backup_path)
        logger.info(f"Created backup: {backup_path}")
        return True
    except Exception as e:
        logger.error(f"Error creating backup for {file_path}: {e}")
        return False

# AI Service Functions
def generate_queries_for_file(file_path: str, content: str, model_id: str) -> List[str]:
    """
    Generate relevant queries for a file using AI.
    
    Args:
        file_path: Path to the file
        content: File content
        model_id: AI model ID
        
    Returns:
        List of relevant queries
    """
    system_prompt = """You are a search engine expert. You can analyze content and generate a set of relevant queries that the content best targets. These queries are the primary queries that users would use to discover the content and content is highly relevant for them. You are supposed to think like a human and identify the set of queries for which my content is supposed to be highly relevant and rank well. Keep a mix of long-tail search queries and more broader queries
    Given a file's contents, generate the set of queries. My goal is to discover these queries.
    Return your response as a JSON object with a 'queries' key containing an array of strings.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze this content and generate relevant queries:\n\nFile: {file_path}\n\nContent:\n{content[:4000]}"}
    ]
    
    try:
        think_content, response_text = generate_response(model_id, messages, response_schema=QUERIES_SCHEMA)
        file_logger.info (f"\n<think>\n{think_content}\n</think>")


        # Extract JSON from response
        json_match = re.search(r'\{.*"queries".*\}', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            queries = result.get("queries", [])
            logger.info (f"Generated {len(queries)} queries for {file_path}")
            file_logger.info (f"Generated queries:\n{queries}")
            return queries
        else:
            logger.warning(f"No valid JSON found in response for {file_path}")
            return []
            
    except Exception as e:
        logger.error(f"Error generating queries for {file_path}: {e}")
        return []

def optimize_content_for_queries(file_path: str, content: str, queries: List[str], model_id: str) -> Optional[str]:
    """
    Optimize file content for given queries using AI.
    
    Args:
        file_path: Path to the file
        content: Original file content
        queries: List of queries to optimize for
        model_id: AI model ID
        
    Returns:
        Optimized content or None if error
    """
    system_prompt = f"""You are an expert content optimizer. Given original content and a list of relevant queries, optimize the content to better match those queries while preserving as much of the original content verbatim and as-is as possible. The original content has been manually reviewed and is of exceptional quality, ensure your generated content also meets these high standards. Improve SEO, readability, and relevance. Return only the optimized content without any additional commentary. Instructions: {GENERAL_CONTENT_GENERATION_INSTRUCTIONS}
    """
    
    queries_text = "\n".join(f"- {query}" for query in queries)
    user_message = f"""Optimize this content for the following queries:
        {queries_text}

        Original content:
        {content}

        Return the optimized content:
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    try:
        think_content, response_text = generate_response(model_id, messages, max_op_tokens=16384)
        
        if response_text and response_text.strip():
            logger.info(f"Optimized content for {file_path}")
            return response_text.strip()
        else:
            logger.warning(f"No optimized content received for {file_path}")
            return None
            
    except Exception as e:
        logger.error(f"Error optimizing content for {file_path}: {e}")
        return None

# Processing Functions
def process_single_file(file_path: str, model_id: str) -> Tuple[str, bool]:
    """
    Process a single file: generate queries and optimize content.
    
    Args:
        file_path: Path to the file to process
        model_id: AI model ID
        
    Returns:
        Tuple of (file_path, success_status)
    """
    logger.info(f"Processing file: {file_path}")
    
    # Read original content
    content = read_file_content(file_path)
    if content is None:
        return file_path, False
    
    # Generate queries
    queries = generate_queries_for_file(file_path, content, model_id)
    if not queries:
        logger.warning(f"No queries generated for {file_path}, skipping optimization")
        return file_path, False
    
    # Optimize content
    """
    optimized_content = optimize_content_for_queries(file_path, content, queries, model_id)
    if optimized_content is None:
        logger.warning(f"No optimized content generated for {file_path}")
        return file_path, False
    
    # Create backup
    if not backup_file(file_path):
        logger.error(f"Failed to create backup for {file_path}")
        return file_path, False
    
    # Write optimized content
    if not write_file_content(file_path, optimized_content):
        logger.error(f"Failed to write optimized content for {file_path}")
        return file_path, False
    """
    logger.info(f"Successfully processed {file_path}")
    return file_path, True

def process_batch(file_paths: List[str], model_id: str) -> List[Tuple[str, bool]]:
    """
    Process a batch of files in parallel.
    
    Args:
        file_paths: List of file paths to process
        model_id: AI model ID
        
    Returns:
        List of (file_path, success_status) tuples
    """
    logger.info(f"Processing batch of {len(file_paths)} files")
    
    results = []
    with ThreadPoolExecutor(max_workers=len(file_paths)) as executor:
        # Submit all tasks
        future_to_path = {
            executor.submit(process_single_file, path, model_id): path 
            for path in file_paths
        }
        
        # Collect results
        for future in as_completed(future_to_path):
            path = future_to_path[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing {path}: {e}")
                results.append((path, False))
    
    return results

def create_batches(file_paths: List[str], batch_size: int) -> List[List[str]]:
    """
    Split file paths into batches.
    
    Args:
        file_paths: List of file paths
        batch_size: Size of each batch
        
    Returns:
        List of batches (each batch is a list of file paths)
    """
    batches = []
    for i in range(0, len(file_paths), batch_size):
        batch = file_paths[i:i + batch_size]
        batches.append(batch)
    
    logger.info(f"Created {len(batches)} batches with size {batch_size}")
    return batches

def process_all_files(file_list_path: str, batch_size: int = DEFAULT_BATCH_SIZE, 
                     model_id: str = DEFAULT_MODEL_ID) -> Dict[str, int]:
    """
    Process all files from the file list in batches.
    
    Args:
        file_list_path: Path to the file containing list of file paths
        batch_size: Number of files to process in each batch
        model_id: AI model ID
        
    Returns:
        Dictionary with processing statistics
    """
    logger.info(f"Starting file processing with batch size: {batch_size}")
    
    # Read file paths
    file_paths = read_file_paths(file_list_path)
    if not file_paths:
        logger.error("No file paths to process")
        return {"total": 0, "successful": 0, "failed": 0}
    
    # Create batches
    batches = create_batches(file_paths, batch_size)
    
    # Process each batch
    total_successful = 0
    total_failed = 0
    
    for i, batch in enumerate(batches, 1):
        logger.info(f"Processing batch {i}/{len(batches)}")
        
        results = process_batch(batch, model_id)
        
        batch_successful = sum(1 for _, success in results if success)
        batch_failed = sum(1 for _, success in results if not success)
        
        total_successful += batch_successful
        total_failed += batch_failed
        
        logger.info(f"Batch {i} completed: {batch_successful} successful, {batch_failed} failed")
    
    # Summary
    stats = {
        "total": len(file_paths),
        "successful": total_successful,
        "failed": total_failed
    }
    
    logger.info(f"Processing complete: {stats}")
    return stats

# Main execution
def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python file_processor.py <path_to_file_list> [--batch-size K] [--model-id MODEL]")
        sys.exit(1)
    
    file_list_path = sys.argv[1]
    batch_size = DEFAULT_BATCH_SIZE
    model_id = DEFAULT_MODEL_ID
    
    # Parse optional arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--batch-size" and i + 1 < len(sys.argv):
            try:
                batch_size = int(sys.argv[i + 1])
                i += 2
            except ValueError:
                logger.error("Invalid batch size")
                sys.exit(1)
        elif sys.argv[i] == "--model-id" and i + 1 < len(sys.argv):
            model_id = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    # Validate environment
    if not API_KEY:
        logger.error("FIREWORKS_API_KEY environment variable not set")
        sys.exit(1)
    
    if not AWS_API_GW_API_KEY:
        logger.error("AWS_API_GW_API_KEY environment variable not set")
        sys.exit(1)
    
    # Process files
    stats = process_all_files(file_list_path, batch_size, model_id)
    
    print(f"\nFinal Results:")
    print(f"Total files: {stats['total']}")
    print(f"Successful: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    
    if stats['failed'] > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
