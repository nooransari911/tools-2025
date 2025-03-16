## Run on render.com
==> Uploading build...
info==> Build uploaded in 8s
info==> Build successful 🎉
info==> Deploying...
info==> Using Node version 20.15.1 (default)
info==> Docs on specifying a Node version: https://render.com/docs/node-version
info==> Using Bun version 1.1.0 (default)
info==> Docs on specifying a bun version: https://render.com/docs/bun-version
info==> Running 'gunicorn compile_image:app'
info==> No open ports detected, continuing to scan...
info==> Docs on specifying a port: https://render.com/docs/web-services#port-binding
infoDownloading stackoverflow-dev-survey-2024-technology-admired-and-desired-webframe-desire-admire-social.png 100%.
infoDownloading stackoverflow-dev-survey-2024-technology-admired-and-desired-platform-desire-admire-social.png 100%.
infoDownloading stackoverflow-dev-survey-2024-technology-admired-and-desired-database-desire-admire-social.png 100%.
infoDownloading stackoverflow-dev-survey-2024-technology-admired-and-desired-language-desire-admire-social.png 100%.
infoDownloading index_im.html 100%.
infoDownloading results_im.html 100%.
info[2024-08-05 11:40:41 +0000] [93] [INFO] Starting gunicorn 22.0.0
info[2024-08-05 11:40:41 +0000] [93] [INFO] Listening at: http://0.0.0.0:10000 (93)
info[2024-08-05 11:40:41 +0000] [93] [INFO] Using worker: sync
info[2024-08-05 11:40:41 +0000] [108] [INFO] Booting worker with pid: 108
info127.0.0.1 - - [05/Aug/2024:11:40:41 +0000] "HEAD / HTTP/1.1" 404 0 "-" "Go-http-client/1.1"
info==> Your service is live 🎉
info127.0.0.1 - - [05/Aug/2024:11:40:44 +0000] "GET / HTTP/1.1" 404 207 "-" "Go-http-client/2.0"
info['/static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-database-desire-admire-social.png', '/static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-language-desire-admire-social.png', '/static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-platform-desire-admire-social.png', '/static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-webframe-desire-admire-social.png']
info127.0.0.1 - - [05/Aug/2024:11:40:57 +0000] "GET /comm HTTP/1.1" 200 3610 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
info127.0.0.1 - - [05/Aug/2024:11:40:57 +0000] "GET /static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-language-desire-admire-social.png HTTP/1.1" 200 0 "https://tools-and-projects.onrender.com/comm" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
info127.0.0.1 - - [05/Aug/2024:11:40:57 +0000] "GET /static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-database-desire-admire-social.png HTTP/1.1" 200 0 "https://tools-and-projects.onrender.com/comm" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
info127.0.0.1 - - [05/Aug/2024:11:40:57 +0000] "GET /static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-platform-desire-admire-social.png HTTP/1.1" 200 0 "https://tools-and-projects.onrender.com/comm" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
info127.0.0.1 - - [05/Aug/2024:11:40:57 +0000] "GET /static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-webframe-desire-admire-social.png HTTP/1.1" 200 0 "https://tools-and-projects.onrender.com/comm" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"



## ~/Downloads/tools and projects/projects/compile image git:(master)±1 python3 ./compile_image.py
 * Serving Flask app 'compile_image' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:8156/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 648-332-664
['/static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-database-desire-admire-social.png', '/static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-language-desire-admire-social.png', '/static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-platform-desire-admire-social.png', '/static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-webframe-desire-admire-social.png']
127.0.0.1 - - [05/Aug/2024 14:57:58] "GET /comm HTTP/1.1" 200 -
127.0.0.1 - - [05/Aug/2024 14:57:58] "GET /static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-platform-desire-admire-social.png HTTP/1.1" 304 -
127.0.0.1 - - [05/Aug/2024 14:57:58] "GET /static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-webframe-desire-admire-social.png HTTP/1.1" 304 -
127.0.0.1 - - [05/Aug/2024 14:57:58] "GET /static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-language-desire-admire-social.png HTTP/1.1" 304 -
127.0.0.1 - - [05/Aug/2024 14:57:58] "GET /static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-database-desire-admire-social.png HTTP/1.1" 304 -
['/static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-database-desire-admire-social.png', '/static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-language-desire-admire-social.png', '/static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-platform-desire-admire-social.png', '/static/image/stackoverflow-dev-survey-2024-technology-admired-and-desired-webframe-desire-admire-social.png']
127.0.0.1 - - [05/Aug/2024 14:59:04] "POST /comm HTTP/1.1" 200 -
127.0.0.1 - - [05/Aug/2024 14:59:17] "GET /static/generated_file.docx HTTP/1.1" 200 -



## GCF
without flask.response:
   [5:04:05 PM] - Execution response:
         {
               "args":{},
               "headers":{"Host":"localhost"},
               "message":"<h1>Hello, World!</h1>
                     <h1>Status code: 200</h1>
                     <h1>Request method: GET</h1>    
                     <h1>Request path: /</h1>    
                     <h2>Request url: http://localhost/</h2>    
                     <h2>Request headers: {'Host': 'localhost'}</h2>    
                     <h2>Request args: {}</h2>",
               "method":"GET","url":"http://localhost/"
         }


with flask.response:

[5:06:27 PM] - Execution response: 
         {
               "args":{},
               "headers":{"Host":"localhost"},
               "message":"<h1>Hello, World!</h1>    
                     <h1>Status code: 200</h1>    
                     <h1>Request method: GET</h1>    
                     <h1>Request path: /</h1>    
                     <h2>Request url: http://localhost/</h2>   
                     <h2>Request headers: {'Host': 'localhost'}</h2>    
                     <h2>Request args: {}</h2>",
               "method":"GET","url":"http://localhost/"
         }



## use images from cloud storage in functions

from google.cloud import storage
from google.cloud import functions

def generate_signed_url(request):
    """Generates a signed URL for an image in Cloud Storage."""

    # Get the image name from the request
    image_name = request.args.get('image_name')

    # Create a Cloud Storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket('my-bucket-name')

    # Create a blob object for the image
    blob = bucket.blob(image_name)

    # Generate a signed URL with a 1-hour expiration
    url = blob.generate_signed_url(expiration=3600)

    # Return the signed URL
    return functions.Response(200, {'url': url})






## move images to cloud storage
from google.cloud import storage
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

# Set up Google Drive API credentials
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'path/to/your/service_account.json'  # Replace with your service account file path
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Set up Cloud Storage client
storage_client = storage.Client()
bucket_name = 'your-cloud-storage-bucket-name'  # Replace with your bucket name
bucket = storage_client.bucket(bucket_name)

# Set up Google Drive API client
drive_service = build('drive', 'v3', credentials=credentials)

def move_images_to_cloud_storage(request):
    '''
    Moves images from a public Google Drive folder to Cloud Storage.

    Args:
        request (flask.Request): The request object.
        
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
    '''

    # Get the Google Drive folder ID from the request
    folder_id = request.args.get('folder_id')

    # Get the list of files in the folder
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and mimeType='image/jpeg'",
        fields='files(id, name, mimeType)'
    ).execute()
    files = results.get('files', [])

    # Iterate through the files and upload them to Cloud Storage
    for file in files:
        # Download the file from Google Drive
        file_data = drive_service.files().get(fileId=file['id'], download=True).execute()

        # Create a Cloud Storage blob object
        blob = bucket.blob(file['name'])

        # Upload the file to Cloud Storage
        blob.upload_from_string(file_data)

        print(f"Uploaded {file['name']} to Cloud Storage.")

    return 'Images moved successfully!'

