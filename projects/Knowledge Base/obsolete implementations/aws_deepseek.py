# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to run a multimodal prompt with Nova Lite (on demand) and InvokeModel.
"""



import os, sys
import json
import logging
import base64
import boto3, botocore
from botocore.exceptions import ClientError
import requests
import readline
import botocore.client






logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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




# Constructing the InferenceProfileModelSource object
def create_inference_profile_model_source(model_name):
    # Example: Constructing the ARN from model name
    region = "us-west-2"  # Replace with the appropriate AWS region
    account_id = "677276075874"  # Replace with your AWS account ID

    # Construct the ARN (this is just an example pattern)
    arn = f"arn:aws:bedrock:{region}:{account_id}:foundation-model/{model_name}"

    # Return the object with 'copyFrom' as the ARN
    return {
        "copyFrom": arn
    }




# Function to make a POST request to create an inference profile
def create_inference_profile (model_name, credentials):
    """
    Creates an inference profile by making a POST request to the /inference-profiles API.
    """
    # AWS API endpoint
    api_url = 'https://bedrock.us-west-2.amazonaws.com/inference-profiles/'  # Replace with your API URL



    modelsource = create_inference_profile_model_source (model_name)


    # Prepare the payload for the request
    payload = {
        "inferenceProfileName": "DeepseekInferenceProfile",  # replace with your profile name
        "modelSource": {
            # Fill in the model source details here
            "someField": "someValue",  # Example key-value pair for model source
        }
    }

    # Get AWS credentials using boto3
    # session = boto3.Session()
    # credentials = session.get_credentials()

    aws_access_key    =    credentials['AccessKeyId']
    aws_secret_key    =    credentials['SecretAccessKey']
    aws_session_token =    credentials['SessionToken']

    # Set the headers, including authorization if necessary
    headers = {
        "Content-type": "application/json",
        "x-amz-security-token": aws_session_token,  # Only if using temporary session credentials
        "x-amz-access-key": aws_access_key,
        "x-amz-secret-key": aws_secret_key
    }

    # Make the POST request
    try:
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            print("Inference profile created successfully:", response.json())
        else:
            logger.error(f"Request failed with status code {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to make the API request: {e}")
        raise





def run_multi_modal_prompt(bedrock_runtime, model_id, prompt, max_tokens):
    """
    Invokes a model with a multimodal prompt.
    Args:
        bedrock_runtime: The Amazon Bedrock boto3 client.
        model_id (str): The model ID to use.
        messages (JSON): The messages to send to the model.
        max_tokens (int): The maximum number of tokens to generate.
    Returns:
        None.
    """


    # Format the request payload using the model's native structure.
    native_request = {
        "prompt": prompt,
        "max_tokens": max_tokens
    }


    body = json.dumps(
        native_request
    )
    
    response = bedrock_runtime.invoke_model (
                    body=body, modelId=model_id)
    # response_body = json.loads (response.get('body').read())

    return response


def main():
    """
    Entrypoint for Nova Lite video prompt example.
    """

    try:
        # Assume the role and get temporary credentials
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
        # print (credentials.keys)
        # print (type (bedrock_runtime))
        # print (dir (bedrock_runtime))

        model_name = "arn:aws:bedrock:us-west-2:677276075874:inference-profile/us.deepseek.r1-v1:0"
        model_name = "us.deepseek.r1-v1:0"
        max_tokens = 32768
        input_video_s3_uri = "s3://ansarimn-public-s3-video/lorem-ipsum-video.mp4"  # Replace with real S3 URI
        video_ext = input_video_s3_uri.split(".")[-1]
        # prompt = "What is an API. Explain in detail."
        try:
            # prompt = input('Enter a prompt: ')
            prompt = "Explain why S3 is the best object storage in its class"


        except KeyboardInterrupt: #still can be raised
            print("^C")
            readline.insert_text ('')
            prompt = ""

        except EOFError:
            print ("^D\nExiting")
            sys.exit (0)
        # inference_profile = create_inference_profile (model_name, credentials)




        try:
            print ("Generating Response....\n\n")
            response: dict = run_multi_modal_prompt (
                            bedrock_runtime, model_name, prompt, max_tokens)
            

            # print(json.dumps (response, indent=4))
            # print(response)
            # response_loaded = json.loads (response)
            # response_body = json.loads (response.get ('body').read())
            raw_body = response ['body'].read()
            response ['body'] = json.loads(raw_body.decode('utf-8'))  # Decode as UTF-8 and parse JSON
            # print (json.dumps (response, indent=4))


            print ("Output size: ", response ["ResponseMetadata"] ["HTTPHeaders"] ["x-amzn-bedrock-output-token-count"])
            # print (type (response ["body"]))
            # print (dir  (response ["body"]))
            # print ((response ["body"]))
            # print ((response ["body"].__dict__))
            # print (dir  (response))
            print (response ["body"] ["choices"] [0] ["text"])
            # print(raw_body)


        except Exception as e:
            print (f"\nException for InvokeModel: {e}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occurred: " + format(message))


if __name__ == "__main__":
    main()
