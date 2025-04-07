
# === Contents of claude_chatbot.py ===

"""
<note>This CLI chatbot is powered by Claude 3.7 Sonnet and deployed on
AWS Bedrock, offering three distinct interaction modes. In Pure Text
Interaction mode, users engage in a standard text-based chat interface
directly with the AI. Image Context Mode allows users to load images
from a specified directory as context for the conversation, followed
by a pure text chat interface. File Context Mode enables users to
provide a directory path containing files. The user also provides a
file path for the initial launch prompt. The chatbot ingests files
from the specified directory, performs an API call using the prompt,
writes the initial response to a user-specified output file, and then
continues the conversation in a pure text chat interface.</note>
"""

import os, io
import sys
import time
import readline

import base64, json, pprint
import humanize



import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
load_dotenv("/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/.env")  # Load environment variables first




ROLE_ARN="arn:aws:iam::677276075874:role/AWSBedrockFullAccesstoLambdaRole"
S3_SRC = os.getenv ("S3_SOURCE_BUCKET")
INPUT_JSONL_FILE_NAME = os.getenv ("INPUT_JSONL_FILE_NAME")
S3_DEST = os.getenv ("S3_DESTINATION_BUCKET")
OUTPUT_JSONL_FILE_NAME = os.getenv ("OUTPUT_JSONL_FILE_NAME")







def load_system_instructions():
    instructions_file_path = os.getenv('SYSTEM_INSTRUCTIONS_PATH')
    if instructions_file_path:
        try:
            with open(instructions_file_path, 'r') as file:
                # print ("can read sys instruct")
                return [
                    {
                        "type": "text",
                        "text": file.read()
                    }
                ]  # Bedrock expects a list of dicts
        except Exception as e:
            print(f"Error reading system instructions: {e}")
    return [{"text": ""}]  # Return a default empty instruction if not found




def assume_role(role_arn, session_name):
    """
    Assumes the specified IAM role and returns temporary credentials.

    Args:
        role_arn (str): The ARN of the IAM role to assume.
        session_name (str): The name of the session.

    Returns:
        dict: Temporary credentials (AccessKeyId, SecretAccessKey, SessionToken).
    """
    sts_client = boto3.client('sts')

    try:
        response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=session_name
        )
        credentials = response['Credentials']
        return credentials
    except ClientError as e:
        logger.error(f"Failed to assume role: {e}")
        raise





def configure_bedrock_runtime():
    """Configures and returns the Bedrock runtime client."""

    # Load .env, but don't require it (AWS credentials might be configured differently)
    load_dotenv()

    # Use environment variables if available, otherwise let boto3 use default credential chain
    region_name = os.getenv("AWS_REGION_NAME")  # Or use a default region like "us-east-1"
    # Access key and secret key are not needed if IAM roles or profiles are properly configured.

    # Bedrock config.  Crucial for long generation tasks.
    custom_config = Config(
        connect_timeout=840,
        read_timeout=840,
        region_name=region_name,  # Always a good idea to specify the region
        #  retries = {  # Optional: Configure retry behavior
        #      'max_attempts': 5, # Example: Retry up to 5 times.
        #      'mode': 'standard'
        #  }
    )
    try:
        role_arn = "arn:aws:iam::677276075874:role/AWSBedrockFullAccesstoLambdaRole"  # Replace with your role ARN
        session_name = "DeepseekR1Session"
        credentials = assume_role (role_arn, session_name)

        # Create a Bedrock client using the temporary credentials
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )
        return bedrock_runtime
    except Exception as e:
        print(f"Error creating Bedrock runtime: {e}")
        print("Check your AWS credentials and region configuration.")
        sys.exit(1)  # Exit, as we can't proceed without a client


def configure_bedrock(session_name="DeepseekR1Session"):
    """Configures and returns the Bedrock runtime."""

    # Load .env, but don't require it (AWS credentials might be configured differently)
    load_dotenv()

    # Use environment variables if available, otherwise let boto3 use default credential chain
    region_name = os.getenv("AWS_REGION_NAME")  # Or use a default region like "us-east-1"
    # Access key and secret key are not needed if IAM roles or profiles are properly configured.

    # Bedrock config.  Crucial for long generation tasks.
    custom_config = Config(
        connect_timeout=840,
        read_timeout=840,
        region_name=region_name,  # Always a good idea to specify the region
        #  retries = {  # Optional: Configure retry behavior
        #      'max_attempts': 5, # Example: Retry up to 5 times.
        #      'mode': 'standard'
        #  }
    )
    try:
        role_arn = "arn:aws:iam::677276075874:role/AWSBedrockFullAccesstoLambdaRole"  # Replace with your role ARN
        credentials = assume_role (role_arn, session_name)

        # Create a Bedrock using the temporary credentials
        bedrock = boto3.client (
            service_name='bedrock',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )
        return bedrock
    except Exception as e:
        print(f"Error creating Bedrock: {e}")
        print("Check your AWS credentials and region configuration.")
        sys.exit(1)  # Exit, as we can't proceed without a







def load_directory_files(directory_path):
    """
    Load all text files from a directory and combine them into a single string.
    Each file is separated by a clear delimiter.
    
    Args:
        directory_path (str): Path to the directory containing text files
        
    Returns:
        str: Combined content of all files with delimiters
    """
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory")
        return None
        
    combined_content = ""
    file_count = 0
    
    # Define common text file extensions to prioritize
    text_extensions = ['.txt', '.md', '.html', '.xml', '.json', '.csv', 
                       '.log', '.py', '.js', '.css', '.yaml', '.yml', 
                       '.cfg', '.ini', '.sh', '.bat', '.tex']
    
    try:
        for filename in sorted(os.listdir(directory_path)):
            file_path = os.path.join(directory_path, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
            
            # Try to determine if it's a text file
            try:
                # Check extension first
                _, file_extension = os.path.splitext(filename)
                is_likely_text = file_extension.lower() in text_extensions
                
                # If not a known extension, check content
                if not is_likely_text:
                    try:
                        with open(file_path, 'rb') as test_file:
                            # Read first KB to detect if it's binary
                            chunk = test_file.read(1024)
                            # If NUL char is present, likely binary
                            if b'\x00' in chunk:
                                continue
                            # Try decoding - if it works, probably text
                            chunk.decode('utf-8')
                            is_likely_text = True
                    except UnicodeDecodeError:
                        # Not valid UTF-8 text
                        continue
                
                # If it passed our checks, try to read it
                if is_likely_text:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()
                        
                    # Add file delimiter with name and separator
                    file_delimiter = f"\n\n{'='*50}\n"
                    file_delimiter += f"FILE: {filename}\n"
                    file_delimiter += f"{'='*50}\n\n"
                    
                    combined_content += file_delimiter + file_content
                    file_count += 1
                    
            except Exception as e:
                print(f"Skipping {filename}: {e}")
                continue
                
        if file_count > 0:
            print(f"Successfully loaded {file_count} text files from {directory_path}")
            return combined_content
        else:
            print(f"No readable text files found in {directory_path}")
            return None
            
    except Exception as e:
        print(f"Error reading directory {directory_path}: {e}")
        return None




def load_image (dir: str, batch_size = None):
    """Load batch_size base-64-encoded images from dir into content[] List"""
    content = []
    
    
    if not os.path.isdir (dir):
        print (f"Error: Provided path is not a dir;")
        return None

    
    # Define text file extensions to process
    image_extensions = ('jpg', 'jpeg', 'png', 'gif')


    for i, path in enumerate (os.listdir (dir)):
        full_path = os.path.join (dir, path)
        
        if os.path.isdir (full_path):
            continue

        if not full_path.endswith (image_extensions):
            continue

        try:
            print (full_path)
            with open (full_path, 'rb') as image:
                # base64_image = base64.b64encode (image.read ())
                base64_image = base64.b64encode (image.read ()).decode ('utf-8')

                image_size = round (sys.getsizeof (base64_image)/1000)



                # print (f"Type of image: {type (base64_image)}KB")
                print (f"Size of image: {image_size}KB\n\n")



                ext = full_path.split ('.') [-1]

                if ext.lower () == "jpg":
                    ext = "jpeg"
                mime_type = f"image/{ext}".lower ()




                content.append (prepare_message_with_data (base64_image, "image", mime_type))


        except Exception as e:
            print (f"An exception occured for {full_path}: {e}")
            

    if batch_size is not None:
        return content [:batch_size]

    else:
        # print (content)
        return content






def load_files_base64 (dir: str, extensions: tuple = ('jpg', 'jpeg', 'png', 'gif'), batch_size: int = None):
    """Load batch_size base-64-encoded files from dir into content[] List"""
    content = []
    
    
    if not os.path.isdir (dir):
        print (f"Error: Provided path is not a dir;")
        return None

    
    # Define text file extensions to process


    for i, path in enumerate (os.listdir (dir)):
        full_path = os.path.join (dir, path)
        
        if os.path.isdir (full_path):
            continue

        if not full_path.endswith (extensions):
            continue

        try:
            print (full_path)
            with open (full_path, 'rb') as file:
                # base64_image = base64.b64encode (image.read ())
                base64_file: bytes = base64.b64encode (file.read ()).decode ('utf-8')

                file_size = round (sys.getsizeof (base64_file)/1000)



                # print (f"Type of image: {type (base64_image)}KB")
                print (f"Size of file: {file_size}KB\n\n")



                ext = full_path.split ('.') [-1]

                if ext.lower () == "jpg":
                    ext = "jpeg"


                mime_type = f"image/{ext}".lower ()




                content.append (prepare_message_with_data (base64_file, "image", mime_type))


        except Exception as e:
            print (f"An exception occured for {full_path}: {e}")
            

    if batch_size is not None:
        return content [:batch_size]

    else:
        # print (content)
        return content












def prepare_message(text_string, role="user"):
    """Formats a text string for Claude Messages."""
    return {
        "role": role,
        "content": [
            {
                "type": "text",
                "text": text_string
            }
        ]
    }








def prepare_message_with_data (data, type_string, mime_type):
    """Format a message that includes base64 encoded data"""
    return {
        "type": type_string,
        "source": {
            "type": "base64",
            "media_type": mime_type,
            "data": data
        }
    }









def prepare_message_with_file(user_message, file_content):
    """Format a message that includes text file content according to DeepSeek R1 API requirements"""
    # Create a formatted message that includes both the user's query and the file content
    combined_message = f"{user_message}\n\n\n\nDocument content:\n{file_content}"
    
    return {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": combined_message
            }
        ]
    }






