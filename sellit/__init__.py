# [BEGIN IMPORTS]
from flask import Flask
from flask_uploads import patch_request_class, configure_uploads, IMAGES, UploadSet
from testbblue import simple_page
from posts import posts
import os
#[END IMPORTS]

# defined app
app = Flask(__name__, static_folder='static')
app.register_blueprint(simple_page)
app.register_blueprint(posts, url_prefix='/posts')
app.config['UPLOADED_PHOTOS_DEST'] = 'sellit/static/upload/photos'

photos = UploadSet('photos', IMAGES)
# config showing where files are going to be saved
# limits uploaded files to 6mb
patch_request_class(app, 6 * 1024 * 1024)
# load config for upload set
configure_uploads(app, photos)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def photopath(post):
    path_to_find = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], post.post_img_path)
    return path_to_find
