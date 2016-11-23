# [BEGIN IMPORTS]
import os

from flask import Flask, url_for, redirect
from flask_uploads import (IMAGES, UploadSet, configure_uploads,
                           patch_request_class)

from auth import auth
from main import main
from posts import posts

# [END IMPORTS]

# defined app
app = Flask(__name__, static_folder='static')
app.register_blueprint(posts, url_prefix='/posts')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(main, url_prefix='/main')
# config showing where files are going to be saved
app.config['UPLOADED_PHOTOS_DEST'] = 'sellit/static/upload/photos'
photos = UploadSet('photos', IMAGES)
# limits uploaded files to 6mb
patch_request_class(app, 6 * 1024 * 1024)
# load config for upload set
configure_uploads(app, photos)

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('main.welcomePage'))
