from flask import render_template
from werkzeug.exceptions import HTTPException


# custom page for status code
def handling_status_error(error: HTTPException):
    return render_template('status/base_status.html', status=error.code, title=error.name, msg=error.description), error.code