def generate_response(bedrock_runtime, model_id, system_prompts, messages, max_op_tokens=131072, thinking_tokens=16000, thinking_en: bool = None):
    """
    Sends messages to Claude and handles the response.
    """

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_op_tokens,
            "system": system_prompts,
            "messages": messages
        }
    )




    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=body
        )
        # print ((response.items ()))
        response ["body"] = json.loads (
            response.get ("body").read ().decode ("utf-8")
        )


        response_body = response.get ("body")
        token_usage = response_body ['usage']

        # print ("Entire response dump: ")
        # print (json.dumps (response, indent = 4))
        # print (json.dumps (response_body, indent = 4))




        print(f"\nInput tokens: {token_usage     ['input_tokens']:<15}")
        print(f"Output tokens:  {token_usage     ['output_tokens']}")
        print(f"Stop reason:    {response_body   ['stop_reason']}")

        raw_content = response_body ['content']
        output_message = []


        
        for content in raw_content:
            if content ["type"].lower () == "text":
                output_message.append (content ["text"])
            else:
                continue

        return_string = "".join (output_message)
        
        print (f"Size of response: {sys.getsizeof (return_string)}B")

        return return_string


        # response_body = json.loads(response.get('body').read())
   
        # return response_body



    except ClientError as e:
        print(f"AWS client error: {e}")
        # Handle specific error codes if you can do something about them
        if e.response['Error']['Code'] == 'ThrottlingException':
            print("Request was throttled. Consider waiting and retrying.")
        elif e.response['Error']['Code'] == 'ValidationException':
             print("Check the request format and parameters.")
        return None  # Or raise, depending on your needs

    except Exception as e:  # Catch *any* other exception
        print(f"An unexpected error occurred: {e}")
        return None  # Or raise, if you want to stop the program on unhandled errors


def run_chatbot():
    """Main chatbot loop."""
    load_dotenv()  # Load environment variables first
    images_dir = "../../img"
    files_dir  = "../../files"
    role_arn = "arn:aws:iam::677276075874:role/AWSBedrockFullAccesstoLambdaRole"  # Replace with your role ARN
    session_name = "Claude37SonnetSession"
    credentials = assume_role (role_arn, session_name)

    bedrock_runtime = configure_bedrock_runtime ()
    bedrock = configure_bedrock ()
    # files_string = load_directory_files ("./files/")

    # print (bedrock.list_foundation_models ())
    # print (bedrock.get_foundation_model (modelIdentifier="deepseek.r1-v1:0"))





    model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0" 
    system_prompts = load_system_instructions()
    messages = []  # Initialize conversation history
    content = []


    num_args = len(sys.argv)
    if num_args >= 2 and sys.argv[1] == "im":
        initial_prompt_string = "this is the first prompt. this is used to provide images to you. tell me how many images do you see. don't tell me anything else"
        initial_prompt = {
            "type": "text",
            "text": initial_prompt_string
        }
        content = load_image (images_dir)
        # print (type (content))
        # print ((system_prompts))


        content.append (initial_prompt)
        # print (len (content))




        initial_message = {
            "role": "user",
            "content": content
        }
        # print (initial_message)

        messages.append (initial_message)
        initial_response = generate_response (bedrock_runtime, model_id, system_prompts, messages)
        # print ("\n\nResponse body dump: ")
        # print (json.dumps (initial_response, indent = 4))
    
        print (initial_response)
        print ("\n\n")




    if num_args >= 2 and sys.argv[1] == "file":
        print("Prompt from file mode;\n")
        prompt_file_path = sys.argv[2]
        text_path = sys.argv[3]  # Can be file or directory
        output_file_path = sys.argv[4]
        should_print = sys.argv[5] if len(sys.argv) > 5 else "no print"  # Default to False if not provided



        # Validate prompt file
        if not os.path.isfile(prompt_file_path):
            print(f"No such file as {prompt_file_path}\n\n")
            sys.exit(1)
    
        # Validate text path exists
        if not os.path.exists(text_path):
            print(f"No such file or directory as {text_path}\n\n")
            sys.exit(1)
    
        if output_file_path is None:
            print(f"No output file path provided\n\n")
            sys.exit(1)

        # Load prompt file
        with open(prompt_file_path, "r") as prompt_file:
            prompt_file_string = prompt_file.read()
            prompt_file_message = prepare_message(prompt_file_string, "user")
            messages.append(prompt_file_message)
    
        # Process text path - check if it's a file or directory
        if os.path.isfile(text_path):
            # Process as a single file
            with open(text_path, "r") as text_file:
                text_content = text_file.read()
            text_file_string = f"Text file: {os.path.basename(text_path)}\n\n{text_content}"
    
        elif os.path.isdir(text_path):
            # Process as a directory
            text_content = load_directory_files(text_path)
            if text_content is None:
                print(f"Failed to load content from directory {text_path}")
                sys.exit(1)
            text_file_string = f"Directory content from: {text_path}\n\n{text_content}"
    
        text_file_message = prepare_message(text_file_string, "user")
        messages.append(text_file_message)
    
        # Generate and process response
        prompt_file_response = generate_response(bedrock_runtime, model_id, system_prompts, messages)
        print(f"Size of response: {sys.getsizeof(prompt_file_response)}B")
        print("\n\n")
    
        messages.append(prepare_message(prompt_file_response, "assistant"))  # Add AI response to history
    
        # Output response
        if should_print.lower() == "print":
            print("\n\n", prompt_file_response, "\n\n")
    
        with open(output_file_path, "w") as output_file:
            output_file.write(prompt_file_response)




    print("\033[92mChatbot started. Type 'exit' to quit or press Ctrl+D.\033[0m")

    while True:
        try:
            user_input = input("\033[94mYou: \033[0m")

            if user_input.lower() == 'exit':
                print("\033[92mChatbot exiting.\033[0m")
                break

            if user_input:
                # messages.append(prepare_message_with_file (user_input, files_string))  # Add user message to history
                # print (user_input)
                # print (json.dumps (prepare_message (user_input, "user")))
                messages.append (prepare_message (user_input, "user"))  # Add user message to history
                start_time = time.time()
                response_message = generate_response(bedrock_runtime, model_id, system_prompts, messages)
                end_time = time.time()



                if response_message:
                    messages.append (prepare_message (response_message, "assistant")) #add ai response to history
                    elapsed_time = end_time - start_time
                    # Print the text content of the response

                    print (f"\n\033[91mChatbot ({elapsed_time:.2f}s):\033[0m\n{response_message}\n\n\n\n")

        except KeyboardInterrupt:
            print("^C")
            user_input = ""
            readline.insert_text('')  # Clear input buffer
            continue  # Go back to the start of the loop

        except EOFError:  # Ctrl+D
            print("\n\033[92mChatbot exiting.\033[0m")
            sys.exit (0)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")  # Catch-all for other errors
            continue




# def dev_main ():
#     load_image ('./img')







if __name__ == "__main__":
    # dev_main ()
    run_chatbot()



# === Contents of claude_batch_inference.py ===

"""
<note>This CLI tool provides batch inference capabilities with Claude
3.5 Sonnet on AWS Bedrock, supporting multiple operational modes. List
mode allows users to view all batch inference jobs, displaying their
names and statuses. Load mode accepts a user prompt file and a
directory of files to process, preparing a job file with model inputs
for batch inference and uploading it to an S3 bucket. Fetch mode
enables downloading produced files from the S3 bucket. Clean mode
processes the downloaded file to extract the actual model response and
write it to a specified file. Dev mode provides development-specific
functionality, while main mode allows users to submit and start batch
inference jobs.</note>
"""

from datetime import datetime
import re

from claude_chatbot import *
import latest_job_file 
import secrets
import ast

load_dotenv("/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/.env")  # Load environment variables first





"""
Get 100 dummy files:
for i in {1..100}; do
    echo "this is a dummy file; ignore it;" > "dummy-file-$i.txt"
done
"""



