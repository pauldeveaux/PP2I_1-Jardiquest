from flask import Blueprint

# allow to create path in multiple file
# useful to let app.py found the path in the controller folder
app = Blueprint('controller', __name__)

# to create a new file of path import him here
# please ignore the 'PEP 8: E402' warning ( create an import partial if you move them to the top file )
from .auth import *
from .status_error import *
from .common import *
from .quest import *
from .account import *
from .handle_garden import *
from .garden import *
from .market import *
from .suggestion import *
from .blog import *
