from genai_gemini_parallel import *


RESULT_DICT = Manager().dict()
METADATA_DICT = Manager().dict()








@timestamped_print
@parallel_blueprint.route('/', methods=['GET', 'POST'])
def phome_async():
    if request.method == 'POST':
        directory = request.form.get('dir')


        if os.path.exists(directory):
            #print("Directory exists!!")
            process = multiprocessing.Process(target=pgemini_chain_all_files, args=(directory, PROMPT_LIST, RESULT_DICT, METADATA_DICT))
            process.start()
            PROCESS_L0.append(process.pid)
            print (f"for pgemini_chain_all_files: {process.pid}")
            return render_template('plive status.html', directory=directory)
        else:
            #print("No such directory")
            return render_template('gemini_app.html', heading="No such directory")


    return render_template('gemini_app.html', file_name=None)


@timestamped_print
@parallel_blueprint.route('/results', methods=['GET', "POST"])
def presults():
    if request.method == 'POST':
        directory = request.form.get('dir')
        print("presults; PROCESS_L0: ", PROCESS_L0)
        print("presults; PROCESS_L1: ", PROCESS_L1)


        if PROCESS_L0:
            active_processes_L0 = [p for p in PROCESS_L0 if psutil.pid_exists(p)]
            active_processes_L1 = [p for p in PROCESS_L1 if psutil.pid_exists(p)]
            print("presults; PROCESS: ", PROCESS_L0)
            print("presults; active process L0: ", active_processes_L0)
            print("presults; active process L1: ", active_processes_L1)
            if not active_processes_L0:
                # Processes have completed
                all_responses_string, iint, oint, total_time = putil(RESULT_DICT, METADATA_DICT)
                return render_template('random_html.html',
                                       directory=directory, responses=all_responses_string, iint=iint, oint=oint, total_time=total_time)
            else:
                # Processes are still running
                return render_template('plive status.html', directory=directory)
        else:
            # No processes have been started
            return render_template('plive status.html', directory=directory)  # Return live status for idle state


    else:
        return render_template('gemini_app.html', file_name=None)



def pprocess_status():
    done_sent = False  # Flag to track if "done" has been sent

    while True:
        if not PROCESS_L0:
            status_string = "data: status: idle\n\n"
        else:
            active_processes = [p for p in PROCESS_L0 if psutil.pid_exists(p)]
            if not active_processes and not done_sent:
                status_string = "data: status: done\n\n"
                done_sent = True  # Set the flag to True
                #PPROCESS.clear()  # Clear the list only once
            elif not active_processes:
                # Keep yielding "done" until the connection is closed by the client
                #process = multiprocessing.Process (target=redirect, args=("/parallel/results",))
                status_string = "data: status: done\n\n"
            else:
                status_string = "data: status: processing\n\n"

        yield status_string
        time.sleep(1)




@parallel_blueprint.route("/events")
def pevents():
    return Response(pprocess_status(), content_type='text/event-stream')



@parallel_blueprint.route ("/up", methods=["GET", "POST"])
def pup ():
    if request.method == 'POST':
        directory = request.form.get('dir')
        upload_directory_to_genai (directory)
        return ("Uploaded all files successfully")
    else:
        return render_template("gemini_app.html")