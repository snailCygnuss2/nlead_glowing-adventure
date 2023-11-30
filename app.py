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
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_FILES'] = {"Research calls.xlsx", "Research conference calls.xlsx", "Seminars webinars etc.xlsx", "Special issues - call for papers.xlsx"}

# Open configuration file
with open("process_file.yml", "r") as ymlfile:
    file_params = yaml.safe_load(ymlfile)


# Set correct directory
os.chdir(file_params["working_dir"])

# Generate Files
def process_excel_js(f_name):
    """
    Convert the information to js file
    """
    # Search for the file params
    for  param in file_params:
        if file_params[param]["file_name"] == f_name:
            file_param = file_params[param]
    print(file_param)
    process_file.generate_out(file_param, "uploads")

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

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