from utils import *
PPROCESS = []

app = Flask (__name__)

def sigchld_handler(signum, frame):
    try:
        while True:
            pid, status = os.waitpid(-1, os.WNOHANG)  # Non-blocking wait
            if pid == 0:
                break  # No more child processes have exited
            print(f"Child process {pid} terminated with status {status}")
    except OSError:
        pass  # Ignore errors if no child processes have exited

signal.signal(signal.SIGCHLD, sigchld_handler)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')

    # Terminate child processes
    for process in PPROCESS:
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



def worker_function2():
    print("Worker2 process started")
    time.sleep(10)  # Simulate long-running process
    print("Worker2 process finished")

def worker_function():
    print("Worker process started")
    process = multiprocessing.Process(target=worker_function2,
                                      args=())
    process.start()
    PPROCESS.append(process)
    time.sleep(10)  # Simulate long-running process
    print("Worker process finished")



@app.route('/')
def hello():
    process = multiprocessing.Process(target=worker_function,
                                      args=())
    process.start()
    PPROCESS.append(process)
    return 'Hello, World!'




if __name__ == '__main__':
    # Create and start a child process (example)
    process = multiprocessing.Process(target=worker_function)
    process.start()
    PPROCESS.append(process)

    app.run(debug=True, port=5000)