def aws_encoder(obj):
    # Handle datetime objects
    if isinstance(obj, datetime):
        return obj.isoformat()
    
    # Handle Decimal objects (common in DynamoDB responses)
    if isinstance(obj, Decimal):
        return float(obj) if obj % 1 else int(obj)
    
    # Handle binary data - properly using read() and decode() for file-like objects
    if hasattr(obj, 'read') and callable(obj.read):
        try:
            return obj.read().decode('utf-8')
        except:
            # Fall back to reading as bytes if decode fails
            obj.seek(0)  # Reset position
            return str(obj.read())
    
    # Handle binary/bytes data directly
    if isinstance(obj, bytes):
        try:
            return obj.decode('utf-8')
        except UnicodeDecodeError:
            # If it can't be decoded as UTF-8, it's probably not text
            return str(obj)
    
    # Handle sets (used by DynamoDB)
    if isinstance(obj, set):
        return list(obj)
    
    # Handle objects with __dict__ attribute (custom response objects)
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    
    # Let the error bubble up with a helpful message
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")





def prepare_model_request (anthropic_version, system_prompts, messages, max_op_tokens=131072):
    return {
        "anthropic_version": anthropic_version,
        "max_tokens": max_op_tokens,
        "system": system_prompts,
        "messages": messages
    }



def prepare_job_record (request):
    return {
        "recordId": f"RECORD-ID-{secrets.token_hex (16)}",
        "modelInput": request
    }








def prepare_input_jsonl_file (prompt, dir, model_id, system_prompts, max_op_tokens=131072, extensions: tuple = ('txt', 'md')):
    list_json_obj = []
    one_jsonl_messages = []






    if not os.path.isdir (dir):
        print (f"Error: Provided path is not a dir;")
        return None

    
    # Define text file extensions to process


    for i, path in enumerate (os.listdir (dir)):
        full_path = os.path.join (dir, path)
        
        if os.path.isdir (full_path):
            continue

        if not full_path.endswith (extensions):
            continue

        try:
            # print (full_path)
            
            with open (full_path, 'r') as file:
                file_string = file.read ()

                file_message   = prepare_message (file_string, "user")
                prompt_message = prepare_message (prompt, "user")
                one_jsonl_messages.append (file_message)
                one_jsonl_messages.append (prompt_message)

                one_file_request = prepare_model_request (
                    anthropic_version="bedrock-2023-05-31",
                    system_prompts=system_prompts,
                    messages=one_jsonl_messages,
                    max_op_tokens=max_op_tokens
                )

                one_file_record = prepare_job_record (one_file_request)
                # print (json.dumps (one_file_record, indent=4))

                list_json_obj.append (one_file_record)
                # print ("")
                one_jsonl_messages = []
                # print (json.dumps (list_json_obj, indent=4))

                
        except Exception as e:
            print (f"An exception occured for {full_path}: {e}")



    s3_head_op = create_and_upload_jsonl (list_json_obj, ROLE_ARN)

    # Construct the S3 URI
    s3_uri = f"s3://{S3_SRC}/{INPUT_JSONL_FILE_NAME}"
    
    # Check if S3 operation was successful
    is_success, response = s3_head_op

    if is_success:
        # Extract key information from successful response
        accept_ranges          =    response ["AcceptRanges"]
        last_modified          =    response ["LastModified"]
        content_length         =    response ["ContentLength"]
        etag                   =    response ["ETag"]
        content_type           =    response ["ContentType"]
        server_side_encryption =    response ["ServerSideEncryption"]
        metadata               =    response ["Metadata"]

        # Print the most important information
        print(f"\n{'S3 URI:':<15} {s3_uri}"
              f"\n{'Size:':<15} {content_length} bytes"
              f"\n{'Type:':<15} {content_type}"
              f"\n{'Last Modified:':<15} {last_modified.isoformat()}"
              f"\n{'ETag:':<15} {etag}")



    else:
        # Handle error case
        error_message = response
        print(f"\nFailed to upload to: {s3_uri}"
              f"\nError: {error_message}")
    
    return list_json_obj




def create_jsonl_file(data_list):
    """
    (Deprecated) Takes a list and creates a JSONL file where each line is an element from the list.
    
    Args:
        data_list (list): List of objects that can be serialized to JSON
        
    Returns:
        str: Path to the created JSONL file
    """


    global INPUT_JSONL_FILE_NAME


    
    try:
        with open(INPUT_JSONL_FILE_NAME, 'w', encoding='utf-8') as file:
            for item in data_list:
                # Convert each item to a JSON string and write to file with newline
                json_line = json.dumps(item)
                file.write(json_line + '\n')

        with open(INPUT_JSONL_FILE_NAME, 'r', encoding='utf-8') as file:
            print(f"\nSuccessfully created JSONL file: {INPUT_JSONL_FILE_NAME} of size {sys.getsizeof (file.read ())}B")


        return INPUT_JSONL_FILE_NAME
    
    except Exception as e:
        print(f"Error creating JSONL file: {e}")
        return None




def create_and_upload_jsonl(data_list, role_arn):
    """
    Takes a list, creates an in-memory JSONL file, and uploads it to S3.
    
    Args:
        data_list (list): List of objects that can be serialized to JSON
        
    Returns:
        tuple: (bool, str) - (success status, S3 URI or error message)
    """
    try:
        # Create an in-memory byte stream
        buffer = io.BytesIO()
        
        # Write JSON lines to the buffer
        for item in data_list:
            json_line = json.dumps(item)
            buffer.write((json_line + '\n').encode('utf-8'))
        
        # Get buffer size and reset position to beginning
        buffer_size = buffer.tell()
        buffer.seek(0)
        



        
        assume_role (role_arn, "ClaudeS3Session")
        s3_client = boto3.client('s3')
        s3_put_op = s3_put_operation (
            S3Client=s3_client,
            role_arn=ROLE_ARN,
            data=buffer.getvalue ()
        )

        return s3_put_op

        
    except Exception as e:
        error_msg = f"Error creating/uploading JSONL file: {e}"
        print(error_msg)
        return False, error_msg










def extract_text_from_jsonl(input_file_path, output_file_path):
    """
    Processes a JSONL file containing model interactions and extracts only the regular text output.
    
    Args:
        input_file_path (str): Path to the input JSONL file
        output_file_path (str): Path to save the output file
    
    Returns:
        int: Number of records processed
    """
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"Input file not found: {input_file_path}")
    
    record_count = 0
    
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
        for line in infile:
            try:
                # Parse the JSONL line
                record = json.loads(line.strip())
                record_id = record.get("recordId", "unknown")
                
                # Extract model output
                model_output = record.get("modelOutput", {})
                
                # Extract text content from the response similar to your generate_response function
                output_text = []
                
                # Check if the response has the expected structure
                if "content" in model_output and isinstance(model_output["content"], list):
                    for content in model_output["content"]:
                        if content.get("type", "").lower() == "text":
                            output_text.append(content.get("text", ""))
                
                # Join all text content
                full_text = "".join(output_text)

                # Check if "dummy" (case-insensitive) does NOT exist in full_text
                if not re.search(r"dummy", full_text, re.IGNORECASE):
                    # Write the extracted text to the output file with record ID ONLY if "dummy" is not found.
                    outfile.write(f"{record_id} :  {full_text}\n\n\n\n")
                    record_count += 1  # Increment only if written


                
            except json.JSONDecodeError:
                print(f"Error parsing JSON in line: {line[:100]}...")
                continue
            except Exception as e:
                print(f"Error processing record: {str(e)}")
                continue
    
    print(f"Processed {record_count} records from {input_file_path}")
    print(f"Extracted text saved to {output_file_path}")
    
    return record_count





def s3_put_operation (S3Client, role_arn, data):
    """Execute S3 Put operation on data; Returns (Success?True:False, Head_Object)"""
    # Create test data
    # buffer = io.BytesIO(data)
    
    try:
        # assume_role (role_arn, "ClaudeS3Session")
        # s3_client = boto3.client('s3')
        s3_put_op = S3Client.put_object(
            Bucket=S3_SRC,
            Key=INPUT_JSONL_FILE_NAME,
            Body=data
        )
        s3_head_op = S3Client.head_object(
            Bucket=S3_SRC,
            Key=INPUT_JSONL_FILE_NAME
        )

        
        return (True, s3_head_op)

    except Exception as e:
        error_msg = f"PutObject verification failed: {e}"
        print(error_msg)
        return (False, error_msg)





def list_batch_inference_jobs (BedrockClient, All: bool, JobArn=None):
    if All == False:
        jobs = BedrockClient.get_model_invocation_job (jobIdentifier=JobArn)['status']

    else:
        jobs = BedrockClient.list_model_invocation_jobs ()

    # jobs ["invocationJobSummaries"] = json.loads (
        # jobs.get ("invocationJobSummaries").read ().decode ("utf-8")
        # jobs.get ("invocationJobSummaries")
    # )

    # jobs = ast.literal_eval(jobs.get ("invocationJobSummaries"))

    job_summaries = []

    for job in jobs.get ("invocationJobSummaries"):
    #     job_obj = ast.literal_eval(jobs.get ("invocationJobSummaries"))
        job_summaries.append({
            "jobName": job ["jobName"],
            "status":  job ["status"]
        })

    for job in job_summaries:
        print(f"{job['jobName']} :  {job['status']}")




    # print (jobs, "\n\n\n\n")
    # print (type (jobs))
    # print (type (jobs.get ("invocationJobSummaries")))
    # print (jobs.get ("invocationJobSummaries"))
    # print (json.dumps (jobs, indent=4))

    return jobs








