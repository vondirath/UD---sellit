from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sellitdata import Base, Posts, Questions

engine = create_engine('sqlite:///sellitdata.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# main page route
@app.route('/')
@app.route('/main/')
def mainPage():
    # will query posts so newest comes first
    posts = session.query(Posts).order_by('time_created desc')
    return render_template('index.html', posts=posts )


# route includes get and post request
@app.route('/post/new/', methods=['GET','POST'])
def newPost():
    if request.method == 'POST':
        server_default = datetime.now()
        newPost = Posts(
                        title = request.form['title'], 
                        description = request.form['description'], 
                        price = request.form['price'], 
                        post_img_path = request.form['post_img_path'],
                        time_created = server_default
                        )
        session.add(newPost)
        session.commit()
        flash("New post!")
        return redirect(url_for('mainPage'))
    else:
        return render_template('newpost.html')


@app.route('/post/<int:post_id>/')
def viewPost(post_id):
    # selects passed in post and renders template
    post = session.query(Posts).filter_by(id=post_id).one()
    return render_template('viewpost.html', post=post)


@app.route('/post/<int:post_id>/edit/', methods=['GET', 'POST'])
def editPost(post_id):
    # selects passed in post and renders template
    editedPost = session.query(Posts).filter_by(id=post_id).one()
    if request.method == 'POST':
        # checks every form POST if one is not changed it wont be modified from original file.
        if request.form['title']:
            editedPost.title = request.form['title']
        if request.form['description']:
            editedPost.description = request.form['description']
        if request.form['image']:
            editedPost.post_img_path = request.form['image']
        if request.form['price']:
            editedPost.price = request.form['price']
        session.add(editedPost)
        session.commit()
        flash("Edit successful!")
        return redirect(url_for('viewPost', post_id=post_id))
    else:
        return render_template('editpost.html', post=editedPost)


@app.route('/post/<int:post_id>/delete/', methods=['GET', 'POST'])
def deletePost(post_id):
    # selects passed in post and renders template
    post = session.query(Posts).filter_by(id=post_id).one()
    if request.method == 'POST':
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