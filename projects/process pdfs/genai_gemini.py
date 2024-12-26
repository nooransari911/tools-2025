"""
export Gemini API Key to API_KEY

"""
import multiprocessing

from utils import *



genai.configure(api_key=os.environ["API_KEY_FREE"])

model = genai.GenerativeModel("gemini-1.5-flash")

prompt = "briefly describe this image"



directory_to_upload = "/home/ansarimn/Downloads/tools and projects/projects/google cloud ai suite/source/vision ai"


def extract_numbers(filename):
    # Extract numbers from the filename using regex
    numbers = re.findall(r'\d+', filename)
    return [int(num) for num in numbers] if numbers else [0]



@timestamped_print
def upload_directory_to_genai(directory_path):
    """Uploads all files in a directory to GenAI.

    Args:
        directory_path: The path to the directory containing the files.
    """
    filenames = os.listdir(directory_path)
    filenames = [f for f in filenames if os.path.isfile(os.path.join(directory_path, f))]
    filenames.sort(key=lambda x: extract_numbers(x), reverse=True)  # Case-insensitive sorting

    print("Sorted filenames:", filenames)


    for filename in filenames:
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            try:
                genai_file = genai.upload_file(
                    path=file_path,
                    display_name=filename  # Set display name to the file name
                )
                print(f"Uploaded: {filename} (ID: {genai_file.name})")
            except Exception as e:
                print(f"Error uploading {filename}: {e}")


def list_genai_file_names ():
    file_info = []
    for file in genai.list_files():
        files_ready_genai()
        model_input_token = model.count_tokens(file)
        file_info.append (f"{file.display_name}; URI: {file.uri}; input tokens: {model_input_token}")
        print (f"{file.display_name}; URI: {file.uri}; input tokens: {model_input_token}")
    return file_info


@timestamped_print
def delete_all_genai_files ():
    for file in genai.list_files():
        print(f"Delete: {file.display_name}")
        genai.delete_file(file.name)


def files_ready_genai ():
    for genai_file in genai.list_files():
        while genai_file.state.name == "PROCESSING":
            print('.', end='')
            time.sleep(10)
            genai_file = genai.get_file (genai_file.name)

        if genai_file.state.name == "FAILED":
            raise ValueError(genai_file.state.name)




def gemini_chain (file=None):
    gemini_input = [file] if file else []
    #gemini_input = LOREM_IPSUM_STRING
    gemini_response = None

    global PROMPT_LIST
    # Iterate over the list of prompts
    #print (PROMPT_LIST)

    if not PROMPT_LIST:
        raise Exception("Empty List")
        return


    for pri in PROMPT_LIST:
        # Append the current prompt to the input
        gemini_input.append(pri)

        # Add previous response (if available) to the current prompt
        if gemini_response:
            gemini_input.append(gemini_response.text)

        # Send the input (PDF or previous response + current prompt) to Gemini
        gemini_response = model.generate_content(gemini_input)
        #time.sleep(80)
        RESPONSES.append (gemini_response.text)
        gemini_input = []

    with open (output_file, "w") as md_output_file:
        md_output_file.write (f"{datetime.datetime.now ()};\n\n{gemini_response.text}")
    with open(all_iterations_file, "w") as md_file:
        md_file.write (f"{datetime.datetime.now ()};\n\n{RESPONSES}")

    # Return Gemini output text
    return gemini_response.text


def gemini_chain_all_files (directory):
    gemini_responses = []
    ilist, olist = [], []


    upload_directory_to_genai(directory)
    #print (list_genai_file_names())
    for file in genai.list_files():
        print (f"Processing file {file.display_name}")
        iint = model.count_tokens (file).total_tokens
        ilist.append (iint)
        gemini_response = gemini_chain(file)

        oint = model.count_tokens(gemini_response).total_tokens
        olist.append(oint)
        gemini_responses.append(gemini_response)



    total_icount = sum (ilist)
    total_ocount = sum (olist)

    istring = f"total input tokens: {total_icount}"
    ostring = f"total output tokens: {total_ocount}"

    gemini_responses.insert (0, ostring)
    gemini_responses.insert (0, istring)




    delete_all_genai_files()
    return gemini_responses


def test_all ():
    # Load test cases from JSON file (or directly from the string)
    with open("./test-steps.json", "r") as f:
        test_cases = json.load(f)["tests"]

    # Base URL for your Flask app (replace with your actual URL)
    base_url = "http://localhost:5000"

    # Iterate through the test cases and execute them
    for test_case in test_cases:
        method = test_case["method"]
        url = base_url + test_case["url"]
        data = test_case["data"]

        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, data=data)
        else:
            print(f"Unsupported method: {method}")
            continue

        # Check for successful response status code (e.g., 200)
        if response.status_code == 200:
            print(f"{method} {url}: Success")
            # Optionally, you can add more specific assertions based on the response content
            # For example:
            # if "some_expected_text" in response.text:
            #     print("Response contains expected text.")
        else:
            print(f"{method} {url}: Failed (Status code: {response.status_code})")
            print(response.text)  # Print the error response for debugging

if __name__ == '__main__':
    upload_directory_to_genai(directory_to_upload)
    list_genai_file_names()
    delete_all_genai_files()
