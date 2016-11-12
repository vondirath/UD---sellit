import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PHOTO_DIR = BASE_DIR + '/static/upload/photos/'

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'webp'])