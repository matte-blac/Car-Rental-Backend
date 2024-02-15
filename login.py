from flask import request
from flask_restful import Resource
from models import db, User #bcrypt

# Define a resource for user registration
class UserRegistrationResource(Resource):
    def post(self):
        try:
            # Extract username and password from the request JSON data
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            # Check if both username and password are provided
            if not username or not password:
                return {"error": "Username and password are required."}, 400

            # Check if the username is already taken
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return {"error": "Username is already taken."}, 400

            # Hash the password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # Create a new user instance
            new_user = User(username=username, password=hashed_password)

            # Add the new user to the database session and commit the transaction
            db.session.add(new_user)
            db.session.commit()

            # Return a success message for user registration
            return {"message": "User registered successfully."}, 201
        except Exception as e:
            # Return an error message for any unexpected errors
            return {"error": str(e)}, 500

# Define a resource for user login
class LoginResource(Resource):
    def post(self):
        try:
            # Extract username and password from the request JSON data
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            # Check if both username and password are provided
            if not username or not password:
                return {"error": "Username and password are required."}, 400

            # Retrieve the user with the provided username from the database
            user = User.query.filter_by(username=username).first()

            # Check if the user exists and the password is correct
            if user and bcrypt.check_password_hash(user.password, password):
                # Return a success message along with the user's details
                return {"message": "Login successful.", "user": {"id": user.id, "username": user.username}}, 200
            else:
                # Return an error message for invalid credentials
                return {"error": "Invalid username or password."}, 401
        except Exception as e:
            # Return an error message for any unexpected errors
            return {"error": str(e)}, 500

