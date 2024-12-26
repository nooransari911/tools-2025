import time
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.cloud import storage
from dotenv import load_dotenv
from strings import *
load_dotenv()


# Initialize Vertex AI with your project details
vertexai.init(project="optimum-task-411411", location="us-west1")
model = GenerativeModel ("gemini-1.5-flash")




# Function to send the PDF and prompt to Gemini
def send_pdf_to_gemini (prompt, pdf_uri=None):
    # Create a Part object for the PDF from the GCS URI
    model_prompt = []
    model_prompt = [Part.from_uri(pdf_uri, mime_type="application/pdf")] if pdf_uri else []
    model_prompt.append (prompt)

    # Send the PDF and prompt to the Gemini model
    response = model.generate_content(model_prompt)

    # Return Gemini output text
    return response.text


def send_to_gemini_chain (pdf_uri=None):
    #gemini_input = [Part.from_uri(pdf_uri, mime_type="application/pdf")] if pdf_uri else []
    gemini_input = LOREM_IPSUM_STRING
    gemini_response = None


    # Iterate over the list of prompts
    for pri in PROMPTS_LOREM_IPSUM:
        # Append the current prompt to the input
        gemini_input.append(pri)

        # Add previous response (if available) to the current prompt
        if gemini_response:
            gemini_input.append(gemini_response.text)

        # Send the input (PDF or previous response + current prompt) to Gemini
        gemini_response = model.generate_content(gemini_input)
        time.sleep(80)
        RESPONSES.append (gemini_response.text)
        gemini_input = []


    with open (output_file, "w") as md_output_file:
        md_output_file.write (gemini_response.text)
    with open(all_iterations_file, "w") as md_file:
        md_file.write (f"{RESPONSES}")

    # Return Gemini output text
    return gemini_response.text





# Function to process a single PDF from GCS and append the Gemini output to markdown file
def process_single_pdf_from_gcs (bucket_name, pdf_blob_name, prompt):
    # Send the PDF to Gemini and get the OCR output
    pdf_uri = f"gs://{bucket_name}/{pdf_blob_name}"
    #gemini_output = send_pdf_to_gemini (prompt, pdf_uri)
    gemini_output = send_to_gemini_chain ()


    # Prepare the markdown content
    markdown_content = f"# {pdf_blob_name}\n\n{gemini_output}\n\n"

    print (markdown_content)




# Function to process multiple PDFs from a GCS bucket and append results to markdown file
def process_pdfs_from_gcs(bucket_name, pdf_folder, output_file, prompt):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs (prefix=pdf_folder)


    # Prepare a string to hold all the markdown content
    all_markdown_content = ""

    for blob in blobs:
        if blob.name.endswith (".pdf"):
            # Send the PDF to Gemini and get the OCR output
            pdf_uri = f"gs://{bucket_name}/{blob.name}"
            gemini_output = send_pdf_to_gemini(pdf_uri, prompt)

            # Append the output to the markdown content
            all_markdown_content += f"# {blob.name}\n\n{gemini_output}\n\n"

    with open (output_file, "w") as md_output_file:
        md_output_file.write (all_markdown_content)




if __name__ == "__main__":
    # Call either function depending on what you need
    # Example: Process a single PDF from GCS
    time_start = time.time_ns()
    process_single_pdf_from_gcs(bucket_name, "Job Roadmap For Students.pdf", prompt_extract)
    time_end = time.time_ns()
    elapsed_time = (time_end - time_start) / (10 ** 9)

    print(f"Request complete in: {elapsed_time} seconds;\n")


    # Example: Process all PDFs in a folder in the GCS bucket
    # process_pdfs_from_gcs(bucket_name, "pdfs/", output_file, prompt_extract)
