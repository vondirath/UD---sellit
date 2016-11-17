from flask_uploads import IMAGES, UploadSet, send_from_directory
from ..posts import posts
from ..auth import auth
from sellit.database import Posts, Base, User
from flask import (Flask, render_template, request, redirect,
 url_for, flash, jsonify )
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from sellit.helpers import PHOTO_DIR, ALLOWED_EXTENSIONS
# for log in checks
from flask import session as login_session

engine = create_engine('sqlite:///sellitdata.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

photos = UploadSet('photos', IMAGES)

# checks zip input is an actual zip
def checkZip(zipcode):
    # if it cannot convert to integer it fails
    try:
        zipcode = int(zipcode)
        # makes sure its the proper length
        if len(str(abs(zipcode))) == 5:
            return True
        else:
            return False
    except:
        return False

# helter to determine if filename has correct extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# helper to find a post
def findpost(post):
    post_to_find = session.query(Posts).filter_by(id=post).one()
    return post_to_find

# shows JSON list of posts
@posts.route('/post/JSON')
def postsJSON():
    postlist = session.query(Posts).all()
    return jsonify(Posts=[i.serialize for i in postlist])


@posts.route('/')
@posts.route('/main/')
def mainPage():
    posts = session.query(Posts).order_by(desc('time_created'))
    if 'username' not in login_session:
    # will query posts so newest comes first
        return render_template('index.html', posts=posts)
    else:
        username = login_session['username']
        return render_template('index.html', posts=posts, username=username)


# route includes get and post request
@posts.route('/post/new/', methods=['GET','POST'])
def newPost():
    if 'username' not in login_session:
        return redirect('/auth/login')
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
        if checkZip(request.form['zipcode']):
            zipcode = str(abs(int(request.form['zipcode'])))
        else:
            flash("Invalid or no zip entered")
            return redirect(request.url)
        # grabs photo extension
        ext = str(file.filename.rsplit(('.'), 1)[1])
        # replaces file name with serialized version
        file.filename = str(uuid4()) + '.' + ext
        # makes sure file extension is allowed
        if file and allowed_file(file.filename):
            # returns a secure filename if it did not properly serialize
            filename = secure_filename(file.filename)
            photos.save(file)
            newPost = Posts(
                            title=request.form['title'],
                            description=request.form['description'],
                            price=request.form['price'],
                            img_name=filename,
                            time_created=datetime.now(),
                            user_id=login_session['user_id'],
                            zipcode=zipcode
                            )
            session.add(newPost)
            session.commit()
            flash("Posted new item!")
            return redirect(url_for('posts.mainPage'))
        else:
            flash('Incorrect file format')
            return redirect(request.url)
    else:
        return render_template('newpost.html')

@posts.route('/post/<int:post_id>/', methods=['GET', 'POST'])
def viewPost(post_id):
    if 'username' not in login_session:
        return redirect('/auth/login')
    else:
        post = findpost(post_id)
        return render_template('viewpost.html', post=post)


@posts.route('/post/<int:post_id>/edit/', methods=['GET', 'POST'])
def editPost(post_id):
    if 'username' not in login_session:
        flash('Please log in')
        return redirect('/auth/login')
    # selects passed in post and renders template
    editedPost = findpost(post_id)
    if editedPost.user_id != login_session['user_id']:
        flash('Unauthorized to edit post')
        return redirect(url_for('posts.mainPage'))
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
        return redirect(url_for('posts.viewPost', post_id=post_id))
    else:
        if 'username' not in login_session:
            return redirect('/auth/login')
        else:
            return render_template('editpost.html', post=editedPost)

@posts.route('/post/<int:post_id>/edit/changephoto', methods=['GET', 'POST'])
def changePic(post_id):
    if 'username' not in login_session:
        return redirect('/auth/login')
    post = findpost(post_id)
    if post.user_id != login_session['user_id']:
        flash('Unauthorized to change post.')
        return redirect(url_for('posts.mainPage'))
    if request.method == 'POST' and 'photo' in request.files:
        old_file_path = PHOTO_DIR + post.img_name
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
            post.img_name = str(filename)
            session.add(post)
            session.commit()
            flash("Edit successful!")
            return redirect(url_for('posts.mainPage'))
        else:
            flash ('Incorrect Format')
            return redirect(request.url)
    else:
        if 'username' not in login_session:
            return redirect('/auth/login')
        else:
            return render_template('editpic.html', post=post)


@posts.route('/post/<int:post_id>/delete/', methods=['GET', 'POST'])
def deletePost(post_id):
    # selects passed in post and renders template
    post = findpost(post_id)
    if 'username' not in login_session:
        return redirect('/auth/login')
    if post.user_id != login_session['user_id']:
        flash('Unauthorized to change post.')
        return redirect(url_for('posts.mainPage'))
    if request.method == 'POST':
        # sets image to be deleted
        file_path = PHOTO_DIR + post.img_name
        try:
            # uses os.remove to remove file
            os.remove(file_path)
        except:
            # if error during delete preserves post and returns to mainpage
            flash("Error deleting image file or it is already deleted")
            redirect(url_for('posts.mainPage'))
        session.delete(post)
        session.commit()
        flash("post Delete successful!")
        return redirect(url_for('posts.mainPage'))
    else:
        if 'username' not in login_session:
            return redirect('/auth/login')
        else:
            return render_template('deletepost.html', post=post, post_id=post_id)
