from flask import Flask, request, jsonify
import requests
import base64
import datetime
import json
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

app = Flask(__name__)
CORS(app)

# Replace these values with your actual Safaricom Daraja API credentials
CONSUMER_KEY = "V9fxIEMJoQZoLMGJTR7KNSFUlEACwkc3IGlwAcuFKlXtntG0"
CONSUMER_SECRET = "nFYKGwWdAiGB9l31HGGIi5LUibx0oG39jSzZSnDi7JwYUHdrwfjK11OT1zgBZnr1"
LIPA_NA_MPESA_PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
SHORTCODE = "174379"
LIPA_NA_MPESA_ONLINE_ENDPOINT = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

# Token cache
token_cache = {
    "token": None,
    "expiry_time": None
}

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
api.add_resource(UserUpdateResource, "/update_user")


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


# Payment logic
@app.route('/callback_url', methods=['POST'])
def callback_url():
    data = request.json

    # Process the callback data
    transaction_status = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
    print(data)
    if transaction_status == 0:
        print("Payment successful")
    else:
        # Payment failed
        # Handle the failure scenario
        print("Payment failed")

    return jsonify({"ResultCode": 0, "ResultDesc": "Success"})  

@app.route('/lipa_na_mpesa', methods=['POST'])
def lipa_na_mpesa():
    try:
        token = generate_token()
        if token is None:
            return jsonify({"error": "Failed to generate token"}), 500
        phone_number = request.json.get('phone_number')
        amount = request.json.get('amount')
        
        if not phone_number or not amount:
            return jsonify({"error": "Phone number and amount are required"}), 400

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode((SHORTCODE + LIPA_NA_MPESA_PASSKEY + timestamp).encode()).decode('utf-8')

        payload = {
            "BusinessShortCode": SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://8ead-41-80-111-14.ngrok-free.app/callback_url",
            "AccountReference": "Safari Wheels Kenya",
            "TransactionDesc": "Payment for testing"
        }

        headers = {
            "Authorization": "Bearer " + generate_token(),
            "Content-Type": "application/json"
        }

        response = requests.post(LIPA_NA_MPESA_ONLINE_ENDPOINT, json=payload, headers=headers)

        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
def generate_token():
    token_endpoint = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    credentials = base64.b64encode((CONSUMER_KEY + ':' + CONSUMER_SECRET).encode()).decode('utf-8')
    headers = {
        'Authorization': 'Basic ' + credentials
    }

    try:
        response = requests.get(token_endpoint, headers=headers)
        response.raise_for_status()  
        return response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to generate token: {e}") from e


if __name__ == '__main__':
    app.run(debug=True)
