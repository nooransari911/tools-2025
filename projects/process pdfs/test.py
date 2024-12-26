#from genai_gemini import *
from genai_gemini_parallel import *

test_blueprint = Blueprint('test', __name__)




@test_blueprint.route("/json/all")
def test_json():
    test_results = []

    try:
        with open("test-steps.json", "r") as f:
            test_cases = json.load(f).get("tests", [])

        base_url = request.host_url  # Use the current request's host URL

        if not test_cases:
            return jsonify({"summary": "No test cases found", "detailed_output": test_results})

        for test_case in test_cases:
            method = test_case.get("method")
            url = base_url + test_case.get("url", "")
            data = test_case.get("data", {})

            if not method or not url:
                test_results.append(f"Invalid test case: {test_case}")
                continue

            try:
                if method == "GET":
                    response = requests.get(url)
                elif method == "POST":
                    response = requests.post(url, data=data)
                else:
                    test_results.append(f"Unsupported method: {method} for URL: {url}")
                    continue

                # Check response status code and validate content if necessary
                if response.status_code == 200:
                    test_results.append(f"{method} {url}: Success")
                    # Add more specific assertions if needed
                    # For example:
                    # if "expected_text" in response.text:
                    #     test_results.append("Response contains expected text.")
                    # else:
                    #     test_results.append("Response does not contain expected text.")
                else:
                    test_results.append(f"{method} {url}: Failed (Status code: {response.status_code})")
                    test_results.append(response.text)  # Print the error response for debugging

            except requests.RequestException as e:
                test_results.append(f"{method} {url}: Exception occurred - {str(e)}")

        return jsonify({"summary": "Tests completed", "detailed_output": test_results})

    except FileNotFoundError:
        return jsonify({"error": "Test cases file not found"})
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON from test cases file"})
    except Exception as e:
        return jsonify({"error": str(e)})


@test_blueprint.route("/")
def test():
    return render_template("test_results.html", route="/test/json/all",
                           thleft="Request", thright="Status")





@test_blueprint.route ("/json/char")
def count_characters ():
    """Counts the number of characters in a text file."""
    count = 0
    filename = "./ex-input files/merge all.md"
    file_char_count = []

    with open(filename, 'r') as file:
        for line in file:  # Read line by line to avoid loading the whole file into memory
            count += len(line)

    file_char_count.append (f"{filename}: {count}")
    return jsonify({"summary": "Tests completed", "detailed_output": file_char_count})


@test_blueprint.route("/char")
def test_char():
    return render_template("test_results.html", route="/test/json/char",
                           thleft="Filename", thright="Char count")




@test_blueprint.route ("/json/split", methods=["GET", "POST"])
def split_file_json ():
    global GLOBAL_GENERIC_LIST

    if request.method == "POST":
        """Counts the number of characters in a text file."""
        directory = request.form.get('dir')
        filenames = os.listdir(directory)
        filenames = [f for f in filenames if os.path.isfile(os.path.join(directory, f))]
        #print("/test/json/split filenames:", filenames)
        count = 0
        #filename = "./ex-input files/merge all.md"
        for filename in filenames:
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                try:
                    split_markdown_file (file_path)
                except Exception as e:
                    raise e
        return jsonify({"summary": "Tests completed", "detailed_output": GLOBAL_GENERIC_LIST})

    else:
        return jsonify({"summary": "Tests completed", "detailed_output": GLOBAL_GENERIC_LIST})


@test_blueprint.route("/split", methods=["GET", "POST"])
def split_file():
    if request.method=="POST":
        directory = request.form.get('dir')
        return render_template("test_results.html", route="/test/json/split",
                               thleft="match", thright="filename", directory=directory)
    else:
        return render_template("gemini_app.html")


@test_blueprint.route ("/process")
def test_all_processes ():
    return render_template ("ge_te_re_3.html", route="/json/process/")