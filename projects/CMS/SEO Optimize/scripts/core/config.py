# config.py
import logging, uuid
import os, sys, json
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# --- AI Configuration ---
# It's highly recommended to use environment variables for sensitive data

load_dotenv ("/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/.env")
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



AWS_API_GW_API_KEY = os.getenv ("AWS_API_GW_API_KEY").strip ()
API_KEY = os.getenv("FIREWORKS_API_KEY").strip()


AWS_API_GW = "https://z8sw7kg1o2.execute-api.us-west-2.amazonaws.com/v1-initial/api/AI/logs"
API_URL = "https://api.fireworks.ai/inference/v1/chat/completions"
#API_URL = "https://webhook.site/c39f67cc-7bc7-46d1-ab68-dca68eba4dac"

# --- Application Configuration (Unchanged) ---
TOKENS_STORE_JSON_FILE_NAME = os.getenv("CLAUDE_TOKENS_STORE_JSON_FILE_NAME")
SESSION_ID = str (uuid.uuid4 ())
logger.info (f"SESSION ID: {SESSION_ID}")



if not API_KEY:
    raise ValueError("FIREWORKS_API_KEY environment variable not set.")

# Model IDs for specific tasks
QWEN3_235B_MODEL_ID = "accounts/fireworks/models/qwen3-235b-a22b"
QUERY_GENERATION_MODEL = QWEN3_235B_MODEL_ID
CONTENT_OPTIMIZATION_MODEL = QWEN3_235B_MODEL_ID

# --- Prompts ---
# Using f-string compatible templates for easy formatting
QUERY_GENERATION_PROMPT_TEMPLATE = """
Analyze the following file content. Generate a list of 5 to 10 highly relevant search engine queries that a user might type to find this content.
Your response MUST be ONLY a valid JSON object with a single key "queries" that holds a list of strings. Do not add any other text, explanation, or markdown.


File Content:
---
{file_content}
---
"""

CONTENT_OPTIMIZATION_PROMPT_TEMPLATE = """
You are an expert SEO content optimizer.
Your task is to rewrite the 'Original Content' below to improve its relevance and ranking potential for the given 'Search Queries'.
- Integrate the keywords and concepts from the queries naturally.
- Improve headings, structure, and clarity for better readability and SEO.
- Do NOT add any commentary, preamble, or explanation.
- Your output should be ONLY the rewritten content, ready to be saved to a file.

Search Queries:
---
{queries_list}
---

Original Content:
---
{file_content}
---
"""


# --- Processing Configuration ---
DEFAULT_BATCH_SIZE = 4
