from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from models import db  # Assuming 'db' is defined in models.py
from users import UsersResource
from login import LoginResource, UserRegistrationResource
from flask_migrate import Migrate

# Create Flask application instance
app = Flask(__name__)

# Configure SQLAlchemy to use SQLite database located at 'app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the secret key for JWT token
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Add Users resource to the Flask-RESTful API with the endpoint '/users'
api = Api(app)
api.add_resource(UsersResource, '/users')

# Add Login resource to the Flask-RESTful API with the endpoint '/login'
api.add_resource(LoginResource, '/login')

# Add User Registration resource to the Flask-RESTful API with the endpoint '/register'
api.add_resource(UserRegistrationResource, '/register')

@app.route('/availablecars')
def availablecars():
    availablecars = AvailableCar.query.all()
    cars_list = []
    for car in availablecars:
        car_dict = {
            'id': car.id,
            'brand': carbrand,
            'price': car.price,
            'car_name': car.car_name,
            'quantity': car.quantity,
            'image_url': car.image_url,
            'number_plate': car.number_plate
        }
        cars_list.append(car_dict)
    return jsonify(cars_list)

@app.route('/availablecars/<int:car_id>', methods=['GET'])
def get_cars_by_id(car_id):
    car = AvailableCar.query.get(car_id)
    if car:
        return jsonify({
            'id': car.id,
            'brand': car.brand,
            'price': car.price,
            'car_name': car.car_name,
            'number_plate': car.number_plate
        }), 200
    else:
        return jsonify({'error': 'car not found'}), 404

@app.route('/availablecars/<int:car_id>', methods=['PUT'])
def update_cars(car_id):
    data = request.json
    car = AvailableCar.query.get(car_id)
    if car:
        car.brand = data.get('brand', car.brand)
        car.price = data.get('price', car.price)
        car.car_name = data.get('car_name', car.car_name)
        car.quantity = data.get('quantity', car.quantity)
        car.image_url = data.get('image_url', car.image_url)
        car.number_plate = data.get('number_plate', car.number_plate)
        db.session.commit()
        return jsonify({'message': 'car updated successfully'}), 200
    else:
        return jsonify({'error': 'car not found'}), 404

@app.route('/availablecars/<int:car_id>', methods=['DELETE'])
def delete_cars(car_id):
    car = AvailableCar.query.get(car_id)
    if car:
        db.session.delete(car)
        db.session.commit()
        return jsonify({'message': 'car deleted successfully'}), 200
    else:
        return jsonify({'error': 'car not found'}), 404

@app.route('/availablecars', methods=['POST'])
def add_car():
    data = request.json
    new_car = AvailableCar(brand=data['brand'], price=data['price'], car_name=data['car_name'],
    quantity=data['quantity'], image_url=data['image_url'], number_plate=data['number_plate']
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({'message': 'car added successfully'}), 201

@app.route('/hiredcars')
def hiredcars():
    hiredcars = HiredCar.query.all()
    cars_list = []
    for car in hiredcars:
        car_dict = {
            'id': car.id,
            'hired_date': car.hired_date,
            'return_date': car.return_date,
            'pickup_location': car.pickup_location,
            'destination': car.destination
        }
        cars_list.append(car_dict)
    return jsonify(cars_list)

@app.route('/hiredcars/<int:car_id>', methods=['GET'])
def get_hiredcars_by_id(car_id):
    car = HiredCar.query.get(car_id)
    if car:
        return jsonify({
            'hired_date': car.hired_date,
            'return_date': car.return_date,
            'pickup_location': car.pickup_location,
            'destination': car.destination
        }), 200
    else:
        return jsonify({'error': 'car not found'}), 404

@app.route('/hiredcars/<int:car_id>', methods=['PUT'])
def update_hiredcars(car_id):
    data = request.json
    car = HiredCar.query.get(car_id)
    if car:
        car.hired_date = data.get('hired_date', car.hired_date)
        car.return_date = data.get('return_date', car.return_date)
        car.pickup_location = data.get('pickup_location', car.pickup_location)
        car.destination = data.get('destination', car.destination)
        db.session.commit()
        return jsonify({'message': 'car updated successfully'}), 200
    else:
        return jsonify({'error': 'car not found'}), 404

@app.route('/hiredcars/<int:car_id>', methods=['DELETE'])
def delete_hiredcars(car_id):
    car = HiredCar.query.get(car_id)
    if car:
        db.session.delete(car)
        db.session.commit()
        return jsonify({'message': 'car deleted successfully'}), 200
    else:
        return jsonify({'error': 'car not found'}), 404

@app.route('/hiredcars', methods=['POST'])
def add_hiredcar():
    data = request.json
    new_car = HiredCar(hired_cars=data['hired_cars'], return_date=data['return_date'], pickup_location=data['pickup_location'],
    destination=data['destination']
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({'message': 'car added successfully'}), 201

# Start the Flask application if this script is executed directly
if __name__ == '__main__':
    app.run(port=5555, debug=True)
