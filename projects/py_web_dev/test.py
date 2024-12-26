import subprocess
import requests
import time
import signal
import os, sys
import argparse
import time

fl_process, da_process = ((subprocess.Popen(['echo "dummy init"'], shell=True)),
                          (subprocess.Popen(['echo "dummy init"'], shell=True)))

def signal_handler (signal, frame):
    print("\nSignal received. Shutting down...")

    global fl_process, da_process
    (subprocess.Popen(f'kill -9 {fl_process.pid}', shell=True))
    (subprocess.Popen(f'kill -9 {da_process.pid}', shell=True))

    sys.exit(0)

def start_app ():
    global fl_process, da_process
    fl_process, da_process = ((subprocess.Popen (['python3 ./app.py'], shell=True)),
                  (subprocess.Popen (['python3 ./dash_dashboard.py'], shell=True)))


def stop_app ():
    global fl_process, da_process
    os.kill(fl_process.pid, signal.SIGTERM)
    os.kill(da_process.pid, signal.SIGTERM)
    fl_process.wait()
    da_process.wait()


def send_get_requests(url):
    try:
        response1 = requests.get(url)
        response2 = requests.get(url)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def send_post_requests (url):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

    payload = {
        "id0": 11,
        "id1": 22,
        "username0": "abcd",
        "username1": "vwxy",
        "email0": "user0@",
        "email1": "user1@"
    }

    try:
        response1 = requests.post(url, json=payload, headers=headers)
        response2 = requests.post(url, json=payload, headers=headers)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def test_path_0 ():
    url=("http://127.0.0.1:8156/prx")

    try:
        send_get_requests(url)
    finally:
        stop_app()

def test_path_1 ():
    url = ("http://127.0.0.1:8156/xrv")

    try:
        send_post_requests(url)
    finally:
        stop_app()

def test_path_2 ():
    url=("http://127.0.0.1:8156/comm")

    try:
        send_get_requests(url)
    finally:
        stop_app()



def test_path_generic (no):
    if (no==-1):
        pass
    if (no==0):
        test_path_0 ()
    if (no==1):
        test_path_1 ()
    if (no==2):
        test_path_2 ()


if __name__ == "__main__":
    parser = argparse.ArgumentParser ()
    parser.add_argument("path", type=int, help="path requested")
    args = parser.parse_args()
    path = args.path

    start_app()
    time.sleep(4)
    test_path_generic (path)
    #save = (subprocess.Popen(['python3 ./save_dash.py'], shell=True))

    signal.signal (signal.SIGINT, signal_handler)
    signal.pause()
