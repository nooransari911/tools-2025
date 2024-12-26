import json
import time


from genai_gemini import *
#from genai_gemini_parallel import *
import multiprocessing
from multiprocessing import Manager



root_blueprint = Blueprint('root', __name__)





manager = Manager()
task_results = manager.dict()
PROCESS: list[multiprocessing.Process] = []



def time_route(f):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        duration = time.time() - start_time
        print(f"Route {f.__name__} took {duration:.4f} seconds")
        return result
    return wrapper




@time_route
@root_blueprint.route('/sync', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        directory = request.form.get('dir')

        if os.path.exists(directory):
            #print("Directory exists!!")
            responses = gemini_chain_all_files(directory)
            json_data = {
                'heading': "Selected directory:",
                'directory': directory,
                'responses': responses
            }
            #print(responses)
            return render_template ('gemini_responses.html',
                                    directory=directory, responses=responses)
        else:
            #print("No such directory")
            return render_template('gemini_app.html', heading="No such directory")


    return render_template('gemini_app.html', file_name=None)







def process_multiple_directories (directory, global_dict):
    time_start = time.time_ns()
    global all_files, PROMPT_LIST
    #print(PROMPT_LIST)

    try:
        # Attempt to run the gemini_chain_all_files function
        result = gemini_chain_all_files(directory)
        time_end = time.time_ns()
        elapsed_time = (time_end-time_start) / (10 ** 9)

        # Store successful result in the shared dictionary
        global_dict [directory] = {
            "status": "completed",
            "directory": directory,
            "response": result,
            "time_taken": elapsed_time
        }
        with open(all_files, "w") as file:
            file.write (f"# {datetime.datetime.now()};\n\n# Total Time taken: {task_results[directory]["time_taken"]}")
            for i in task_results[directory]["response"]:
                file.write(f"\n\n{i}")

    except Exception as e:
        time_end = time.time_ns()
        elapsed_time = (time_end - time_start) / (10 ** 9)

        # Store the error message in the dictionary if an exception occurs
        global_dict [directory] = {
            "status": "failed",
            "directory": directory,
            "response": str(e),
            "time_taken": elapsed_time
        }
        with open(all_fileserr, "w") as file:
            file.write(f"{datetime.datetime.now ()};\n\n{task_results[directory]["response"]}")

        raise e








@time_route
@root_blueprint.route('/', methods=['GET', 'POST'])
def home_async():
    if request.method == 'POST':
        directory = request.form.get('dir')

        if os.path.exists(directory):
            #print("Directory exists!!")
            process = multiprocessing.Process(target=process_multiple_directories, args=(directory, task_results))
            process.start()
            PROCESS.append(process)
            return render_template('live status.html', directory=directory)
        else:
            #print("No such directory")
            return render_template('gemini_app.html', heading="No such directory")


    return render_template('gemini_app.html', file_name=None)


def process_status():
    while True:  # Keep checking the status indefinitely
        if not PROCESS:  # Handle the case where the list is empty
            status_string = "data: status: idle\n\n"
        else:
            status_value = PROCESS[-1].is_alive()
            if status_value == False:
                status_string = "data: status: done\n\n"
                PROCESS.pop()  # Remove the finished process from the list
            else:
                status_string = "data: status: processing\n\n"
        yield status_string
        time.sleep(1)




@root_blueprint.route("/events")
def events():
    return Response(process_status(), content_type='text/event-stream')



@root_blueprint.route('/results', methods=['GET', "POST"])
def results():
    if request.method == 'POST':
        directory = request.form.get('dir')

        if PROCESS and not PROCESS [-1].is_alive():
            # Return the result (either success or failure) as a JSON response

            return render_template ('gemini_responses.html',
                                   directory=directory, responses=task_results[directory]["response"], elapsed_time=task_results[directory]["time_taken"])

        else:
            return render_template('live status.html', directory=directory)

    else:
        return render_template('gemini_app.html', file_name=None)




# Route to check if the process is done and get the results
@root_blueprint.route('/delete-files', methods=['GET', "POST"])
def delete_files():
    delete_all_genai_files()
    return ("<h1>Delete successful</h1>")



@root_blueprint.route('/delete-prompts', methods=['GET', "POST"])
def delete_prompt():
    global PROMPT_LIST
    PROMPT_LIST = []
    return ("<h1>Delete successful</h1>")


@root_blueprint.route('/delete', methods=['GET', "POST"])
def delete():
    return render_template ("generic_delete.html")



@root_blueprint.route('/prompts', methods=['GET', "POST"])
def prompts():
    global PROMPT_LIST
    if request.method == 'POST':
        prompt = request.form.get('prompt')

        if prompt:
            PROMPT_LIST.append (prompt)

        # Return the result (either success or failure) as a JSON response
        return render_template ('show_all_prompts.html',
                               prompt_list=PROMPT_LIST)


    else:
        return render_template('add_prompts.html',
                               prompt_list=PROMPT_LIST)







