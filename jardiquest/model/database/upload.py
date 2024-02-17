# upload a file from a request
import os

from flask import flash

from jardiquest.setup_flask import ALLOWED_EXTENSIONS, UPLOAD_FOLDER


def upload_file(request, path, filename_stored):
    if 'file' not in request.files:
        flash('Aucun fichier trouvé')
        return False
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('Aucun fichier sélectionné')
        return False

    if file and allowed_file(file.filename):
        file.save(os.path.join(UPLOAD_FOLDER, path, filename_stored))
        return True
    return False


def delete_file(path, filename):
    os.remove(os.path.join(path, filename))


def file_exist(path, filename):
    return os.path.isfile(os.path.join(path, filename))


def allowed_file(filename):
    return '.' in filename \
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
