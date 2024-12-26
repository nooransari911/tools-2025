import os
from typing import Iterator, MutableSequence, Optional, Sequence, Tuple

import google.cloud.documentai_v1 as docai
from tabulate import tabulate
from document_ai_batch_process import batch_process_documents


PROJECT_ID = os.getenv("PROJECT_ID", "")
API_LOCATION = os.getenv("API_LOCATION", "")

assert PROJECT_ID, "PROJECT_ID is undefined"
#assert API_LOCATION in ("us", "eu"), "API_LOCATION is incorrect"


# Test processors
document_ocr_display_name = "document-ocr"
document_summary_display_name = "document-summary"
document_invoice_display_name = "document-invoice"

test_processor_display_names_and_types = (
    (document_ocr_display_name, "OCR_PROCESSOR"),
    (document_summary_display_name, "SUMMARY_PROCESSOR"),
    (document_invoice_display_name, "INVOICE_PROCESSOR")
)



# TODO(developer): Fill these variables before running the sample.
project_id = "optimum-task-411411"
location = "us"  # Format is "us" or "eu"
processor_id = "YOUR_PROCESSOR_ID"  # Create processor before running sample
gcs_output_uri = "gs://gcloud_pdf_intelligence_destination/"  # Must end with a trailing slash `/`. Format: gs://bucket/directory/subdirectory/
processor_version_id = (
    "pretrained-foundation-model-v1.0-2023-08-22"  # Optional. Example: pretrained-ocr-v1.0-2020-09-23
)

# TODO(developer): If `gcs_input_uri` is a single file, `mime_type` must be specified.
gcs_input_uri = "gs://gcloud_pdf_intelligence/"  # Format: `gs://bucket/directory/file.pdf`` or `gs://bucket/directory/``
input_mime_type = "application/pdf"
field_mask = "text,entities,pages.pageNumber"  # Optional. The fields to return in the Document object.




# Get client, parent
def get_client() -> docai.DocumentProcessorServiceClient:
    client_options = {"api_endpoint": f"{API_LOCATION}-documentai.googleapis.com"}
    return docai.DocumentProcessorServiceClient(client_options=client_options)


def get_parent(client: docai.DocumentProcessorServiceClient) -> str:
    return client.common_location_path(PROJECT_ID, API_LOCATION)


def get_client_and_parent() -> Tuple[docai.DocumentProcessorServiceClient, str]:
    client = get_client()
    parent = get_parent(client)
    return client, parent




def create_processor (display_name: str, type: str) -> docai.Processor:
    client, parent = get_client_and_parent()
    processor = docai.Processor (display_name=display_name, type_=type)

    return client.create_processor (parent=parent, processor=processor)


def create_all_test_processors ():
    separator = "=" * 80
    for display_name, type in test_processor_display_names_and_types:
        print(separator)
        print(f"Creating {display_name} ({type})...")
        try:
            create_processor(display_name, type)
        except Exception as err:
            print(err)
    print(separator)
    print("Done")


def list_processors() -> MutableSequence[docai.Processor]:
    client, parent = get_client_and_parent()
    response = client.list_processors(parent=parent)

    return list(response.processors)



def get_processor(
        display_name: str,
        processors: Optional[Sequence[docai.Processor]] = None,
) -> Optional[docai.Processor]:
    if processors is None:
        processors = list_processors()
    for processor in processors:
        if processor.display_name == display_name:
            return processor
    return None




def delete_processor(processor: docai.Processor):
    client = get_client()
    operation = client.delete_processor(name=processor.name)
    operation.result()  # Wait for operation to complete

def delete_all_processors ():
    for processor in list_processors():
        print(f"  Deleting {processor.display_name}...")
        delete_processor(processor)




if (__name__ == "__main__"):
    create_all_test_processors()
    ocr_processor = get_processor (document_invoice_display_name)

    batch_process_documents(
        project_id=project_id,
        location=location,
        processor=ocr_processor,
        gcs_input_uri=gcs_input_uri,
        gcs_output_uri=gcs_output_uri,
        field_mask=field_mask,
    )