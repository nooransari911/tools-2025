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
TOKENS_STORE_JSON_FILE_NAME = os.getenv ("CLAUDE_TOKENS_STORE_JSON_FILE_NAME")







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



def load_usage_json ():
    try:
        with open(TOKENS_STORE_JSON_FILE_NAME, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def save_usage_json (data: list):
    old_data = load_usage_json ()
    new_data = {}

    if not old_data:
        old_data = {
            "input_tokens": 0,
            "output_tokens": 0
        }
    
    new_data ["input_tokens"]  = old_data ["input_tokens"]   +  data [0]
    new_data ["output_tokens"] = old_data ["output_tokens"]  +  data [1]
    
    with open(TOKENS_STORE_JSON_FILE_NAME, 'w') as f:
        json.dump(new_data, f, indent=4)

def reset_usage ():
    
    new_data = {
        "input_tokens": 0,
        "output_tokens": 0
    }


    with open(TOKENS_STORE_JSON_FILE_NAME, 'w') as f:
        json.dump(new_data, f, indent=4)




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


    should_deep_think = os.getenv ("SHOULD_CLAUDE_37_DEEP_THINK")
    deep_think_budget = os.getenv ("CLAUDE_37_DEEP_THINK_BUDGET")

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_op_tokens,
        "system": system_prompts,
        "messages": messages
    }
    # if should_deep_think.lower () == "true":
    #     body ["thinking"] = {
    #         "type": "enabled",
    #         "budget_tokens": int (deep_think_budget)
    #     }

    body_string = json.dumps (
        body
    )

    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=body_string
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

        save_usage_json ([
                             int (token_usage ['input_tokens']),
                             int (token_usage ['output_tokens'])
                         ])


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
        print(f"An unexpected error occurred in generate_response: {e}")
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





    # model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0" 
    model_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0" 
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
