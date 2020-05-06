import uuid
from werkzeug.utils import secure_filename
import os

def upload_file(this_file, username):
    main_path = "/static/upload/" + username
    path = "PyGram" + main_path # add full path because utils directory was not a blueprint and not recognize static route
    filename = this_file.filename
    filename = f'{uuid.uuid1()}_{secure_filename(filename)}'
    this_file.save(f'{path}/{filename}')
    return main_path + "/" + filename