def submit_batch_inference_job (BedrockClient, InputDataConfig, OutputDataConfig, IAMRole, ModelID, JobName):
    """Submit a batch inference job to bedrock"""




    response=BedrockClient.create_model_invocation_job(
        roleArn=IAMRole,
        modelId=ModelID,
        jobName=JobName,
        inputDataConfig=InputDataConfig,
        outputDataConfig=OutputDataConfig
    )

    jobArn = response.get('jobArn')
   
    BedrockClient.get_model_invocation_job(jobIdentifier=jobArn)['status']


    return jobArn







def jobs_status ():

    system_prompts = load_system_instructions()
    session_name = "Claude37SonnetSession"
    bedrock = configure_bedrock ()
    role_arn = "arn:aws:iam::677276075874:role/AWSBedrockFullAccesstoLambdaRole"
    credentials = assume_role (role_arn, session_name)



    # records = prepare_input_jsonl_file (
    #     prompt="say hi",
    #     dir="./files",
    #     system_prompts=system_prompts,
    #     model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    # )


    # create_jsonl_file (records)


    list_batch_inference_jobs (bedrock, All=True)




def load_mode ():

    load_dotenv()  # Load environment variables first
    system_prompts = load_system_instructions()

    prompt_file_path = sys.argv [2]
    source_files     = sys.argv [3]
    if not os.path.isfile(prompt_file_path):
        print(f"No such file as {prompt_file_path}\n\n")
        sys.exit(1)

    if not os.path.isdir (source_files):
        print(f"No such dir as {source_files}\n\n")
        sys.exit(1)

    with open(prompt_file_path, "r") as prompt_file:
        prompt_file_string = prompt_file.read()


    num_args = len(sys.argv)
    records = prepare_input_jsonl_file (
        prompt=prompt_file_string,
        dir=source_files,
        system_prompts=system_prompts,
        model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    )


    create_jsonl_file (records)

    # print ("\n\nLoaded JSONL File")
    sys.exit (0)








def dev_main ():
    global ROLE_ARN
    pass
    test_s3_put_operation (ROLE_ARN)
    # extract_text_from_jsonl ("./BedrockJobSrc.jsonlv1.out", "./BedrockJobOutv1.txt")










def main ():
    """Main function"""
    global S3_SRC, S3_DEST, INPUT_JSONL_FILE_NAME, OUTPUT_JSONL_FILE_NAME

    
    load_dotenv()  # Load environment variables first
    system_prompts = load_system_instructions()













    role_arn = "arn:aws:iam::677276075874:role/AWSBedrockFullAccesstoLambdaRole"
    session_name = "Claude37SonnetSession"
    # credentials = assume_role (role_arn, session_name)
    # bedrock = boto3.client(service_name="bedrock")


    # images_dir = "./img"
    # files_dir = "./files"
    # session_name = "Claude37SonnetSession"
    # credentials = assume_role (role_arn, session_name)


    # bedrock_runtime = configure_bedrock_runtime ()
    bedrock = configure_bedrock ()


    # system_prompts = load_system_instructions()
    # messages = []  # Initialize conversation history
    # content = []


    # num_args = len(sys.argv)




            


    service_role_arn = "arn:aws:iam::677276075874:role/AWSBedrockServiceRole"
    model_id = "arn:aws:bedrock:us-west-2:677276075874:inference-profile/us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    job_name = f"InferenceJob-{datetime.now().isoformat().replace(':', '-').replace('.', '-')}"

    input_data_config=({
        "s3InputDataConfig": {
            "s3Uri": f"s3://{S3_SRC}/{INPUT_JSONL_FILE_NAME}"
        }
    })

    output_data_config=({
        "s3OutputDataConfig": {
            "s3Uri": f"s3://{S3_DEST}/"
        }
    })


    JobArn = submit_batch_inference_job (
        BedrockClient=bedrock,
        IAMRole=service_role_arn,
        ModelID=model_id,
        JobName=job_name,
        InputDataConfig=input_data_config,
        OutputDataConfig=output_data_config
    )

    list_batch_inference_jobs (bedrock, All=True)


    









def print_help():
    print("Usage:")
    print("    python3 script.py list")
    print("        List jobs status\n")
    print("    python3 script.py load ./prompt file")
    print("        Load data from regular files (text) into batch inference job input file with prompt from prompt file")
    print("    python3 script.py fetch") 
    print("        Fetch the latest job output file from S3")
    print("    python3 script.py clean <input_file> <output_file>")
    print("        Load data from batch inference job output file into human-readable text file\n")
    print("    python3 script.py dev")
    print("        Run in development mode\n")
    print("    python3 script.py help")
    print("        Show this help message\n")  # Consistent indentation
    print("    (No arguments)")
    print("        Run the main program\n")




if __name__ == "__main__":
    num_args = len(sys.argv)
    if num_args >= 2 and sys.argv[1] == "list":
        jobs_status()
    elif num_args >= 2 and sys.argv[1] == "load":
        load_mode()
    elif num_args >= 2 and sys.argv[1] == "fetch":
        latest_job_file.DownloadLatestS3FileMain ()
    elif num_args >= 4 and sys.argv[1] == "clean":
        extract_text_from_jsonl(sys.argv[2], sys.argv[3])
    elif num_args >= 2 and sys.argv[1] == "dev":
        dev_main()
    elif num_args >= 2 and (sys.argv[1] == "help" or sys.argv[1] == "-h" or sys.argv[1] == "--help"): #added this
        print_help()
    else:
        main() #changed this to call main by default



# === Contents of deepseek_chatbot.py ===

"""
<note>A basic CLI chatbot that uses Deepseek R1 on AWS Bedrock.</note>
"""

import os
import sys
import time
import readline
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
load_dotenv ("/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/.env")



def load_system_instructions():
    instructions_file_path = os.getenv('SYSTEM_INSTRUCTIONS_PATH')
    if instructions_file_path:
        try:
            with open(instructions_file_path, 'r') as file:
                return [{"text": file.read()}]  # Bedrock expects a list of dicts
        except Exception as e:
            print(f"Error reading system instructions: {e}")
    return [{"text": ""}]  # Return a default empty instruction if not found




def assume_role(role_arn, session_name):
    """
    Assumes the specified IAM role and returns temporary credentials.

    Args:
        role_arn (str): The ARN of the IAM role to assume.
        session_name (str): The name of the session.

    Returns:
        dict: Temporary credentials (AccessKeyId, SecretAccessKey, SessionToken).
    """
    sts_client = boto3.client('sts')

    try:
        response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=session_name
        )
        credentials = response['Credentials']
        return credentials
    except ClientError as e:
        logger.error(f"Failed to assume role: {e}")
        raise





def configure_bedrock_runtime():
    """Configures and returns the Bedrock runtime client."""

    # Load .env, but don't require it (AWS credentials might be configured differently)
    load_dotenv()

    # Use environment variables if available, otherwise let boto3 use default credential chain
    region_name = os.getenv("AWS_REGION_NAME")  # Or use a default region like "us-east-1"
    # Access key and secret key are not needed if IAM roles or profiles are properly configured.

    # Bedrock config.  Crucial for long generation tasks.
    custom_config = Config(
        connect_timeout=840,
        read_timeout=840,
        region_name=region_name,  # Always a good idea to specify the region
        #  retries = {  # Optional: Configure retry behavior
        #      'max_attempts': 5, # Example: Retry up to 5 times.
        #      'mode': 'standard'
        #  }
    )
    try:
        role_arn = "arn:aws:iam::677276075874:role/AWSBedrockFullAccesstoLambdaRole"  # Replace with your role ARN
        session_name = "DeepseekR1Session"
        credentials = assume_role (role_arn, session_name)

        # Create a Bedrock client using the temporary credentials
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )
        return bedrock_runtime
    except Exception as e:
        print(f"Error creating Bedrock runtime: {e}")
        print("Check your AWS credentials and region configuration.")
        sys.exit(1)  # Exit, as we can't proceed without a client


def configure_bedrock():
    """Configures and returns the Bedrock runtime."""

    # Load .env, but don't require it (AWS credentials might be configured differently)
    load_dotenv()

    # Use environment variables if available, otherwise let boto3 use default credential chain
    region_name = os.getenv("AWS_REGION_NAME")  # Or use a default region like "us-east-1"
    # Access key and secret key are not needed if IAM roles or profiles are properly configured.

    # Bedrock config.  Crucial for long generation tasks.
    custom_config = Config(
        connect_timeout=840,
        read_timeout=840,
        region_name=region_name,  # Always a good idea to specify the region
        #  retries = {  # Optional: Configure retry behavior
        #      'max_attempts': 5, # Example: Retry up to 5 times.
        #      'mode': 'standard'
        #  }
    )
    try:
        role_arn = "arn:aws:iam::677276075874:role/AWSBedrockFullAccesstoLambdaRole"  # Replace with your role ARN
        session_name = "DeepseekR1Session"
        credentials = assume_role (role_arn, session_name)

        # Create a Bedrock using the temporary credentials
        bedrock = boto3.client (
            service_name='bedrock',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )
        return bedrock
    except Exception as e:
        print(f"Error creating Bedrock: {e}")
        print("Check your AWS credentials and region configuration.")
        sys.exit(1)  # Exit, as we can't proceed without a







