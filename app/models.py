from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
    
    # serialize_rules = ('-restaurant_pizzas.restaurant',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    address = db.Column(db.String)
    
    # restaurant_pizza = db.relationship('RestaurantPizza', backref='restaurant')
    pizzas =db.relationship('Pizza', secondary ='restaurant_pizzas', back_populates=('restaurants'))
    
    
    
    def __repr__(self):
        return f'<Restaurant {self.name}, {self.address}>'
    
class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'
    
    serialize_rules = ('-restaurants',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # restaurant_pizza = db.relationship('RestaurantPizza', backref='pizza')
    restaurants =db.relationship('Restaurant', secondary ='restaurant_pizzas', back_populates=('pizzas'))
    
    
    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'
  
class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'
        
    # serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas')
    
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
        
    
    @validates("price")
    def validate_price(self, key, price):
        
        if (type(price) in (int, float)) and (1 >= price >= 30):
            raise ValueError("price must be between 1 and 30")
        return price
    
    def __repr__(self):
        return f'<Restaurant Pizza {self.price}>'
