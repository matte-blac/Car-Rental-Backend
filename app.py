from flask import Flask, jsonify, make_response
from models import db, User
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource

# Initialize Flask application
app = Flask(__name__)

# Configure SQLAlchemy to use SQLite database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set JSON compact mode to False to make the JSON response more readable
app.json_compact = False

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Initialize Flask-Migrate for handling database migrations
migrate = Migrate(app, db)

# Enable Cross-Origin Resource Sharing (CORS) for allowing requests from any origin
CORS(app)

# Initialize Flask-RESTful API
api = Api(app)

# Define a resource class for handling user-related operations
class Users(Resource):
    # Define a method to handle HTTP GET requests
    def get(self):
        try:
            # Retrieve all users from the database and convert them to dictionaries
            users = [user.to_dict() for user in User.query.all()]

            # Return a JSON response with the list of user dictionaries and HTTP status code 200 (OK)
            return jsonify(users), 200
        except Exception as e:
            # If an error occurs, create an error message dictionary
            error_message = {'error': str(e)}

            # Return a JSON response with the error message and HTTP status code 500 (Internal Server Error)
            return jsonify(error_message), 500

# Add the Users resource to the Flask-RESTful API with the endpoint '/users'
api.add_resource(Users, '/users')

if __name__ == '__main__':
    # Run the Flask application on port 5555 in debug mode with reloader enabled
    app.run(port=5555, debug=True, use_reloader=True)
