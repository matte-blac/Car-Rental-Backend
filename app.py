from flask import Flask, jsonify, request
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, AvailableCar, HiredCar, User, Category
from users import UsersResource
from login import LoginResource, UserRegistrationResource
from admin import AvailableCarResource,AdminAvailableCarResource, UserRoleResource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from hire import AdminActionResource, HireStatusResource, HireResource
from hire import AdminActionResource, HireResource, HireStatusResource

# Create Flask application instance
app = Flask(__name__)
CORS(app)

# Configure SQLAlchemy to use SQLite database located at 'app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)
# Set the secret key for JWT token
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600000  # Token expiration time (1 hour)

# Initialize SQLAlchemy with the Flask app
migrate = Migrate(app, db)
db.init_app(app)

# Initialize Flask-JWT-Extended
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Add Users resource to the Flask-RESTful API with the endpoint '/users'
api = Api(app)
CORS(api)
api.add_resource(UsersResource, '/users')

# Add Login resource to the Flask-RESTful API with the endpoint '/login'
api.add_resource(LoginResource, '/login')

# Add User Registration resource to the Flask-RESTful API with the endpoint '/register'
api.add_resource(UserRegistrationResource, '/register')

api.add_resource(AvailableCarResource, '/availablecars', '/availablecars/<int:availablecar_id>', '/public/availablecars')
api.add_resource(AdminAvailableCarResource, '/availablecars/<int:availablecar_id>')

api.add_resource(HireResource, '/hire')
api.add_resource(HireStatusResource, '/hire_status/<int:user_id>')
api.add_resource(AdminActionResource, '/admin/action')

# udate user role endpoint
api.add_resource(UserRoleResource, '/usersrole/<int:user_id>/role')


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

#update available cars
@app.route('/availablecars/<int:availablecars_id>', methods=['PUT'])
def update_availablecar(availablecars_id):
    data = request.json
    car = AvailableCar.query.get(availablecars_id)
    if car:
        car.brand = data.get('brand', car.brand)
        car.price = data.get('price', car.price)
        car.car_name = data.get('car_name', car.car_name)
        car.quantity = data.get('quantity', car.quantity)
        car.image_url = data.get('image_url', car.image_url)
        car.number_plate = data.get('number_plate', car.number_plate)
        db.session.commit()
        return jsonify({'message': 'Available car updated successfully'})
    else:
        return jsonify({"message": 'Car not found. Failed to update.'})

#delete available car by id
@app.route('/availablecars/<int:availablecars_id>', methods=['DELETE'])
def delete_availablecar(availablecars_id):
    car = AvailableCar.query.get(availablecars_id)
    if car:
        db.session.delete(car)
        db.session.commit()
        return jsonify({'message': 'Available car has been deleted'})
    else:
        return jsonify ({'message': 'Error deleting car'})

# add new available car
@app.route('/availablecars', methods=['POST'])
def add_availablecar():
    data = request.json
    new_car = AvailableCar(
    brand=data['brand'],
    price=data['price'],
    car_name=data['car_name'],
    quantity=data['quantity'],
    image_url=data['image_url'],
    number_plate=data['number_plate']
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify ({'message': 'New car addded succssfully'})

#get all categories
@app.route('/categories')
def get_categories():
    categories = Category.query.all()
    categories_list = []
    for category in categories:
        category_dict = {
            'id': category.id,
            'category_name': category.category_name
        }
        categories_list.append(category_dict)
    return jsonify (categories_list)

#get categories by id
@app.route('/categories/<int:categories_id>', methods=['GET'])
def get_categories_by_id(categories_id):
    category = Category.query.get(categories_id)
    if category:
        return jsonify({
            'id': category.id,
            'category_name': category.category_name
        }), 200
    else:
        return jsonify ({'error': 'Category not found'}, 400)

#update categories
@app.route('/categories/<int:categories_id>', methods=['PUT'])
def update_category(categories_id):
    data = request.json
    category = Category.query.get(categories_id)
    if category:
        category.category_name = data.get('category_name', category.category_name)
        db.session.commit()
        return jsonify({'message': 'Category updated successfully'})
    else:
        return jsonify({"message": 'Failed to update'})

#delete category by id
@app.route('/categories/<int:categories_id>', methods=['DELETE'])
def delete_category(categories_id):
    category = Category.query.get(categories_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category has been deleted'})
    else:
        return jsonify ({'message': 'Error deleting category'})

# add new category
@app.route('/categories', methods=['POST'])
def add_category():
    data = request.json
    new_category = Category(
    category_name=data['category_name']
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify ({'message': 'Category addded succssfully'})


# Start the Flask application if this script is executed directly
if __name__ == '__main__':
    app.run(port=5555, debug=True)
