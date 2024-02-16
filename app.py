from flask import Flask, jsonify, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from models import db, AvailableCar, HiredCar, User, Category
from users import UsersResource
from login import LoginResource, UserRegistrationResource
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

# Create Flask application instance
app = Flask(__name__)

# Configure SQLAlchemy to use SQLite database located at 'app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the secret key for JWT token
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # Token expiration time (1 hour)

# Initialize SQLAlchemy with the Flask app
migrate = Migrate(app, db)
db.init_app(app)

# Initialize Flask-JWT-Extended
jwt = JWTManager(app)

# Add Users resource to the Flask-RESTful API with the endpoint '/users'
api = Api(app)
api.add_resource(UsersResource, '/users')

# Add Login resource to the Flask-RESTful API with the endpoint '/login'
api.add_resource(LoginResource, '/login')

# Add User Registration resource to the Flask-RESTful API with the endpoint '/register'
api.add_resource(UserRegistrationResource, '/register')

#get all available cars
@app.route('/availablecars')
def get_availablecars():
    availablecars = AvailableCar.query.all()
    cars_list = []
    for car in availablecars:
        car_dict = {
            'id': car.id,
            'brand': car.brand,
            'price': car.price,
            'car_name': car.car_name,
            "quantity": car.quantity,
            'image_url': car.image_url,
            'number_plate': car.number_plate
        }
        cars_list.append(car_dict)
    return jsonify (cars_list)

#get available cars by id
@app.route('/availablecars/<int:availablecars_id>', methods=['GET'])
def get_availablecars_by_id(availablecars_id):
    car = AvailableCar.query.get(availablecars_id)
    if car:
        return jsonify({
            'id': car.id,
            'brand': car.brand
        }), 200
    else:
        return jsonify ({'error': 'Car not found'}, 400)


# Start the Flask application if this script is executed directly
if __name__ == '__main__':
    app.run(port=5555, debug=True)
