from flask import Flask, jsonify, make_response
from models import db, User
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource
from users import Users


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


# Add the Users resource to the Flask-RESTful API with the endpoint '/users'
api.add_resource(Users, '/users')

if __name__ == '__main__':
    # Run the Flask application on port 5555 in debug mode with reloader enabled
    app.run(port=5555, debug=True, use_reloader=True)
