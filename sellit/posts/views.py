import os
from datetime import datetime
from uuid import uuid4

from flask import session as login_session
# for log in checks
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   url_for)
from flask_uploads import IMAGES, UploadSet, send_from_directory
from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename

from sellit.database import Base, Posts, User, Store
from sellit.helpers import ALLOWED_EXTENSIONS, PHOTO_DIR

from ..auth import auth
from ..posts import posts

engine = create_engine('sqlite:///sellitdata.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


photos = UploadSet('photos', IMAGES)


# checks zip input is an actual zip replace with google api when over https
def checkZip(zipcode):
    """Checkzip helper takes zipcode and
    determines if it is a number within 5 digits"""
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
    """ compares fileextension to allowed extensions helper """
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# helper to find a post
def findpost(post):
    post_to_find = session.query(Posts).filter_by(id=post).one()
    return post_to_find


# JSON list routes
@posts.route('/post/JSON')
def postsJSON():
    """This returns a JSON for ALL posts"""
    postlist = session.query(Posts).all()
    return jsonify(Posts=[i.serialize for i in postlist])


@posts.route('/store/JSON')
def storeJSON():
    """This returns a JSON for ALL stores"""
    storelist = session.query(Store).all()
    return jsonify(Store=[i.serialize for i in storelist])


@posts.route('/store/<int:store_id>/posts/JSON')
def storecontentJSON(store_id):
    """This returns a JSON of all POSTS in a STORE"""
    store = session.query(Store).filter_by(id=store_id).one()
    posts = session.query(Posts).filter_by(
        store_id=store_id).all()
    return jsonify(Posts=[i.serialize for i in posts])


@posts.route('/')
def welcomePage():
    """ Welcome Page Route """
    return render_template('splash.html')


@posts.route('/main/')
def mainPage():
    """ Main page route showing all posts """
    posts = session.query(Posts).order_by(desc('time_created'))
    return render_template('index.html', posts=posts,
                           login_session=login_session)


@posts.route('/stores/')
def showStores():
    """ Store route showing and allowing creation of stores """
    stores = session.query(Store).order_by(asc(Store.name))
    if 'username' not in login_session:
        return redirect('/auth/login')
    else:
        return render_template('stores.html', stores=stores,
                               login_session=login_session)


@posts.route('/newstore/', methods=['GET', 'POST'])
def newStore():
    """ new store creation route """
    if 'username' not in login_session:
        return redirect('/auth/login')
    if request.method == 'POST':
        if request.form['name'].strip() == '':
            flash('No Name entered')
            return redirect(request.url)
        newStore = Store(
            name=request.form['name'], user_id=login_session['user_id']
        )
        session.add(newStore)
        flash("New store %s created!" % newStore.name)
        session.commit()
        return redirect(url_for('posts.showStores'))
    else:
        return render_template('newstore.html')


@posts.route('/store/<int:store_id>/edit', methods=['GET', 'POST'])
def editStore(store_id):
    """ Route to edit a store  """
    if 'username' not in login_session:
        return redirect('/auth/login')
    editedStore = session.query(Store).filter_by(id=store_id).one()
    if request.method == 'POST':
        if editedStore.user_id != login_session['user_id']:
            flash('Unauthorized to edit store')
            return redirect(url_for('posts.mainPage'))
        if request.form['name'].strip() == '':
            flash('No Name entered')
            return redirect(request.url)
        editedStore.name = request.form['name']
        session.add(editedStore)
        session.commit()
        flash("Store edited!")
        return redirect(url_for('posts.viewStore', store_id=store_id))
    else:
        return render_template('editstore.html', store=editedStore)


# does not delete posts associated with store
@posts.route('/store/<int:store_id>/delete', methods=['GET', 'POST'])
def deleteStore(store_id):
    """ Route to delete a store """
    if 'username' not in login_session:
        flash('Please log in')
        return redirect('/auth/login')
    # selects passed in post and renders template
    deletedStore = session.query(Store).filter_by(id=store_id).one()
    if deletedStore.user_id != login_session['user_id']:
        flash('Unauthorized to edit store')
        return redirect(url_for('posts.mainPage'))
    if request.method == 'POST':
        session.delete(deletedStore)
        session.commit()
        flash("store Delete successful!")
        return redirect(url_for('posts.mainPage'))
    else:
        return render_template('deletestore.html', store_id=store_id,
                               store=deletedStore)


@posts.route('/store/<int:store_id>')
def viewStore(store_id):
    """ Route to view a store by its ID """
    store = session.query(Store).filter_by(id=store_id).one()
    creator = getUserInfo(store.user_id)
    posts = session.query(Posts).filter_by(
        store_id=store_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return redirect(url_for('auth.showLogin'))
    else:
        return render_template('viewstore.html',
                               store=store,
                               creator=creator,
                               posts=posts,
                               login_session=login_session)


# route includes get and post request
@posts.route('/post/<int:store_id>/new/', methods=['GET', 'POST'])
def newPost(store_id):
    """ Creation of a new post in a store by the store ID """
    if 'username' not in login_session:
        return redirect('/auth/login')
    store = session.query(Store).filter_by(id=store_id).one()
    if login_session['user_id'] != store.user_id:
        flash("You are not authorized to post in this store")
        return redirect('/posts/main')
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
        # replace zip with google api when over https
        if checkZip(request.form['zipcode']):
            zipcode = str(abs(int(request.form['zipcode'])))
        else:
            flash("Invalid zip entered")
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
                            user_id=store.user_id,
                            zipcode=zipcode,
                            store_id=store_id
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


@posts.route('/post/<int:post_id>/', methods=['GET'])
def viewPost(post_id):
    """  Route to view a post by its ID  """
    if 'username' not in login_session:
        return redirect('/auth/login')
    else:
        post = findpost(post_id)
        return render_template('viewpost.html', post=post,
                               login_session=login_session)


@posts.route('/post/<int:post_id>/edit/', methods=['GET', 'POST'])
def editPost(post_id):
    """ Route to edit a post taking its ID as an argument """
    if 'username' not in login_session:
        flash('Please log in')
        return redirect('/auth/login')
    # selects passed in post and renders template
    editedPost = findpost(post_id)
    if editedPost.user_id != login_session['user_id']:
        flash('Unauthorized to edit post')
        return redirect(url_for('posts.mainPage'))
    if request.method == 'POST':
        # Form Checks
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
    """ Route to change a picture by its post id  """
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
            flash('Incorrect Format')
            return redirect(request.url)
    else:
        if 'username' not in login_session:
            return redirect('/auth/login')
        else:
            return render_template('editpic.html', post=post)


@posts.route('/post/<int:post_id>/delete/', methods=['GET', 'POST'])
def deletePost(post_id):
    """ Deletes a post by its ID """
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
            return render_template('deletepost.html',
                                   post=post, post_id=post_id)
