# [BEGIN IMPORTS]
from flask import Flask
from flask_uploads import configure_uploads, patch_request_class
#[END IMPORTS]

# defined app
app = Flask(__name__, static_folder='static')

#imports app routing
from views import *

# config showing where files are going to be saved
app.config['UPLOADED_PHOTOS_DEST'] = 'sellit/static/upload/photos'
# limits uploaded files to 6mb
patch_request_class(app, 6 * 1024 * 1024)
# load config for upload set
configure_uploads(app, photos)
