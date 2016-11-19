# connects posts blueprint to main app
from flask import Blueprint

posts = Blueprint('posts', __name__, template_folder='templates')

import views
