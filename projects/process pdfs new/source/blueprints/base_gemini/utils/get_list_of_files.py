from flask import Flask, request, render_template
from genai_gemini import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# Route to accept directory from user
@app.route('/directory2', methods=['POST'])
def accept_directory2():
    #template: index2.html
    if 'directory' not in request.files:
        return 'No directory selected', 400

    directory = request.files['directory']
    # Assuming you want to print the directory names or handle them in some way
    directory_names = directory.filename
    print(f"Received directory: {directory_names}")

    # Process the directory here (e.g., save it, analyze it, etc.)

    return f"Directory {directory_names} received successfully!"


@app.route('/directory', methods=['POST'])
def accept_directory():
    #template: index.html
    if 'files[]' not in request.files:
        return 'No files selected', 400

    files = request.files.getlist('files[]')

    if not files:
        return 'No files found in the directory', 400

    file_names = [file.filename for file in files]

    # Print file names or handle files here
    print("Files in the directory:")
    for file_name in file_names:
        print(file_name)

    return f"Files received: {', '.join(file_names)}"



if __name__ == '__main__':
    app.run(debug=True)
