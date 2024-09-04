from flask import Flask, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define the upload folder path
UPLOAD_FOLDER = '/home/shachis/Documents/ASU/CSE 535 - Mobile Computing/Project/SmartHomeGestureControl/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        # Construct a secure filename
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "File uploaded successfully", 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

