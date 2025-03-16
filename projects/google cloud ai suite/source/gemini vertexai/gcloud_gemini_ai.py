"""
export Gemini API Key to API_KEY

"""
import time

import google.generativeai as genai
from vertexai.generative_models import Part
from google.cloud import storage
import datetime, os, json, re


genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel("gemini-1.5-pro")

prompt = "briefly describe this image"
image_file = Part.from_uri(
    "gs://gcloud_image_intelligence/The Lesser Evil - Pick it.mp4",
    mime_type="video/mp4",
)
#image_contents = [prompt, image_file]
#response = model.generate_content(image_contents)


# lesser evil video:
#   total_tokens=351,640, 0.3 millions
#   roughly $1.225 @ $3.5/1 million tokens





"""
gcs_source_uri = "gs://gcloud_image_intelligence/"
gs_url_pattern = r'gs://([^/]+)'
match = re.match (gs_url_pattern, gcs_source_uri)
bucket_name = match.group(1)

storage_client = storage.Client(project="optimum-task-411411")
bucket = storage_client.get_bucket(bucket_name)


# List objects with the given prefix, filtering out folders.
blob_list = bucket.list_blobs ()

pattern = re.compile(r'.*\.mp4$')
# Filter and list files using re.match()
all_files = [blob for blob in blob_list if pattern.match(blob.name)]
print (all_files)
"""


genai_file = genai.upload_file (path="/home/ansarimn/Downloads/lesser evil.mp4", display_name="lesser evil")

while genai_file.state.name == "PROCESSING":
    print('.', end='')
    time.sleep(10)
    genai_file = genai.get_file (genai_file.name)

if genai_file.state.name == "FAILED":
  raise ValueError(genai_file.state.name)



for file in genai.list_files():
    print(f"{file.display_name}, URI: {file.uri}")
    model_input_token = model.count_tokens(file)
    print(model_input_token)
    genai.delete_file(file.name)

