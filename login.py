from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask import request
from models import User

# Define the LoginResource class to handle user authentication
class LoginResource(Resource):
    # Define method to authenticate users
    def post(self):
        try:
            # Get the username and password from the request JSON data
            username = request.json.get('username')
            password = request.json.get('password')

            # Query the database to find the user with the provided credentials
            user = User.query.filter_by(username=username, password=password).first()

            # Check if user exists and credentials are correct
            if user:
                # Generate JWT access token for the user
                access_token = create_access_token(identity=username)

                # Return the access token as JSON response with HTTP status code 200 (OK)
                return {'access_token': access_token}, 200
            else:
                # Return error message for invalid username or password with HTTP status code 401 (Unauthorized)
                return {'error': 'Invalid username or password'}, 401
        except Exception as e:
            # Return error message for internal server error with HTTP status code 500 (Internal Server Error)
            return {'error': str(e)}, 500
