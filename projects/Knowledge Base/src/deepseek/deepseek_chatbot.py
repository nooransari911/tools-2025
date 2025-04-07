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
    # files_string = load_directory_files ("./files/")

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
