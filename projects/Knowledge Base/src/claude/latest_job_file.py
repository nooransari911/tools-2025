import os, io
import sys
import time
import readline




import claude_chatbot
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from dotenv import load_dotenv
load_dotenv ("/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/.env")






def ListBucketObjects(S3Client, bucket_name, prefix=""):
    """List objects in S3 bucket with optional prefix
    
    Args:
        S3Client: boto3 S3 client
        bucket_name: Name of S3 bucket
        prefix: Optional prefix to filter results
        
    Returns:
        (Success?True:False, List of objects or error message)
    """
    try:
        response = S3Client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix
        )
        
        if 'Contents' in response:
            return (True, response['Contents'])
        else:
            return (True, [])
            
    except Exception as e:
        error_msg = f"ListBucketObjects failed: {e}"
        print(error_msg)
        return (False, error_msg)


def GetObjectMetadata(S3Client, bucket_name, key):
    """Get metadata for an S3 object
    
    Args:
        S3Client: boto3 S3 client
        bucket_name: Name of S3 bucket
        key: Object key
        
    Returns:
        (Success?True:False, Object metadata or error message)
    """
    try:
        response = S3Client.head_object(
            Bucket=bucket_name,
            Key=key
        )
        return (True, response)
        
    except Exception as e:
        error_msg = f"GetObjectMetadata failed: {e}"
        print(error_msg)
        return (False, error_msg)


def FindLatestFolder(objects):
    """Find the most recent folder based on object list
    
    Args:
        objects: List of S3 objects
        
    Returns:
        String containing the latest folder prefix
    """
    if not objects:
        return None
        
    # Group objects by folder prefix (random string part)
    folders = {}
    for obj in objects:
        key = obj['Key']
        parts = key.split('/')
        if len(parts) >= 2:
            folder = parts[0] + '/'
            if folder not in folders:
                folders[folder] = []
            folders[folder].append(obj)
    
    # Find the most recent folder based on LastModified
    latest_folder = None
    latest_date = None
    
    for folder, folder_objects in folders.items():
        for obj in folder_objects:
            if latest_date is None or obj['LastModified'] > latest_date:
                latest_date = obj['LastModified']
                latest_folder = folder
    
    return latest_folder


def GetLatestFileKey(objects, folder_prefix):
    """Get the key of the latest file in the specified folder
    
    Args:
        objects: List of S3 objects
        folder_prefix: Folder prefix to filter by
        
    Returns:
        Key of the latest file in the folder
    """
    if not objects or not folder_prefix:
        return None
        
    # Filter objects in the specified folder
    folder_objects = [obj for obj in objects if obj['Key'].startswith(folder_prefix)]
    
    # Find the most recent object
    if folder_objects:
        latest_object = max(folder_objects, key=lambda x: x['LastModified'])
        return latest_object['Key']
    
    return None


def GetLatestS3File(S3Client, bucket_name):
    """Get the most recently created file in the S3 bucket
    
    Args:
        S3Client: boto3 S3 client
        bucket_name: Name of S3 bucket
        
    Returns:
        (Success?True:False, Object key or error message)
    """
    try:
        # Get all objects
        success, objects = ListBucketObjects(S3Client, bucket_name)
        if not success:
            return (False, objects)  # objects contains the error message
            
        # Find the latest folder
        latest_folder = FindLatestFolder(objects)
        if not latest_folder:
            return (False, "No folders found in bucket")
            
        # Get the latest file in that folder
        latest_file_key = GetLatestFileKey(objects, latest_folder)
        if not latest_file_key:
            return (False, f"No files found in latest folder: {latest_folder}")
            
        return (True, latest_file_key)
        
    except Exception as e:
        error_msg = f"GetLatestS3File failed: {e}"
        print(error_msg)
        return (False, error_msg)


def DownloadLatestS3File(S3Client, bucket_name, local_path="./latest_file"):
    """Download the most recently created file from S3 bucket
    
    Args:
        S3Client: boto3 S3 client
        bucket_name: Name of S3 bucket
        local_path: Local path to save the downloaded file
        
    Returns:
        (Success?True:False, Local file path or error message)
    """
    try:
        # Get the key of the latest file
        success, result = GetLatestS3File(S3Client, bucket_name)
        if not success:
            return (False, result)  # result contains the error message
            
        latest_file_key = result
        
        # Download the file
        S3Client.download_file (
            Bucket=bucket_name,
            Key=latest_file_key,
            Filename=local_path
        )

        s3_head_op = S3Client.head_object(
            Bucket=bucket_name,
            Key=latest_file_key
        )


        s3_head_op ["Key"] = latest_file_key
        # print ("Success")        
        return (True, s3_head_op)
        
    except Exception as e:
        error_msg = f"DownloadLatestS3File failed: {e}"
        print(error_msg)
        return (False, error_msg)



def DownloadLatestS3FileMain ():
    claude_chatbot.assume_role (claude_chatbot.ROLE_ARN, "DownloadLatestJobFileSession")
    S3Client = boto3.client ("s3")
    
    # _, file_key = GetLatestS3File (
    #     S3Client=S3Client,
    #     bucket_name=S3_DEST
    # )


    is_success, response = DownloadLatestS3File (
        S3Client,
        claude_chatbot.S3_DEST
    )

    if is_success:
        # Extract key information from successful response
        key                    =    response ["Key"]
        accept_ranges          =    response ["AcceptRanges"]
        last_modified          =    response ["LastModified"]
        content_length         =    response ["ContentLength"]
        etag                   =    response ["ETag"]
        content_type           =    response ["ContentType"]
        server_side_encryption =    response ["ServerSideEncryption"]
        metadata               =    response ["Metadata"]

        # Print the most important information
        print(f"\n{'Key:':<15} {key}"
              f"\n{'Size:':<15} {content_length} bytes"
              f"\n{'Type:':<15} {content_type}"
              f"\n{'Last Modified:':<15} {last_modified.isoformat()}"
              f"\n{'ETag:':<15} {etag}")



def dev_main ():
    pass




def main ():
    DownloadLatestS3FileMain ()



if __name__ == "__main__":
    num_args = len(sys.argv)
    # if num_args == 2 and sys.argv[1] == "list":
    #     jobs_status()
    # elif num_args == 2 and sys.argv[1] == "load":
    #     load_mode()
    # elif num_args == 4 and sys.argv[1] == "clean":
    #     extract_text_from_jsonl(sys.argv[2], sys.argv[3])
    if num_args == 2 and sys.argv[1] == "dev":
        dev_main()
    # elif num_args == 2 and (sys.argv[1] == "help" or sys.argv[1] == "-h" or sys.argv[1] == "--help"): #added this
    #     print_help()
    else:
        main() #changed this to call main by default

