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
