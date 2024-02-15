from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, bcrypt


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