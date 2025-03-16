import os
import subprocess

from flask import Flask, render_template, jsonify, request, Request

from docx import Document
from docx.shared import Inches, Pt, RGBColor

ROOT="/tmp/rootdir/"

inits = [
    "mkdir -p {ROOT}",
    "cd {ROOT}",
    "sudo apt install python3 python3-venv",
    "python3 -m venv venv",
    "source venv/bin/activate",
    "mkdir -p ./static",
    "mkdir -p ./static/image",
    "mkdir -p ./templates",
    'python3 gdrive_im.py',
    'python3 gdrive_te.py'
]

[subprocess.Popen (x, shell=True).wait() for x in inits]


PATH_APP = ROOT
PATH_STATIC = PATH_APP+"static/"
PATH_TEMPLATE = PATH_APP+"templates/"
IMAGE_DIR = PATH_STATIC+"image/"


app = Flask(__name__, static_folder=PATH_STATIC, template_folder=PATH_TEMPLATE)



@app.route ("/comm", methods=["GET", "POST"])
def compile_image ():
    image_list_rel = [os.path.join ("/static/image/", im) for im in os.listdir(IMAGE_DIR) if im.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    image_list_rel = sorted (image_list_rel)
    print (image_list_rel)
    image_list_abs = [os.path.join(IMAGE_DIR, im) for im in os.listdir(IMAGE_DIR) if
                      im.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    doc = Document()
    section = doc.sections[0]
    margins = {
        'top': 0.4,  # 1 inch
        'bottom': 0.4,  # 1 inch
        'left': 0.4,  # 1 inch
        'right': 0.4  # 1 inch
    }
    section.top_margin = Inches(margins['top'])
    section.bottom_margin = Inches(margins['bottom'])
    section.left_margin = Inches(margins['left'])
    section.right_margin = Inches(margins['right'])


    if (request.method=="GET"):
        return render_template("index_im.html", images=image_list_rel)

    if (request.method=="POST"):
        for im in image_list_rel:

            para = doc.add_heading(level=1)
            run = para.add_run (request.form.get (im, ""))
            run.font.size = Pt (20)
            run.font.color.rgb = RGBColor (0, 0, 0)
            run.font.bold = True

            doc.add_picture (PATH_APP[:-1]+im, width=Inches (3.0))


        doc.save (PATH_STATIC+"generated_file.docx")

        return render_template ("results_im.html")


@functions_framework.http
def entry (request: Request) -> str:
    # Forward the request to the Flask app
    with app.test_request_context(request.url, request.method, request.get_data(), request.headers):
        response = app.full_dispatch_request()
        return response.get_data(as_text=True), response.status_code

if (__name__=="__main__"):
    app.run (debug=True, port=8156, host="127.0.0.1")