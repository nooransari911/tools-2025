# ai_operations.py
import logging
import json
import re
import sys
from datetime import datetime
import requests

# Import config variables
from config import (
    API_KEY, QUERY_GENERATION_MODEL, CONTENT_OPTIMIZATION_MODEL,
    QUERY_GENERATION_PROMPT_TEMPLATE, CONTENT_OPTIMIZATION_PROMPT_TEMPLATE,
    AWS_API_GW, AWS_API_GW_API_KEY, SESSION_ID
)

logger = logging.getLogger(__name__)

# The provided sample AI call function
def generate_response(
    model_id: str,
    messages: list,
    max_op_tokens=8192
):
    """
    Sends messages to the Fireworks.ai API and returns the response text.
    (This is the function provided in the prompt, slightly adapted for modularity)
    """
    logger.info(f"Generating response from model: {model_id}")
    try:
        from fireworks.client import Fireworks

        client = Fireworks(api_key=API_KEY)
        
        # The sample code used a different SDK structure, this aligns with fireworks-ai > 1.0.0
        response_generator = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=max_op_tokens,
            stream=True,
        )

        response_text = ""
        for chunk in response_generator:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                response_text += chunk.choices[0].delta.content
        
        logger.info(f"Raw response received, length: {len(response_text)} chars")
        return response_text

    except ImportError:
        logger.error("Fireworks SDK not installed. Please install it via `pip install fireworks-ai`.")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred in generate_response: {e}")
        return None

def get_relevant_queries(file_content: str) -> list[str] | None:
    """
    Calls the AI to generate relevant queries for the given content.
    """
    prompt = QUERY_GENERATION_PROMPT_TEMPLATE.format(file_content=file_content)
    messages = [{"role": "user", "content": prompt}]
    
    response_text = generate_response(QUERY_GENERATION_MODEL, messages)
    
    if not response_text:
        logger.error("Did not receive a response for query generation.")
        return None

    try:
        # The AI might include markdown ```json ... ```, so we extract it.
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            logger.error(f"Could not find a JSON object in the AI response: {response_text}")
            return None
            
        data = json.loads(json_match.group(0))
        queries = data.get("queries")
        
        if not isinstance(queries, list):
            logger.error(f"JSON response is malformed. 'queries' is not a list: {data}")
            return None
            
        logger.info(f"Successfully extracted {len(queries)} queries.")
        return queries
        
    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON from response: {response_text}")
        return None

def optimize_content_for_queries(file_content: str, queries: list[str]) -> str | None:
    """
    Calls the AI to optimize content based on a list of queries.
    """
    queries_list_str = "\n".join(f"- {q}" for q in queries)
    prompt = CONTENT_OPTIMIZATION_PROMPT_TEMPLATE.format(
        queries_list=queries_list_str,
        file_content=file_content
    )
    messages = [{"role": "user", "content": prompt}]

    optimized_content = generate_response(CONTENT_OPTIMIZATION_MODEL, messages)

    if not optimized_content:
        logger.error("Did not receive a response for content optimization.")
        return None

    logger.info("Successfully generated optimized content.")
    return optimized_content.strip()
