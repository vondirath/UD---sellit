from flask_uploads import UploadSet, IMAGES, send_from_directory
from sellit import app
from sellitdata import Posts, Base
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from datetime import datetime
from werkzeug.utils import secure_filename
import os

engine = create_engine('sqlite:///sellitdata.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'webp'])

# single collection of files declared
photos = UploadSet('photos', IMAGES)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# helper to find a post
def findpost(post):
    post_to_find = session.query(Posts).filter_by(id=post).one()
    return post_to_find

# helper to find path of photo
def photopath(post):
    path_to_find = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], post.post_img_path)
    return path_to_find

@app.route('/')
@app.route('/main/')
def mainPage():
    # will query posts so newest comes first
    posts = session.query(Posts).order_by('time_created desc')
    return render_template('index.html', posts=posts )

# route includes get and post request
@app.route('/post/new/', methods=['GET','POST'])
def newPost():
    if request.method == 'POST' and 'photo' in request.files:
        # requests photo
        file = request.files['photo']
        # makes sure file was selected
        if file.filename == '':
            flash('No selected image')
            return redirect(request.url)
        if request.form['title'].strip() == '':
            flash('No title entered')
            return redirect(request.url)
        if request.form['description'].strip() == '':
            flash('No description entered')
            return redirect(request.url)
        if request.form['price'].strip() == '':
            flash('No price entered')
            return redirect(request.url)
        # grabs photo extension
        ext = str(file.filename.rsplit(('.'), 1)[1])
        # replaces file name with serialized version
        file.filename = str(uuid4()) + '.' + ext
        # default server time for database entry
        server_default = datetime.now()
        # makes sure file extension is allowed
        if file and allowed_file(file.filename):
            # returns a secure filename if it did not properly serialize
            filename = secure_filename(file.filename)
            photos.save(file)
            newPost = Posts(
                            title = request.form['title'],
                            description = request.form['description'],
                            price = request.form['price'],
                            post_img_path = str(filename),
                            time_created = server_default
                            )
            session.add(newPost)
            session.commit()
            flash("Posted new item!")
            return redirect(url_for('mainPage'))
        else:
            flash('Incorrect file format')
            return redirect(request.url)
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
        # makes sure incoming information is not empty.
        if editedPost.title.strip() == '':
            flash('No title entered')
            return redirect(request.url)
        if editedPost.description.strip() == '':
            flash('No description entered')
            return redirect(request.url)
        if editedPost.price.strip() == '':
            flash('No price entered')
            return redirect(request.url)
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
        file = request.files['photo']
        if file.filename == '':
            flash('No Selected Image')
            return redirect(request.url)
        # grabs photo extension
        ext = str(file.filename.rsplit(('.'), 1)[1])
        # replaces file name with serialized version
        file.filename = str(uuid4()) + '.' + ext
        # checks if extension is allowed
        if file and allowed_file(file.filename):
            # deletes old file if new file is allowed and secure
            filename = secure_filename(file.filename)
            try:
                os.remove(old_file_path)
            except:
                flash("Error replacing file")
                redirect(request.url)
            photos.save(file)
            post.post_img_path = str(filename)
            session.add(post)
            session.commit()
            flash("Edit successful!")
            return redirect(url_for('mainPage'))
        else:
            flash ('Incorrect Format')
            return redirect(request.url)
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
        flash("post Delete successful!")
        return redirect(url_for('mainPage'))
    else:
        return render_template('deletepost.html', post=post, post_id=post_id)


