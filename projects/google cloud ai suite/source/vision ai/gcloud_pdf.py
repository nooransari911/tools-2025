import time

from google.cloud import storage
import json, os
import re
from google.cloud import vision
from google.cloud import storage

list_all_documents = []


def async_detect_document(gcs_source_uri, gcs_destination_uri, output_dir, mime_type):
    """OCR with PDF/TIFF as source files on GCS"""
    import json, os
    import re
    from google.cloud import vision
    from google.cloud import storage

    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    #mime_type = mime_type


    # How many pages should be grouped into each json output file.
    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size
    )

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config, output_config=output_config
    )

    operation = client.async_batch_annotate_files(requests=[async_request])

    print("Waiting for the operation to finish.")
    operation.result(timeout=420)




def fetch_detination (gcs_destination_uri, output_dir):

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.

    gs_url_pattern = r'gs://([^/]+)'
    match = re.match (gs_url_pattern, gcs_destination_uri)
    if match:
        bucket_name = match.group(1)
    else:
        print("No such bucket")
        exit(1)


    #prefix = match.group(2)


    storage_client = storage.Client(project="optimum-task-411411")
    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix, filtering out folders.
    blob_list = bucket.list_blobs ()

    pattern = re.compile(r'.*\.json$')
    # Filter and list files using re.match()
    all_files = [blob for blob in blob_list if pattern.match(blob.name)]





    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.

    for bucket_file in all_files:
        json_string = bucket_file.download_as_bytes().decode("utf-8")
        response = json.loads(json_string)
        pretty_json = json.dumps(response, indent=4)
        #print (pretty_json)
        file_str = ""


        try:
            te = response["responses"]

            output_dir_json = os.path.join(output_dir, "json/")
            output_file_path = os.path.join(output_dir_json, ("pdf_" + os.path.basename(bucket_file.name)))

            with open(output_file_path, 'w') as file:
                file.write(pretty_json)


            for page in response ["responses"]:
                page_text   = page ["fullTextAnnotation"] ["text"]
                page_number = page ["context"] ["pageNumber"]

                cleaned_page_text = re.sub(r'\n', ' ', page_text)

                cat = f"""
                Content of {bucket_file.name}, page {page_number}: \n {cleaned_page_text} \n
                """
                file_str = "".join ([file_str, cleaned_page_text, "\n"])
                #print (cat)
            list_all_documents.append("".join ([file_str, "\n\n\n\n"]))



        except Exception as e:
            output_file_path = os.path.join(output_dir, ("img_" + os.path.basename(bucket_file.name)))

            with open(output_file_path, 'w') as file:
                file.write(pretty_json)

            page_text = response ["text"]
            page_number = 1

            cleaned_page_text = re.sub (r'\n', ' ', page_text)

            cat = f"""
            Content of {bucket_file.name}, page {page_number}: \n {cleaned_page_text} \n
            """
            list_all_documents.append(cleaned_page_text)
            #print(cat)


    list_all_documents_path = os.path.join (output_dir, "all_documents_text.txt")

    with open(list_all_documents_path, "w") as list_file:
        for f in list_all_documents:
            list_file.write(f)





        # Here we print the full text from the first page.
        # The response contains more information:
        # annotation/pages/blocks/paragraphs/words/symbols
        # including confidence scores and bounding boxes





if __name__ == "__main__":
    time_start = time.time_ns()
    # Replace with the path to your scanned document image
    source = "gs://gcloud_pdf_intelligence/scanned_doc.pdf"
    destination = "gs://gcloud_pdf_intelligence_destination/"
    source_bucket_name = "gcloud_pdf_intelligence"
    destination_bucket_name = "gcloud_pdf_intelligence_destination"
    output_dir = "/google cloud intelligence/output files archive/"
    #async_detect_document (source, destination, output_dir)


    client = storage.Client()
    bucket = client.get_bucket (source_bucket_name)
    pattern = re.compile(r'.*\.pdf$')
    blobs = bucket.list_blobs()

    all_files = [(blob.name, blob.content_type) for blob in blobs if pattern.match(blob.name)]



    # Process each file
    for name, mime in all_files:
        source_uri = f"gs://{source_bucket_name}/{name}"
        destination_uri = f"gs://{destination_bucket_name}/"
        print (f"\n\nName: {name}, mime: {mime}")
        # Call the async document detection function for each file
        async_detect_document(source_uri, destination_uri, output_dir, mime_type=mime)
        print(f"Started processing for {name}")


    fetch_detination (destination, output_dir)


    time_end = time.time_ns()
    elapsed_time = (time_end - time_start) / (10**9)
    print (f"\n\nElapsed time is: {elapsed_time}")
