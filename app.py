import logging
logging.basicConfig(filename="record.log", level=logging.DEBUG, format='%(levelname)s:%(name)s: [%(asctime)s] - - %(message)s')
import os
from flask import Flask, render_template, request
import yaml
import process_file

# TODO: Edit the HTML template file
# TODO: Move data file to static
# TODO: Generate updated date.

app = Flask(__name__)

# Open configuration file
with open("process_file.yml", "r") as ymlfile:
    file_params = yaml.safe_load(ymlfile)

app.config['UPLOAD_FOLDER'] = file_params["Dir"]["uploads"]
app.config['WORKING_DIR'] = file_params["Dir"]["working_dir"]
app.config['OUTPUT'] = file_params["Dir"]["output"]
app.config['ALLOWED_FILES'] = {file_params[d]["file_name"] for d in file_params if "file_name" in file_params[d]}

# Set correct directory
os.chdir(app.config["WORKING_DIR"])

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['OUTPUT']):
    os.makedirs(app.config['OUTPUT'])

# Generate Files
def process_excel_js(f_name):
    """
    Convert the information to js file
    """
    # Search for the file params
    file_param = {}
    for file_type in file_params:
        if "file_name" in file_params[file_type] and file_params[file_type]["file_name"] == f_name:
            file_param = file_params[file_type]
    if len(file_param) != 0:
        process_file.generate_out(file_param, "uploads")
    else:
        app.logger.warning("File Parameters not Found")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_FILES']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file and file.filename in app.config["ALLOWED_FILES"]:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        app.logger.info("File %s uploaded succesfully.", file.filename)
        process_excel_js(file.filename) # Call the conversion function
        return "File Uploaded"

    app.logger.warning("File not uploaded. Invalid name/type.")
    return 'Invalid file type'

if __name__ == '__main__':
    app.run(debug=True)