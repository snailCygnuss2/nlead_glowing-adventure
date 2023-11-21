from flask import Flask, render_template, request
import logging
import os


logging.basicConfig(filename="record.log", level=logging.DEBUG, format='%(levelname)s:%(name)s: [%(asctime)s] - - %(message)s')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_FILES'] = {"Research calls.xlsx", "Research conference calls.xlsx", "Seminars webinars etc.xlsx", "Special issues - call for papers.xlsx"}

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
        app.logger.info(f"File {file.filename} uploaded succesfully.")
        return 'File uploaded successfully'

    app.logger.warning("File not uploaded. Invalid name/type.")
    return 'Invalid file type'

if __name__ == '__main__':
    app.run(debug=True)