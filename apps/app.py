#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Restaurant GET-POST-DELETE API</h1>'

@app.route('/restaurants', methods =['GET'])
def restaurant():
    if request.method == 'GET':
        restaurants = [restaurant.to_dic() for restaurant in Restaurant.query.all()]
    return make_response( restaurants, 200 )
