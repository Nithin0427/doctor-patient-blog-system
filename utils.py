import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_image(filename):
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config.get('ALLOWED_IMAGE_EXTENSIONS', set())

def save_image(file_obj):
    if not file_obj or file_obj.filename == '':
        return None
    if not allowed_image(file_obj.filename):
        return None
    filename = secure_filename(file_obj.filename)
    filename = f"{uuid.uuid4().hex}_{filename}"
    dest_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(dest_folder, exist_ok=True)
    dest = os.path.join(dest_folder, filename)
    file_obj.save(dest)
    return filename
