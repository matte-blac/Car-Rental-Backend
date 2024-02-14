from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
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

    # relationship to HiredCars
    hired_cars = db.relationship('HiredCar', backref='availablecar', lazy=True)

    # foreign key to Categories
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

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

    # Foreign Key to Users
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Foreign Key to AvailableCars
    availablecars_id = db.Column(db.Integer, db.ForeignKey('availablecars.id'), nullable=False)