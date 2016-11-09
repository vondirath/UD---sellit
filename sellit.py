from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sellitdata import Base, 

engine = create_engine('sqlite:///sellitdata.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def mainPage():
    # restaurants = session.query(Restaurant)
    return render_template('index.html', restaurants=restaurants )

@app.route('/restaurants/new/')
def newRestaurant():
    return render_template('newrestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def viewMenu(restaurant_id):
    return render_template('restaurantmenu.html', restaurant=restaurant, items=items)

@app.route('/restaurants/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    return render_template('editrestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    return render_template('deleterestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/menu/new/')
def addItem(restaurant_id):
    return render_template('additem.html')

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def deleteItem(restaurant_id, menu_id):
    return render_template('deleteitem.html')

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def editItem(restaurant_id, menu_id):
    return render_template('edititem.html')

# wont work unless ran from this file
if __name__ == '__main__':
    # this should not be visable
    app.secret_key = 'super_secret_key'
    # reloads itself when code is changed
    app.debug = True
    # listens to all IP addresses for debugging
    app.run(host='0.0.0.0', port = 9000)