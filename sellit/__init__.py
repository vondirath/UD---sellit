# [BEGIN IMPORTS]
from flask import Flask
from flask_uploads import (patch_request_class,
            configure_uploads, IMAGES, UploadSet)
from posts import posts
import os
from auth import auth
# [END IMPORTS]

# defined app
app = Flask(__name__, static_folder='static')
app.register_blueprint(posts, url_prefix='/posts')
app.register_blueprint(auth, url_prefix='/auth')
# config showing where files are going to be saved
app.config['UPLOADED_PHOTOS_DEST'] = 'sellit/static/upload/photos'
photos = UploadSet('photos', IMAGES)
# limits uploaded files to 6mb
patch_request_class(app, 6 * 1024 * 1024)
# load config for upload set
configure_uploads(app, photos)
