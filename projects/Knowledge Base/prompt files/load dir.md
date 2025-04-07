rewrite this to intelligently accept: 1 text (not strictly .txt, but anything text like md, html, xml, etc) file path or a directory that contains arbitrary number of text files. when its a text file, read the file and form a string from it. when its a dir, properly form a string from all the files with each file identified explictly. you can refer load_directory_files (dir) function; it achieves a similar functionality. you are free to rewrite both as needed


what you need to rewrite:

    if num_args >= 2 and sys.argv[1] == "file":
        print ("Prompt from file mode;\n")
        prompt_file_path = sys.argv [2]
        text_file_path   = sys.argv [3]
        output_file_path = sys.argv [4]
        should_print     = sys.argv [5]


        
        if not os.path.isfile (prompt_file_path):
            print (f"No such file as {prompt_file_path}\n\n")

        if not os.path.isfile (text_file_path):
            print (f"No such file as {text_file_path}\n\n")

        if output_file_path is None:
            print (f"No output file path provided\n\n")

        else:
            with open (prompt_file_path, "r") as prompt_file, open (text_file_path, "r") as text_file:
                prompt_file_string = prompt_file.read ()
                prompt_file_message = prepare_message (prompt_file_string, "user")
                messages.append (prompt_file_message)
                text_file_string = f"Text file:\n\n{text_file.read ()}"
                text_file_message = prepare_message (text_file_string, "user")
                messages.append (text_file_message)

                prompt_file_response = generate_response (bedrock_runtime, model_id, system_prompts, messages)
                # print ("\n\nResponse body dump: ")
                # print (json.dumps (initial_response, indent = 4))

                print (f"Size of response: {sys.getsizeof (prompt_file_response)}B")
                print ("\n\n")


            messages.append (prepare_message (prompt_file_response, "assistant")) #add ai response to history


            if should_print.lower () == "print":
                print ("\n\n", prompt_file_response, "\n\n")


            with open (output_file_path, "w") as output_file:
                output_file.write (prompt_file_response)


load_directory_files (dir):

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

