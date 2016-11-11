# [BEGIN IMPORTS]
# main app related
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# for image uploading
from flask_uploads import UploadSet, configure_uploads, IMAGES, send_from_directory
# database related
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sellitdata import Base, Posts, Questions
import os
#[END IMPORTS]


app = Flask(__name__)

# single collection of files declared
photos = UploadSet('photos', IMAGES)
# config showing where files are going to be saved
app.config['UPLOADED_PHOTOS_DEST'] = 'static/upload/photos/'
# load config for upload set
configure_uploads(app, photos)


engine = create_engine('sqlite:///sellitdata.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# helper to find a post
def findpost(post):
    post_to_find = session.query(Posts).filter_by(id=post).one()
    return post_to_find

# helper to find path of photo
def photopath(post):
    path_to_find = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], post.post_img_path)
    return path_to_find


# helper for url_for in template
@app.route('/static/upload/photos/<filename>')
def post_img(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


# main page route
@app.route('/')
@app.route('/main/')
def mainPage():
    # will query posts so newest comes first
    posts = session.query(Posts).order_by('time_created')
    return render_template('index.html', posts=posts )


# route includes get and post request
@app.route('/post/new/', methods=['GET','POST'])
def newPost():
    if request.method == 'POST' and 'photo' in request.files:
        # photos is determined by app.config and save is a flask_uploads command
        filename = photos.save(request.files['photo'])
        # sets date to servers date
        server_default = datetime.now()
        newPost = Posts(
                        title = request.form['title'],
                        description = request.form['description'],
                        price = request.form['price'],
                        # saves filename
                        post_img_path = str(filename),
                        # sets date to server date
                        time_created = server_default
                        )
        session.add(newPost)
        session.commit()
        flash("Posted new item!")
        return redirect(url_for('mainPage'))
    else:
        return render_template('newpost.html')


@app.route('/post/<int:post_id>/', methods=['GET', 'POST'])
def viewPost(post_id):
    post = findpost(post_id)
    return render_template('viewpost.html', post=post)


@app.route('/post/<int:post_id>/edit/', methods=['GET', 'POST'])
def editPost(post_id):
    # selects passed in post and renders template
    editedPost = findpost(post_id)
    if request.method == 'POST':
        # checks every form POST if one is not changed it wont be modified from original file.
        if request.form['title']:
            editedPost.title = request.form['title']
        if request.form['description']:
            editedPost.description = request.form['description']
        if request.form['price']:
            editedPost.price = request.form['price']
        session.add(editedPost)
        session.commit()
        flash("Post edited!")
        return redirect(url_for('viewPost', post_id=post_id))
    else:
        return render_template('editpost.html', post=editedPost)

@app.route('/post/<int:post_id>/edit/changephoto', methods=['GET', 'POST'])
def changePic(post_id):
    post = findpost(post_id)
    if request.method == 'POST' and 'photo' in request.files:
        old_file_path = photopath(post)
        try:
            os.remove(old_file_path)
        except:
            flash("Error replacing file")
            redirect(url_for('mainPage'))
        newfilename = photos.save(request.files['photo'])
        post.post_img_path = str(newfilename)
        session.add(post)
        session.commit()
        flash("Edit successful!")
        return redirect(url_for('mainPage'))
    else:
        return render_template('editpic.html', post=post)

@app.route('/post/<int:post_id>/delete/', methods=['GET', 'POST'])
def deletePost(post_id):
    # selects passed in post and renders template
    post = findpost(post_id)
    if request.method == 'POST':
        # sets image to be deleted
        file_path = photopath(post)
        try:
            # uses os.remove to remove file
            os.remove(file_path)
        except:
            # if error during delete preserves post and returns to mainpage
            flash("Error deleting image file or it is already deleted")
            redirect(url_for('mainPage'))
        session.delete(post)
        session.commit()
        flash("Delete successful!")
        return redirect(url_for('mainPage'))
    else:
        return render_template('deletepost.html', post=post, post_id=post_id)

# wont work unless ran from this file
if __name__ == '__main__':
    # for flash messaging.
    app.secret_key = 'super_secret_key'
    # reloads itself when code is changed
    app.debug = True
    # listens to all IP addresses for debugging
    app.run(host='0.0.0.0', port = 9000)