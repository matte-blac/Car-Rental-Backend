from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer(12), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.column(db.String, nullable=False)

    # relationship to HiredCars
    hired_cars = db.relationship('HiredCars', backref='user', lazy=True)

class HiredCars(db.Model, SerializerMixin):
    __tablename__ = 'hiredcars'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    car_name = db.Column(db.String, nullable=False)

    users_id = db.Column(db.Integer, Foreign_Key=('users.id'), nullable=True)