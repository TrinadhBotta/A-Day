from flask import Flask, request, jsonify
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from configparser import ConfigParser
from elasticsearch_client.elastic_client import send_data_to_index

app = Flask(__name__)

# Define the folder where uploaded images will be stored
config = ConfigParser()
config.read('config.ini')

UPLOAD_FOLDER = config.get('DEFAULT', 'UPLOAD_FOLDER')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def validate_data(data):
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")
    if 'datetime' not in data or 'Description' not in data:
        raise ValueError("Data must contain 'datetime' and 'Description' keys")

ALLOWED_EXTENSIONS = set({'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'heic'})

def allowed_file(filename):
    return ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

print('hiiiiiii')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file and allowed_file(file.filename):
            current_year_month = datetime.now().strftime('%Y%m%d')
            filename = secure_filename(file.filename)
            file_format = '.'+filename.split('.')[-1]
            filename = secure_filename(current_year_month)

            # Delete existing files with the same filename
            for existing_file in os.listdir(app.config['UPLOAD_FOLDER']):
                if existing_file.startswith(filename):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], existing_file))
                    app.logger.info(f"Deleted existing file: {existing_file}")
            
            filename = filename + file_format

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            data = request.form.to_dict()
            validate_data(data)

            send_data_to_index(data)
            return jsonify({'message': 'File uploaded successfully'})
        else:
            return jsonify({'error': 'Invalid file type'})
    except Exception as e:
        app.logger.error(f'Error occurred during file upload: {e}')
        return jsonify({'error': 'Failed to upload file'})

if __name__ == '__main__':
    app.run(debug=True)