def load_directory_files(directory_path):
    """
    Load all text files (.txt, .md) from a directory and combine them into a single string.
    Each file is separated by a clear delimiter.
    
    Args:
        directory_path (str): Path to the directory containing text files
        
    Returns:
        str: Combined content of all files with delimiters
    """
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory")
        return None
        
    combined_content = ""
    file_count = 0
    
    # Define text file extensions to process
    text_extensions = ['.txt', '.md']
    
    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            # Skip directories and non-text files
            if os.path.isdir(file_path):
                continue
                
            # Check if file has a text extension
            _, file_extension = os.path.splitext(filename)
            if file_extension.lower() not in text_extensions:
                continue
                
            # Try to read the file as text
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                    
                # Add file delimiter with name and separator
                file_delimiter = f"\n\n{'='*50}\n"
                file_delimiter += f"FILE: {filename}\n"
                file_delimiter += f"{'='*50}\n\n"
                
                combined_content += file_delimiter + file_content
                file_count += 1
                    
            except Exception as e:
                print(f"Skipping {filename}: {e}")
                continue
                
        if file_count > 0:
            print(f"Successfully loaded {file_count} files from {directory_path}")
            return combined_content
        else:
            print(f"No readable text files found in {directory_path}")
            return None
            
    except Exception as e:
        print(f"Error reading directory {directory_path}: {e}")
        return None




def prepare_message_with_file(user_message, file_content):
    """Format a message that includes file content according to DeepSeek R1 API requirements"""
    # Create a formatted message that includes both the user's query and the file content
    combined_message = f"{user_message}\n\n\n\nDocument content:\n{file_content}"
    
    return {
        "role": "user",
        "content": [{"text": combined_message}]
    }




def prepare_message(user_input):
    """Formats user input for the Bedrock API."""
    return {
        "role": "user",
        "content": [{"text": user_input}]
    }





def generate_response(bedrock_runtime, model_id, system_prompts, messages):
    """
    Sends messages to the DeepSeek model and handles the response.
    Error handling is significantly improved.
    """
    try:
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=messages,
            system=system_prompts,
            inferenceConfig={
                "temperature": 0.5,  # You can adjust these
                "maxTokens": (32768*1),   #  as needed.
            }
        )

        token_usage = response['usage']
        print(f"\nInput tokens: {token_usage['inputTokens']}")
        print(f"Output tokens: {token_usage['outputTokens']}")
        print(f"Total tokens: {token_usage['totalTokens']}")
        print(f"Stop reason: {response['stopReason']}")

        output_message = response['output']['message']

        #Remove reasoning
        output_contents = []
        for content in output_message["content"]:
            if content.get("reasoningContent"):
                continue
            else:
                output_contents.append(content)
        output_message["content"] = output_contents

        return output_message

    except ClientError as e:
        print(f"AWS client error: {e}")
        # Handle specific error codes if you can do something about them
        if e.response['Error']['Code'] == 'ThrottlingException':
            print("Request was throttled. Consider waiting and retrying.")
        elif e.response['Error']['Code'] == 'ValidationException':
             print("Check the request format and parameters.")
        return None  # Or raise, depending on your needs

    except Exception as e:  # Catch *any* other exception
        print(f"An unexpected error occurred: {e}")
        return None  # Or raise, if you want to stop the program on unhandled errors


def run_chatbot():
    """Main chatbot loop."""
    load_dotenv("/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/.env")  # Load environment variables first

    role_arn = "arn:aws:iam::677276075874:role/AWSBedrockFullAccesstoLambdaRole"  # Replace with your role ARN
    session_name = "DeepseekR1Session"
    credentials = assume_role (role_arn, session_name)

    bedrock_runtime = configure_bedrock_runtime ()
    bedrock = configure_bedrock ()
    files_string = load_directory_files ("./files/")

    # print (bedrock.list_foundation_models ())
    # print (bedrock.get_foundation_model (modelIdentifier="deepseek.r1-v1:0"))





    model_id = "us.deepseek.r1-v1:0"  # Or get from env, but a default is useful
    system_prompts = load_system_instructions()
    messages = []  # Initialize conversation history

    print("\033[92mChatbot started. Type 'exit' to quit or press Ctrl+D.\033[0m")

    while True:
        try:
            user_input = input("\033[94mYou: \033[0m")

            if user_input.lower() == 'exit':
                print("\033[92mChatbot exiting.\033[0m")
                break

            if user_input:
                # messages.append(prepare_message_with_file (user_input, files_string))  # Add user message to history
                messages.append(prepare_message (user_input))  # Add user message to history
                start_time = time.time()
                response_message = generate_response(bedrock_runtime, model_id, system_prompts, messages)
                end_time = time.time()

                if response_message:
                    messages.append(response_message) #add ai response to history
                    elapsed_time = end_time - start_time
                    # Print the text content of the response
                    response_text = ""
                    for content in response_message['content']:
                        if 'text' in content:
                            response_text += content['text'] + " "

                    print (f"Size of response: {sys.getsizeof (response_text.strip ())}B")
                    print (f"\n\033[91mChatbot ({elapsed_time:.2f}s):\033[0m\n{response_text.strip()}\n")

        except KeyboardInterrupt:
            print("^C")
            user_input = ""
            readline.insert_text('')  # Clear input buffer
            continue  # Go back to the start of the loop

        except EOFError:  # Ctrl+D
            print("\n\033[92mChatbot exiting.\033[0m")
            sys.exit (0)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")  # Catch-all for other errors
            continue

if __name__ == "__main__":
    run_chatbot()



# === Contents of gemini_generate.py ===

"""
<note>A parallel AI-powered document processing application using
Gemini 2.0 Pro and Flash models with free and paid API keys. The app
processes multiple text, PDF, and image files from a specified
directory in parallel using multiprocessing, combines the outputs, and
writes the results to a single output file.</note>
"""

import sys
import os, json
import asyncio
import logging
import concurrent.futures
from multiprocessing import cpu_count, Manager
import google.generativeai as genai
from google.genai import types

from dotenv import load_dotenv
import functools
import google.api_core
import pprint
import pathlib






load_dotenv()
SYS_INS = ""
MODEL_NAME = "GEMINI_20_FL"
PRO_MODEL_NAME = "GEMINI_20_PRO"
FLASH_MODEL_NAME = "GEMINI_20_FL"
API_KEY_PAID_STR = "API_KEY_PAID"
API_KEY_FREE_STR = "API_KEY_FREE"



# Set up logging with timestamp in the desired format (yyyy-mm-dd 24 hr)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s : %(levelname)s : %(message)s",  # Default log format with timestamp, level, and message
    datefmt="%Y-%m-%d %H:%M:%S",  # Timestamp format (yyyy-mm-dd 24 hr)
    handlers=[logging.FileHandler("gemini.log")]  # Output logs to console
)
logger = logging.getLogger(__name__)


# trace_client = trace.Client()



