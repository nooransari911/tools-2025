# Uses static-manifest project ONLY

import vertexai, time
from vertexai.generative_models import GenerativeModel, Part
import time


vertexai.init(project="static-manifest", location="us-west1")
model = GenerativeModel("gemini-1.5-pro-001")
prompt = "perform OCR on this document. Give entire text"




time_start = time.time_ns()

image_file = Part.from_uri(
    "gs://gcloud_pdf_intelligence/scanned_doc.pdf",
    mime_type="application/pdf",
)
image_contents = [image_file, prompt]
response = model.generate_content(image_contents)
print (f"\n\n\n\n{response.text}")
time_end = time.time_ns()
elapsed_time = (time_end - time_start) / (10**9)
print (f"\nOCR on pdf; Gemini 1.5 Pro model;\nElapsed Time for Gemini 1.5 Pro model: {elapsed_time} seconds;\n")