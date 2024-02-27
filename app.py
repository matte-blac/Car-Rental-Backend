from flask import Flask, jsonify, request
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, AvailableCar, HiredCar, User, Category
from login import LoginResource, UserRegistrationResource
from admin import AdminAvailableCarResource
from users import UserResource, UserUpdateResource
from availablecars import AvailableCarResource
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from hire import (
    AdminActionResource,
    HireResource,
    HireStatusResource,
    AdminAllHiresResource,
    UserHiresResource,
)

# Create Flask application instance
app = Flask(__name__)

CORS(app)

# Configure SQLAlchemy to use SQLite database located at 'app.db'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

jwt = JWTManager(app)
# Set the secret key for JWT token
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600000  # Token expiration time (1 hour)

# Initialize SQLAlchemy with the Flask app
migrate = Migrate(app, db)
db.init_app(app)

# Initialize Flask-JWT-Extended
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Add Users resource to the Flask-RESTful API with the endpoint '/users'
api = Api(app)


# Endpoint for user login
api.add_resource(LoginResource, "/login")

# Endpoint for user registration
# Add User Registration resource to the Flask-RESTful API with the endpoint '/register'
api.add_resource(UserRegistrationResource, "/register")

api.add_resource(UserResource, "/current_user")
api.add_resource(UserUpdateResource, "/current_user/update")


# Endpoints for retrieving and managing available cars
api.add_resource(
    AvailableCarResource,
    "/availablecars",
    "/availablecars/<int:availablecar_id>",
    "/public/availablecars",
)
# Endpoint for admin actions on available cars
api.add_resource(AdminAvailableCarResource, "/availablecars/<int:availablecar_id>")

# Endpoint for hiring a car
api.add_resource(HireResource, "/hire")
# Endpoint for checking hire status
api.add_resource(HireStatusResource, "/hire_status/<int:user_id>")
# Endpoint for admin actions
api.add_resource(AdminActionResource, "/admin/action")


# Add routes to the API
api.add_resource(AdminAllHiresResource, "/admin/hires")
api.add_resource(UserHiresResource, "/user/<int:user_id>/hires")


# search for car
@app.route("/cars/<search_term>")
def search_cars(search_term):
    # Perform search query using SQLAlchemy
    search_results = AvailableCar.query.filter(
        (AvailableCar.brand.ilike(f"%{search_term}%"))
        | (AvailableCar.car_name.ilike(f"%{search_term}%"))
    ).all()
    # Serialize search results and return as JSON
    return jsonify([car.serialize() for car in search_results])


# get all categories
@app.route("/categories")
def get_categories():
    categories = Category.query.all()
    categories_list = []
    for category in categories:
        category_dict = {"id": category.id, "category_name": category.category_name}
        categories_list.append(category_dict)
    return jsonify(categories_list)


# get categories by id
@app.route("/categories/<int:categories_id>", methods=["GET"])
def get_categories_by_id(categories_id):
    category = Category.query.get(categories_id)
    if category:
        return (
            jsonify({"id": category.id, "category_name": category.category_name}),
            200,
        )
    else:
        return jsonify({"error": "Category not found"}, 400)


# update categories
@app.route("/categories/<int:categories_id>", methods=["PUT"])
def update_category(categories_id):
    data = request.json
    category = Category.query.get(categories_id)
    if category:
        category.category_name = data.get("category_name", category.category_name)
        db.session.commit()
        return jsonify({"message": "Category updated successfully"})
    else:
        return jsonify({"message": "Failed to update"})


# delete category by id
@app.route("/categories/<int:categories_id>", methods=["DELETE"])
def delete_category(categories_id):
    category = Category.query.get(categories_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category has been deleted"})
    else:
        return jsonify({"message": "Error deleting category"})


# add new category
@app.route("/categories", methods=["POST"])
def add_category():
    data = request.json
    new_category = Category(category_name=data["category_name"])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Category addded succssfully"})


# Start the Flask application if this script is executed directly
if __name__ == "__main__":
    app.run(port=5555, debug=True)
