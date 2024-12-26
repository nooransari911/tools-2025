from flask import Flask
from flask_cors import CORS
from blueprints.genai_gemini_app import root_blueprint
#from source.blueprints.genai_gemini_app import root_blueprint
from blueprints.test import test_blueprint
from blueprints.json_blueprints import json_blueprint
from blueprints.events_blueprints import events_blueprint
from blueprints.parallel import parallel_blueprint, PROCESS_L0
from blueprints.base_gemini.utils.utils import *


app = Flask(__name__)
CORS(app)
app.register_blueprint (root_blueprint, url_prefix="/")
app.register_blueprint (test_blueprint, url_prefix="/test")
app.register_blueprint (parallel_blueprint, url_prefix="/parallel")
app.register_blueprint (json_blueprint, url_prefix="/json")
app.register_blueprint (events_blueprint, url_prefix="/events")



#@timestamped_print
def sigchld_handler(signum, frame):
    # Simplified handler, avoid print
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break
            # Log to a file or use a signal-safe mechanism
            with open("../output files/SIGCHLD_log.txt", "a") as f:
                f.write(f"Child process {pid} terminated with status {status}\n")
        except OSError:
            break
signal.signal(signal.SIGCHLD, sigchld_handler)


@timestamped_print
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')

    # Terminate child processes
    for process in PROCESS_L0:
        try:
            p = psutil.Process(process.pid)
            p.terminate()
            p.wait(timeout=5)
        except psutil.NoSuchProcess:
            print(f"Process with PID {process.pid} not found.")
        except Exception as e:
            print(f"Error terminating process {process.pid}: {e}")

    # ... other cleanup or shutdown tasks ...

    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)











if __name__ == '__main__':
    '''
    You need to reorganize content in these markdown files. Goals: 1) most important: information should not be lost; preserve all details; 2) some heading names are wrong. They don't reflect content. Fix them; 3) make it more readable by using adding heading levels, rewriting, adding content/explanation, etc. as deemed necessary; 4) remove garbage text like copyright notices. Replace them if needed;


    You need to reorganize content in these markdown files. Goals: 1) most important: information should not be lost; preserve all details; 2) some heading names are wrong. They don't reflect content. Fix them; 3) remove garbage text like copyright notices. Replace them if needed; 4) Mild effect: make it more readable by using adding heading levels, rewriting, adding content/explanation, etc. as deemed necessary. Avoid excessive bullet points or excessively small paragraphs. Limit doing this;  5) Elaborate and add content where deemed necessary;
    '''

    app.run(debug=True)