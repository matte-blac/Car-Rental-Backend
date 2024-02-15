from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import time
from flask_bcrypt import Bcrypt
import re

db = SQLAlchemy()
bcrypt = Bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    # relationship to HiredCars
    hired_cars = db.relationship('HiredCar', backref='user', lazy=True)

    @validates('email')
    def validates_email(self, key, email):
        assert '@' and '.com' in email, 'Invalid Email'
        return email

class AvailableCar(db.Model, SerializerMixin):
    __tablename__ = 'availablecars'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    car_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    number_plate = db.Column(db.String, unique=True, nullable=False)

    # relationship to HiredCars
    hired_cars = db.relationship('HiredCar', backref='availablecar', lazy=True)

    # foreign key to Categories
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    @validates('number_plate')
    def validate_number_plate(self, key, number_plate):
        # the number plate should start with 'K
        assert number_plate[0] == 'K', "Number plate must start with 'K'"
        # the second and third characters should be letters
        assert number_plate[1:3].isalpha(), "The second and third characters must be letters"
        # there must be a space after the first 3 characters
        assert number_plate[3] == ' ', "There must be a space after the first three letters"
        # the first 3 characters after the space must be digits
        assert number_plate[4:7].isdigit(), 'The first 3 characters after the space must be numbers'
        # the last character must be a letter
        assert number_plate[7].isalpha(), 'The last character must be a letter'

class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String, nullable=False)

    #  relationship to AvailableCar
    available_cars = db.relationship('AvailableCar', backref='category', lazy=True)

class HiredCar(db.Model, SerializerMixin):
    __tablename__ = 'hiredcars'

    id = db.Column(db.Integer, primary_key=True)
    hired_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)
    pickup_location = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)

    # Foreign Key to Users
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_users') , nullable=True)

    # Foreign Key to AvailableCars
    availablecars_id = db.Column(db.Integer, db.ForeignKey('availablecars.id', name='fk_availablecars'), nullable=False)

    # validates acceptable times and days for hiring and returning
    @validates('hired_date', 'return_date')
    def validate_date(self, key, date):
        assert date.weekday() < 6, "Apologies, Sunday is closed"
        if date.weekday() < 5: # Monday to Friday
            assert time(8, 0) <= date.time() <= time(17, 0), "Opening Hours is from 8am to 5pm"
        else: # Saturday
            assert time(9, 0) <= date.time() <= time(14, 0), "Opening Hours is from 9am to 2pm"
        return date 