def log_entry_exit(func):
    """Decorator to log function entry and exit with function name."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the logger for the module where the function is defined
        func_logger = logging.getLogger(func.__module__)

        # Log function entry with function name
        func_logger.debug(f"Entering {func.__name__}")

        try:
            result = func(*args, **kwargs)
            return result
        finally:
            # Log function exit with function name
            func_logger.debug(f"Exiting {func.__name__}")

    return wrapper



def load_system_instructions():
    global SYS_INS
    # Retrieve the file path from the environment variable
    instructions_file_path = os.getenv('SYSTEM_INSTRUCTIONS_PATH')

    if instructions_file_path:
        try:
            # Open and read the system instructions file
            with open(instructions_file_path, 'r') as file:
                SYS_INS = file.read()

            # print ("sys_ins L70: ", sys_ins, "\n")
        except Exception as e:
            print(f"Error reading system instructions file: {e}")
    else:
        print("Environment variable 'SYSTEM_INSTRUCTIONS_PATH' not set.")






def configure_genai():
    global SYS_INS, PRO_MODEL_NAME, FLASH_MODEL_NAME, API_KEY_PAID_STR, API_KEY_FREE_STR

    if len(sys.argv) < 3:
        raise ValueError("Model type (pro/flash) and API key type (free/paid) must be provided.")


    SYS_INS = load_system_instructions ()




    model_type = sys.argv[1].lower()
    api_key_type = sys.argv[2].lower()

    if model_type == "pro":
        model_name = os.environ.get(PRO_MODEL_NAME)
    elif model_type == "flash":
        model_name = os.environ.get(FLASH_MODEL_NAME)
    else:
        raise ValueError("Invalid model_type. Must be 'pro' or 'flash'.")

    if api_key_type == "free":
        api_key = os.environ.get(API_KEY_FREE_STR)
        if not api_key:
             raise ValueError(f"The {API_KEY_FREE_STR} environment variable is not set.")

    elif api_key_type == "paid":
        api_key = os.environ.get(API_KEY_PAID_STR)
        if not api_key:
            raise ValueError(f"The {API_KEY_PAID_STR} environment variable is not set.")
    else:
        raise ValueError("Invalid api_key_type. Must be 'free' or 'paid'.")



    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name=model_name,
        system_instruction=SYS_INS
    )






@log_entry_exit
def gen_response(prompts, record):
    """Generate a response from the Gemini API using multiple prompts."""
    # logger.debug("Entering gen_response")
    gemini_response = None
    RESPONSES = []
    model = configure_genai()  # Initialize the model once
    # print ("record L101:", record, "\n")
    # print (len (record))

    
    if not prompts:
        logger.error("No prompts provided.")
        raise Exception("No prompts provided")
    
    for prompt in prompts:
        # Append the prompt to the record for context
        record.append(prompt)
        if gemini_response:
            # Add the previous response to the record for context
            record.append(gemini_response.text)

        try:
            # print ()
            # Call the Gemini API to generate a response based on the combined record and prompt list
            gemini_response = model.generate_content (contents=record)
            # logger.info(f"Successfully generated response for prompt: {prompt}".rstrip())

        except google.api_core.exceptions.ResourceExhausted as f:
            print("Error: API quota exhausted. Try again later.")
            return f"Error: {str(f)}"

        except Exception as e:
            # Log and handle errors appropriately
            logger.error(f"Error generating response for prompt '{prompt}': {e}")
            gemini_response = f"Error: {str(e)}"
            return f"Error: {str(e)}"

        record = []  # Reset the record for the next iteration
        # In this case, we do NOT reset the `record` here, because we need to keep context for subsequent prompts.

    return gemini_response.text

@log_entry_exit
def process_record(record, prompts, results_queue):
    """Process a single record with multiple prompts."""
    try:
        # Generate response based on record and prompts
        # print ("record L136:", [record])
        response = gen_response(prompts, [record])  # Pass record as list
        results_queue.put(response)  # Put the result in the queue
    except Exception as e:
        logger.error(f"Error processing record: {e}")
        results_queue.put(f"Error: {str(e)}")  # Put error message in the queue


@log_entry_exit
def collect_results_from_queue(results_queue):
    """Collect all results from the results_queue."""
    all_responses = []
    while not results_queue.empty():
        response = results_queue.get()
        all_responses.append(response)

    logger.info (f"Number of responses processed: {len (all_responses)}")
    # for res in all_responses:
    #     print (res [:2000], "\n\n\n\n")
    return all_responses


@log_entry_exit
def parallelize_processing(records, prompts):
    """Parallelize the processing of records and prompts using multiprocessing."""
    # global model
    # Get the number of available CPU cores
    num_workers = cpu_count()


    # Create a Manager and get a Queue that can be shared across processes
    with Manager() as manager:
        results_queue = manager.Queue()

        # Use ProcessPoolExecutor for parallel processing
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = []
            for record in records:
                futures.append(executor.submit(process_record, record, prompts, results_queue))


            # Wait for all futures to complete
            concurrent.futures.wait(futures)



        


            # Collecting results from the queue as the workers complete
            all_responses = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    # Ensure the process completes without error
                    future.result()  # If there was an exception in the worker, it will be raised here
                except Exception as e:
                    logger.error(f"Error during future processing: {e}")

            # Now gather all results from the queue
            all_responses = collect_results_from_queue(results_queue)

    return all_responses





def files_content() -> list:
    """
    Reads files from a directory, handling text, markdown, and PDF files.
    Returns a list of file contents (strings for text/markdown, Blobs for PDFs).
    """
    md_directory = './files/'
    records = []

    try:
        for f in os.listdir(md_directory):
            file_path = os.path.join(md_directory, f)

            try:  # Inner try-except for individual file processing
                if f.endswith((".txt", ".md")):
                    with open(file_path, 'r', encoding="utf-8") as file:
                        records.append(file.read())
                elif f.endswith(".pdf"):
                    pathlib_file_path = pathlib.Path(file_path)
                    content = types.Part.from_bytes(
                        data=pathlib_file_path.read_bytes(),
                        mime_type='application/pdf',
                    ).inline_data

                    blob = google.generativeai.protos.Blob (
                        data=content.data,
                        mime_type=content.mime_type
                    )
                    # print ("\nIs blob an instance of protos.Blob?: ", isinstance (blob, google.generativeai.protos.Blob), "\n")
                    # print (len (content.data))
                    records.append(blob)
                else:
                    logger.warning(f"Skipping unsupported file type: {f}")

            except FileNotFoundError:
                logger.error(f"File not found: {file_path}")  # Specific file, not directory
                # Don't exit; continue processing other files
            except OSError as e:
                logger.error(f"OS error reading file {file_path}: {e}")
                # Don't exit; continue processing other files
            except (TypeError, ValueError) as e:
                logger.error(f"Error processing file content {file_path} : {e}")
            except Exception as e:
                logger.error(f"Unexpected error processing {file_path}: {e}")
                # Consider logging stack trace for debugging:
                # logger.exception(f"Unexpected error processing {file_path}: {e}")

        return records  # Return even if some files had errors

    except FileNotFoundError:
        logger.error(f"Directory not found: {md_directory}")
        sys.exit(1)  # Exit if the *directory* is not found
    except OSError as e:
        logger.error(f"OS error accessing directory {md_directory}: {e}")
        sys.exit(1) #exit if cannot access directory
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)  # Exit for unexpected errors at the directory level




def lines_content ():
    # First argument is the file containing records (e.g., links)
    input_file = sys.argv[1]


    try:
        with open(input_file, 'r') as f:
            records = [line.strip() for line in f.readlines()]
            return records
    except FileNotFoundError:
        logger.error(f"File not found: {input_file}")
        sys.exit(1)



async def files_count_tokens_async () -> dict:
    """
    Reads files and "asynchronously" counts tokens (using asyncio.to_thread).
    ONLY uses asyncio.to_thread for count_tokens. File reading is synchronous
    Returns only the files_tokens dictionary.
    """
    
    md_directory = './files/'
    files_tokens = {}
    model = configure_genai ()


    async def process_file(file_path):
        nonlocal files_tokens

        if file_path.endswith((".txt", ".md")):
            try:
                # Synchronous file reading:
                with open(file_path, 'r', encoding="utf-8") as f:
                    content = f.read()

                # "Asynchronous" token counting (using asyncio.to_thread):
                token_count = await asyncio.to_thread(model.count_tokens, content)
                files_tokens[file_path] = token_count.total_tokens


            except Exception as e:
                print(f"Error processing {file_path}: {e}", file=sys.stderr)
                files_tokens[file_path] = -1

        elif file_path.endswith(".pdf"):
            try:
                # Synchronous file reading:
                pathlib_file_path = pathlib.Path(file_path)
                content = pathlib_file_path.read_bytes()
                part = types.Part.from_bytes(data=content, mime_type='application/pdf').inline_data
                blob = google.generativeai.protos.Blob (data=part.data, mime_type=part.mime_type)


                # "Asynchronous" token counting (using asyncio.to_thread):
                token_count = await asyncio.to_thread(model.count_tokens, blob)
                files_tokens[file_path] = token_count.total_tokens
            except Exception as e:
                print(f"Error processing {file_path}: {e}", file=sys.stderr)
                files_tokens[file_path] = -1
        else:
            print(f"Skipping unsupported file type: {file_path}", file=sys.stderr)

    try:
        tasks = [process_file(os.path.join(md_directory, f)) for f in os.listdir(md_directory)]
        await asyncio.gather(*tasks)
        return files_tokens

    except FileNotFoundError:
        print(f"Error: Directory not found: {md_directory}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)




@log_entry_exit
def res_agg (base_responses):
    # perform aggregate on base_responses

    try:
        with open("base_prompts.md", "r") as file:
            base_prompt = file.readline().strip()  # Read the first line and remove any trailing whitespace
            agg_prompt  = file.readline().strip()  # Read the second line and remove any trailing whitespace

    except FileNotFoundError:
        print("Error: base_prompts.md not found.")
        base_prompt = ""  # If the file isn't found, set base_prompt to an empty string
        agg_prompt = ""  # If the file isn't found, set agg_prompt to an empty string

    except Exception as e:
        print(f"An error occurred: {e}")

    
    prompts = ""
    custom_agg = input("Enter your custom aggregation prompt if any: ").strip()  # Take user input and strip any extra spaces

    # Append only if custom_agg is not empty
    # Now base_prompt is redundant
    if custom_agg:
        prompts = f"{agg_prompt} {custom_agg}"
    else:
        prompts = f"{agg_prompt}"

    # Log the created prompt
    logger.info(f"Aggregate prompt <agg prompt>: {prompts}")
   
    base_responses.append (prompts)
    
    # global model
    model = configure_genai ()




    gemini_response = model.generate_content (base_responses)
    aggregate_responses = [gemini_response.text]
    
    return aggregate_responses







@log_entry_exit
async def main():
    """Main function to read input, parallelize the work, and print the results."""
    logger.critical ("A new run;")
    logger.critical ("<run>")



    # Remaining arguments are the prompts
    # prompts = sys.argv[2:]

    # # Read the prepend string from base_prompts.md
    # try:
    #     with open("base_prompts.md", "r") as file:
    #         prepend_string = file.readline().strip()  # Read the first line and remove any trailing whitespace
    # except FileNotFoundError:
    #     print("Error: base_prompts.md not found.")
    #     prepend_string = ""  # If the file isn't found, set prepend_string to an empty string

    # Modify sys.argv[2:] by adding the prepend string before each prompt
    # prompts = [f"{prepend_string} {prompt}" for prompt in sys.argv[2:]]


    prompts = []
    # prepend_string = "Your prepend string here"

    # Interactive loop with break condition
    while True:
        user_input = input('Enter a prompt (or "done" to finish): ')
        if user_input.lower() == 'done':
            break
        # Now prepend_string is redundant
        prompt = f"{user_input}"
        prompts.append(prompt)
        logger.info(f"Prompt added <prompt>: {prompt}")








    # print("Modified prompts:", prompts)

    # Prompt user for input
    user_input = input("Choose the content source (1 for files, 2 for lines): ")
    agg_opt = input ("Do you want to perform aggregate operation? 1 for agg, 2 for no agg; ")
    # Assign records based on the input
    if user_input == '1':
        records = files_content()
        try:
            if sys.argv[3].lower() == "count":
                token_count = await files_count_tokens_async()
                pprint.pprint(token_count, indent=4)
        except IndexError:
            pass
        
    elif user_input == '2':
        records = lines_content()
    else:
        # Log error and exit program if the input is invalid
        logger.error(f"Invalid option chosen: {user_input}")
        sys.exit(1)    




    logger.info(f"Starting parallel processing for {len(records)} records with {len(prompts)} prompts.")

    # Parallelize processing
    all_responses = parallelize_processing(records, prompts)

    # Output results
    for i, responses in enumerate(all_responses):
        # logger.info(f"Responses for record {i + 1}:\n{responses}".rstrip())
        pass
    # for i, responses in enumerate(all_responses):
    #     print(f"{responses.rstrip()}")


    if (agg_opt == '1'):
        all_responses = res_agg (all_responses)
    else:
        pass



    # Clean and print all responses, then copy them to the clipboard
    cleaned_responses = "\n\n".join(responses.rstrip() for responses in all_responses)
    # logger.info(cleaned_responses)
    # print(cleaned_responses)  # Print the cleaned responses
    # pyperclip.copy(cleaned_responses)  # Copy them to the clipboard

    # print (cleaned_responses)
    with open("output_response.md", "w") as file:
        file.write(cleaned_responses + "\n\n")



    
    logger.critical ("</run>")












    
if __name__ == "__main__":
    # trace_span = client.start_span(name="application_start")
    asyncio.run (main())
    # trace_span.end ()



# === Contents of one_context.py ===

"""
<note>A parallel AI-powered document processing application using
Gemini 2.0 Pro and Flash models with free and paid API keys. The app
processes multiple directories in parallel using multiprocessing,
combining all text and PDF files within each directory before
processing, and writes the consolidated output to a single file</note>
"""

import sys
import os, signal, atexit
import concurrent.futures
from multiprocessing import cpu_count, Manager
import google.generativeai as genai
from google.genai import types
from dotenv import load_dotenv
import pathlib
import logging
import functools
import readline
import pprint, json





# --- Configuration and Setup ---
load_dotenv()
SYS_INS = ""
MODEL_NAME = "GEMINI_20_FL"  # Placeholder
PRO_MODEL_NAME = "GEMINI_20_PRO"
FLASH_MODEL_NAME = "GEMINI_20_FL"
API_KEY_PAID_STR = "API_KEY_PAID"
API_KEY_FREE_STR = "API_KEY_FREE"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("gemini_one_context.log")]
    # handlers=[logging.FileHandler("gemini_one_context.log")]
)
logger = logging.getLogger(__name__)

def log_entry_exit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Entering {func.__name__}")
        try:
            return func(*args, **kwargs)
        finally:
            logger.debug(f"Exiting {func.__name__}")
    return wrapper



def handle_sigpipe(signum, frame):
    print("SIGPIPE on stdout", file=sys.stdout)
    print("SIGPIPE on stderr", file=sys.stderr)
    logging.warning("SIGPIPE Warning: Attempting to write to a closed pipe....")

signal.signal (signal.SIGPIPE, handle_sigpipe)


def at_exit_function():
    print("atexit function called", file=sys.stderr)
    logging.info("atexit function called")

atexit.register(at_exit_function)


# Utility Functions

def load_system_instructions():
    """Loads system instructions."""
    global SYS_INS
    instructions_file_path = os.getenv('SYSTEM_INSTRUCTIONS_PATH')
    if instructions_file_path:
        try:
            with open(instructions_file_path, 'r') as file:
                SYS_INS = file.read()
        except Exception as e:
            logger.error(f"Error reading system instructions file: {e}")
    else:
        logger.warning("Environment variable 'SYSTEM_INSTRUCTIONS_PATH' not set.")

def configure_genai():
    """Configures the Gemini API."""
    global SYS_INS, PRO_MODEL_NAME, FLASH_MODEL_NAME, API_KEY_PAID_STR, API_KEY_FREE_STR

    if len(sys.argv) < 4:
        raise ValueError("Model type, API key type, and root/noroot must be provided.")


    model_type = sys.argv[1].lower()
    api_key_type = sys.argv[2].lower()

    if model_type == "pro":
        model_name = os.environ.get(PRO_MODEL_NAME)
    elif model_type == "flash":
        model_name = os.environ.get(FLASH_MODEL_NAME)
    else:
        raise ValueError("Invalid model_type. Must be 'pro' or 'flash'.")

    if api_key_type == "free":
        api_key = os.environ.get(API_KEY_FREE_STR)
        if not api_key:
             raise ValueError(f"The {API_KEY_FREE_STR} environment variable is not set.")
    elif api_key_type == "paid":
        api_key = os.environ.get(API_KEY_PAID_STR)
        if not api_key:
            raise ValueError(f"The {API_KEY_PAID_STR} environment variable is not set.")
    else:
        raise ValueError("Invalid api_key_type. Must be 'free' or 'paid'.")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name=model_name, system_instruction=SYS_INS)



@log_entry_exit
def gen_response(prompt, record):
    """Generates a response."""
    model = configure_genai()
    # print (type (prompt))
    contents = record + prompt
    try:
        response = model.generate_content(contents=contents)
        # print ("<response>: ", response.text [:100], "\n\n")
        logger.debug(f"Response length: {len(response.text)}") #Best Practice
        return response.text
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return f"Error: {e}"

@log_entry_exit
def process_record(directory, record, prompt, results_dict):
    """Processes a single record and stores result in a dictionary."""
    response = gen_response(prompt, record)
    results_dict[directory] = response  # Use directory as the key

@log_entry_exit
def collect_results_from_queue(results_queue):
    """Collects results from the queue."""
    all_responses = []
    while not results_queue.empty():
        response = results_queue.get()
        all_responses.append(response)
    return all_responses




@log_entry_exit
def parallelize_processing(directories, prompt):
    """Parallelizes processing using a dictionary for results."""
    num_workers = cpu_count()

    with Manager() as manager:
        results_dict = manager.dict()  # Use a managed dictionary

        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = []
            for directory in directories:
                record = files_content(directory)
                if not record:
                    continue
                # Pass directory to process_record
                futures.append(executor.submit(process_record, directory, record, prompt, results_dict))

            concurrent.futures.wait(futures)
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()  # Check for errors
                except Exception as e:
                    logger.error(f"Error during future processing: {e}")


        use_json = True
        filename = "rawresult.json"

        try:
            with open(filename, 'w') as f:
                if use_json:
                    json.dump(results_dict.copy (), f, indent=4)  # Use JSON with indentation
                else:
                    pprint.pprint(results_dict, stream=f) # Use pprint
        except Exception as e:
            logger.error (f"Error writing to file: {e}")




        # No need for collect_results_from_queue
        write_results_to_files(directories, results_dict)  # Pass the dictionary
    return list(results_dict.values()) #return values





@log_entry_exit
def files_content(directory_path) -> list:
    """Reads files from a directory."""
    records = []
    if not os.path.isdir(directory_path):
        logger.error(f"'{directory_path}' is not a valid directory.")
        return records

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            try:
                if filename.endswith((".txt", ".md")):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        records.append(f.read())
                elif filename.endswith(".pdf"):
                    pathlib_file_path = pathlib.Path(file_path)
                    part = types.Part.from_bytes(data=pathlib_file_path.read_bytes(), mime_type="application/pdf").inline_data
                    blob = genai.protos.Blob (data=part.data, mime_type=part.mime_type)
                    # blob = genai.types.Blob(data=part.data, mime_type=part.mime_type)
                    records.append(blob)
                else:
                    logger.warning(f"Unsupported file type: {file_path}")
            except Exception as e:
                logger.error(f"Error reading file {file_path}: {e}")
        else:
            logger.warning(f"Skipping non-file: {file_path}")
    return records




@log_entry_exit
def write_results_to_files(directories, results_dict):
    """Writes results to separate output files, using the results dictionary."""
    for i, directory in enumerate(directories):
        output_file_name = f"output_{i + 1}.md"
        with open(output_file_name, 'w') as outfile:
            outfile.write(f"# Directory: {directory}\n\n")
            # Get response directly from the dictionary using the directory as key
            if directory in results_dict:
                outfile.write(results_dict[directory])
                outfile.write("\n\n")
            else:
                logger.warning(f"No response found for directory: {directory}")
        logger.info(f"Responses for directory {directory} written to {output_file_name}")






def get_user_prompts():
    """Gets prompts interactively."""
    prompts = []
    while True:
        try:
            user_input = input('Enter a prompt (or "done" to finish): ')
        except KeyboardInterrupt: #still can be raised
            print("^C")
            readline.insert_text ('')
            user_input = ""
            continue

        except EOFError:
            print ("^D\nExiting")
            sys.exit (0)
        
        if user_input.lower() == 'done':
            break
        prompts.append(user_input)
    return prompts

def get_directories(root_or_noroot, remaining_args):
    """Gets the list of directories."""
    if root_or_noroot == "root":
        root_dir = remaining_args[0]
        if not os.path.isdir(root_dir):
            raise ValueError(f"'{root_dir}' is not a valid directory.")
        all_dirs = sorted([os.path.join(root_dir, d) for d in os.listdir(root_dir)])
        all_dirs = [d for d in all_dirs if os.path.isdir(d)]
        return all_dirs[:5]  # First 5
    elif root_or_noroot == "noroot":
        return remaining_args
    else:
        raise ValueError("Invalid option. Must be 'root' or 'noroot'.")

@log_entry_exit
def main():
    """Main function."""
    load_system_instructions()

    if len(sys.argv) < 4:
        logger.error("Usage: python script.py <pro/flash> <free/paid> <root/noroot> [<root_dir> | <dir1> <dir2> ...]")
        sys.exit(1)

    root_or_noroot = sys.argv[3].lower()
    remaining_args = sys.argv[4:]

    # Get directories with its own try-except block
    try:
        directories = get_directories(root_or_noroot, remaining_args)
        # print (directories)
        if not directories: #check for empty list
            logger.error("No directories to process.")
            sys.exit(1)
    except ValueError as e:
        logger.error(f"Error getting directories: {e}")
        sys.exit(1)



    directories.sort ()

    # Get prompts with its own try-except block
    try:
        # prompts = get_user_prompts()
        # prompts = ["summarize this with a proper H1 heading at top"]
        prompts = get_user_prompts ()
        
        if not prompts: #check for emtpry list
            logger.error("No prompts entered. Exiting.")
            sys.exit(1)
        # prompt = ' '.join(prompts)
    except Exception as e:
        logger.error(f"Error getting prompts: {e}")
        sys.exit(1)

    # print ("main", type (prompts))

    try:
       all_responses = parallelize_processing(directories, prompts)
       print("All directories processed. Check output files")
    except Exception as e: #Catch any other exception
        logger.error (f"An exception occurred: {e}")
        # sys.exit(1)



if __name__ == "__main__":
    main()



# === Contents of chatbot.py ===

"""
<note>A basic CLI chatbot that uses gemini 2.0 pro/2.0 flash AI
models.</note>
"""

import google.generativeai as genai
from google.genai import types
from google import genai as gemini
import os, time
import sys
import signal
import readline
from dotenv import load_dotenv
import pathlib





PRO_MODEL_NAME = "GEMINI_20_PRO"
FLASH_MODEL_NAME = "GEMINI_20_FL"
API_KEY_PAID_STR = "API_KEY_PAID"
API_KEY_FREE_STR = "API_KEY_FREE"





def load_system_instructions():
    instructions_file_path = os.getenv('SYSTEM_INSTRUCTIONS_PATH')
    if instructions_file_path:
        try:
            with open(instructions_file_path, 'r') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading system instructions: {e}")
    return ""

def configure_genai():
    global API_KEY_FREE_STR, API_KEY_PAID_STR, PRO_MODEL_NAME, FLASH_MODEL_NAME


    SYS_INS = load_system_instructions()

    if len(sys.argv) < 3:
        print("Usage: python your_script.py <pro|flash> <free|paid>")
        sys.exit(1)

    model_type = sys.argv[1].lower()
    api_key_type = sys.argv[2].lower()

    if model_type == "pro":
        model_name = os.getenv (PRO_MODEL_NAME)
    elif model_type == "flash":
        model_name = os.getenv (FLASH_MODEL_NAME)
    else:
        print("Invalid model_type. Must be 'pro' or 'flash'.")
        sys.exit(1)

    if api_key_type == "free":
        api_key = os.getenv(API_KEY_FREE_STR)
    elif api_key_type == "paid":
        api_key = os.getenv(API_KEY_PAID_STR)
    else:
        print("Invalid api_key_type. Must be 'free' or 'paid'.")
        sys.exit(1)

    if not api_key:
        print(f"Error: Required API key environment variable not set ({api_key_type}).")
        sys.exit(1)

    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name=model_name, system_instruction=SYS_INS)
    # return gemini.Client (api_key=api_key)





def files_content() -> list:
    """
    Reads files from a directory, handling text, markdown, and PDF files.
    Returns a list of file contents (strings for text/markdown, Blobs for PDFs).
    """
    md_directory = './chat/files/'
    records = []

    try:
        for f in os.listdir(md_directory):
            file_path = os.path.join(md_directory, f)

            try:  # Inner try-except for individual file processing
                if f.endswith((".txt", ".md")):
                    with open(file_path, 'r', encoding="utf-8") as file:
                        records.append(file.read())
                elif f.endswith((".pdf")):
                    pathlib_file_path = pathlib.Path(file_path)
                    content = types.Part.from_bytes(
                        data=pathlib_file_path.read_bytes(),
                        mime_type='application/pdf',
                    ).inline_data

                    blob = genai.protos.Blob (
                        data=content.data,
                        mime_type=content.mime_type
                    )
                    # print ("\nIs blob an instance of protos.Blob?: ", isinstance (blob, google.generativeai.protos.Blob), "\n")
                    # print (len (content.data))
                    records.append(blob)

                elif f.endswith((".png")):
                    pathlib_file_path = pathlib.Path(file_path)
                    content = types.Part.from_bytes(
                        data=pathlib_file_path.read_bytes(),
                        mime_type='image/png',
                    ).inline_data

                    blob = genai.protos.Blob (
                        data=content.data,
                        mime_type=content.mime_type
                    )
                    # print ("\nIs blob an instance of protos.Blob?: ", isinstance (blob, google.generativeai.protos.Blob), "\n")
                    # print (len (content.data))
                    records.append(blob)


                else:
                    print (f"Skipping unsupported file type: {f}")

            except FileNotFoundError:
                print (f"File not found: {file_path}")  # Specific file, not directory
                # Don't exit; continue processing other files
            except OSError as e:
                print (f"OS error reading file {file_path}: {e}")
                # Don't exit; continue processing other files
            except (TypeError, ValueError) as e:
                print (f"Error processing file content {file_path} : {e}")
            except Exception as e:
                print (f"Unexpected error processing {file_path}: {e}")
                # Consider logging stack trace for debugging:
                # print (f"Unexpected error processing {file_path}: {e}")

        return records  # Return even if some files had errors

    except FileNotFoundError:
        print (f"Directory not found: {md_directory}")
        sys.exit(1)  # Exit if the *directory* is not found
    except OSError as e:
        print (f"OS error accessing directory {md_directory}: {e}")
        sys.exit(1) #exit if cannot access directory
    except Exception as e:
        print (f"An unexpected error occurred: {e}")
        sys.exit(1)  # Exit for unexpected errors at the directory level









def run_chatbot():
    load_dotenv()
    model = configure_genai()
    # model = gemini.Client ()

    user_input = ""
    records = []

    # print (dir (model.start_chat ().send_message ("say Hi")))
    # print (model.start_chat ().send_message ("say Hi").usage_metadata.candidates_token_count)
    # print (model.start_chat ().send_message ("say Hi"))
    # print (model)

    # try:
    #     if sys.argv[3].lower() == "file":
    #         records = files_content ()
    # except IndexError:
    #     pass

    # session = model.start_chat (history=[
    #                                 types.Content (
    #                                     role="user",
    #                                     parts=[types.Part(records)]
    #                                 )
    #                             ])

    session = model.start_chat ()
    
    print("\033[92mChatbot started. Type 'exit' to quit or press Ctrl+D.\033[0m")

    while True:
        try:
            # readline.set_pre_input_hook(pre_input_hook)
            # print("\033[2K\r", end="", flush=True)  # Clear the line
            user_input = input("\033[94mYou: \033[0m")

            if user_input.lower() == 'exit':
                print("\033[92mChatbot exiting.\033[0m")
                break

            if user_input:
                try:
                    start_time = time.time ()
                    response = session.send_message (user_input)
                    end_time = time.time ()
                    elapsed_time = end_time - start_time
                    tokens_count = response.usage_metadata.candidates_token_count



                    print(f"\033[91mChatbot ({elapsed_time:.2f}s, {tokens_count}):\033[0m\n" + response.text + "\n")
                except Exception as e:
                    print(f"Chatbot: (Error generating response: {e})")

        except KeyboardInterrupt: #still can be raised
            print("^C")
            readline.insert_text ('')
            user_input = ""
            continue


        except EOFError:
            print("\n\033[92mChatbot exiting.\033[0m")
            sys.exit(0)


        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run_chatbot()

