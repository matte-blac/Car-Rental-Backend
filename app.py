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
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-JWT-Extended
jwt = JWTManager(app)

# Add Users resource to the Flask-RESTful API with the endpoint '/users'
api = Api(app)
api.add_resource(UsersResource, '/users')

# Add Login resource to the Flask-RESTful API with the endpoint '/login'
api.add_resource(LoginResource, '/login')

# Add User Registration resource to the Flask-RESTful API with the endpoint '/register'
api.add_resource(UserRegistrationResource, '/register')

# Sample protected route requiring JWT authentication
@app.route('/protected')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/')
def home():
    return 'home'

# Start the Flask application if this script is executed directly
if __name__ == '__main__':
    app.run(port=5555, debug=True)
