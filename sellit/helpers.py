import os


# defines app photo directory for uploads from the position of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTO_DIR = BASE_DIR + '/static/upload/photos/'


# allowed extensions for post image uploads
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'webp', 'png'])
