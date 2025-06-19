import requests, json
from requests import Request
import http.client
import logging



# --- Basic Setup ---
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


http.client.HTTPConnection.debuglevel = 1

requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True




url = "https://api.fireworks.ai/inference/v1/chat/completions"

"""
payload = {
    "max_tokens": 2000,
    "prompt_truncate_len": 1500,
    "temperature": 1,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "repetition_penalty": 1,
    "mirostat_lr": 0.1,
    "mirostat_target": 1.5,
    "n": 1,
    "ignore_eos": False,
    "response_format": {"type": "text"},
    "stream": False,
    "model": "accounts/fireworks/models/deepseek-r1-basic",
    "messages": [
        {
            "role": "user",
            "content": "hi"
        }
    ]
}
"""


payload = {
    "max_tokens": 2000,
    "response_format": {"type": "text"},
    "model": "accounts/fireworks/models/deepseek-r1-basic",
    "messages": [
        {
            "role": "user",
            "content": "hi"
        }
    ]
}
headers = {
    "Authorization": "Bearer fw_3ZnkAi67NHqNZqtD9uhyZWzW",
    "Content-Type": "application/json"
}



# logger.debug(f"Request payload: {json.dumps(payload, indent=4)}")
print (f"Request payload: {json.dumps(payload, indent=4)}")

# llm = LLM (api_key=API_KEY, model=model_id, deployment_type="serverless")
# print (type (messages [0]))
# print (type (messages))
payloadstr = json.dumps (payload)
payloadbytes = payloadstr.encode ("utf-8")
reqobj = Request ("POST", url, headers=headers, json=payload)
prepared_req =reqobj.prepare()

# 3. Print the components for analysis
print("\n" + "="*50)
print("--- REQUEST DETAILS ---")
print(f"METHOD: {prepared_req.method}")
print(f"URL: {prepared_req.url}")
print("\nHEADERS:")
for key, value in prepared_req.headers.items():
    # Hide the API key for security when sharing logs
    if key.lower() == 'authorization':
        print(f"  {key}: Bearer [REDACTED]")
    else:
        print(f"  {key}: {value}")

print("\nBODY (JSON):")
# The body is in bytes, so we decode for pretty printing
if prepared_req.body:
    # Use json.loads and json.dumps for pretty printing
    body_json = json.loads(prepared_req.body.decode('utf-8'))
    print(json.dumps(body_json, indent=4))
else:
    print("  <No Body>")

print("="*50 + "\n")



response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
