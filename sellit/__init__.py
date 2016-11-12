# [BEGIN IMPORTS]
from flask import Flask
from flask_uploads import configure_uploads, patch_request_class
from testbblue import simple_page
from posts import posts
#[END IMPORTS]

# defined app
app = Flask(__name__, static_folder='static')
app.register_blueprint(simple_page)
app.register_blueprint(posts, url_prefix='/posts')

#imports app routing
from views import *

# config showing where files are going to be saved
app.config['UPLOADED_PHOTOS_DEST'] = 'sellit/static/upload/photos'
# limits uploaded files to 6mb
patch_request_class(app, 6 * 1024 * 1024)
# load config for upload set
configure_uploads(app, photos)
