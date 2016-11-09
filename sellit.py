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
    # restaurants = session.query(Restaurant)
    posts = session.query(Posts)
    return render_template('index.html', posts=posts )

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
        return redirect(url_for('mainPage'))
    else:
        return render_template('newpost.html')

@app.route('/post/<int:post_id>/')
def viewPost(post_id):
    return render_template('viewpost.html', post=post)

@app.route('/post/<int:post_id>/edit/')
def editPost(post_id):
    return render_template('editpost.html')

@app.route('/post/<int:post_id>/delete/')
def deletePost(post_id):
    return render_template('deletepost.html')


# wont work unless ran from this file
if __name__ == '__main__':
    # this should not be visable, for flash messaging.
    app.secret_key = 'super_secret_key'
    # reloads itself when code is changed
    app.debug = True
    # listens to all IP addresses for debugging
    app.run(host='0.0.0.0', port = 9000)