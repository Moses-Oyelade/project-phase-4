#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():
    Restaurant.query.delete()
    Pizza.query.delete()
    RestaurantPizza.query.delete()
    
    sottocasa_nyc = Restaurant(
        id= 1,
        name= "Sottocasa NYC",
        address= "298 Atlantic Ave, Brooklyn, NY 11201",
    )

    pizzarte = Restaurant(
        id = 2,
        name= "PizzArte",
        address= "69 W 55th St, New York, NY 10019",
    )
    
    db.session.add_all([sottocasa_nyc, pizzarte])
    db.session.commit()
    
    
    cheese = Pizza(
        id = 1,
        name= "Cheese",
        ingredients= "Dough, Tomato Sauce, Cheese",
        )
    
    pepperoni= Pizza(
        id=2,
        name= "Pepperoni",
        ingredients= "Dough, Tomato Sauce, Cheese, Pepperoni",
    )
    
    db.session.add_all([cheese, pepperoni])
    db.session.commit()
    
    price_a = RestaurantPizza(
        price = 4, 
        pizza_id = 1,
        restaurant_id = 2,
    )
    price_b = RestaurantPizza(
        price = 20, 
        pizza_id = 2,
        restaurant_id = 2,
    )
    price_c = RestaurantPizza(
        price = 15, 
        pizza_id = 1,
        restaurant_id = 1,
    )
    price_d = RestaurantPizza(
        price = 25, 
        pizza_id = 2,
        restaurant_id = 1,
    )
    db.session.add_all([price_a, price_b, price_c, price_d])
    db.session.commit()