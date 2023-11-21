#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
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

@app.route('/restaurants', methods=['GET'])
def restaurants():
    if request.method == 'GET':
        restaurants = Restaurant.query.all()

        response = make_response(
            jsonify([restaurant.to_dict(rules=('-pizzas',)) for restaurant in restaurants]),
            200
        )

        return response

# @app.route('/restaurants', methods =['GET'])
# def restaurant():
#     if request.method == 'GET':
#         restaurants = [] 
#         for restaurant in Restaurant.query.all():
#             restaurant_dict = restaurant.to_dict()
#             restaurants.append(restaurant_dict)
#     return make_response( jsonify(restaurant_dict(rules=('-pizzas',))), 200 )

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    
    if restaurant == None:
        response_body = {
            "error": "Restaurant not found"
        }
        return make_response( response_body, 404 )
    else:
        if  request.method == 'GET':
            
            restaurant_serialized = restaurant.to_dict()
            return make_response( restaurant_serialized, 200 )
        elif request.method == 'DELETE':
            db.session.delete(restaurant)
            db.session.commit()
            
            response_body = {
                "delete_successful": True,
                "message": "Restaurant deleted."
            }
            return make_response( response_body, 200 )

@app.route('/pizzas', methods = ['GET'])
def pizza():
    if request.method == 'GET':
        pizza = [pizza.to_dict() for pizza in Pizza.query.all()]
        return make_response( jsonify(pizza), 200 )
    
@app.route('/restaurant_pizzas', methods = ['GET', 'POST'])
def restaurant_pizzas():
    restaurant_pizzas = [restaurant_pizza.to_dict() for restaurant_pizza in RestaurantPizza.query.all()]
    if not restaurant_pizzas:
        response_body = {"errors": ["validation errors"]}
        return make_response( response_body, 404 )
    else:
        if request.method == 'GET':
            return make_response(jsonify(restaurant_pizzas), 200 )
        
        elif request.method == 'POST':
            new_restaurant_pizza = RestaurantPizza(
                price=request.form.get("price"),
                pizza_id=request.form.get("pizza_id"),
                restaurant_id=request.form.get("restaurant_id"),
            )
            db.session.add(new_restaurant_pizza)
            db.session.commit()
            
            restaurant_pizza_dict= new_restaurant_pizza.to_dict()
            return make_response( restaurant_pizza_dict, 201 )

if __name__ == '__main__':
    app.run(port=5555, debug=True)
