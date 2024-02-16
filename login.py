from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, bcrypt 

# Define a resource for user registration
class UserRegistrationResource(Resource):
    def post(self):
        try:
            # Get JSON data from the request
            data = request.get_json()  
            
            # Extract user data from the request JSON data
            email = data.get('email')  
            first_name = data.get('first_name')  
            last_name = data.get('last_name')  
            phone_number = data.get('phone_number')  
            password = data.get('password')  

            # Check if all required fields are provided
            if not email or not first_name or not last_name or not phone_number or not password:
                return {"error": "All fields are required."}, 400

            # Check if the email is already registered
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return {"error": "Email is already registered."}, 400

            # Hash the password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # Create a new user instance
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                password=hashed_password
            )

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
            data = request.get_json()  
            email = data.get('email')  
            password = data.get('password')  

            # Check if both email and password are provided
            if not email or not password:
                return {"error": "Email and password are required."}, 400

            # Retrieve the user with the provided email from the database
            user = User.query.filter_by(email=email).first()

            # Check if the user exists and the password is correct
            if user and bcrypt.check_password_hash(user.password, password):
                # Generate JWT token for the user
                access_token = create_access_token(identity=user.id)
                # Return a success message along with the user's details and token
                return {
                    "message": "Login successful.",
                    "user": {"id": user.id, "email": user.email},
                    "access_token": access_token
                }, 200
            else:
                # Return an error message for invalid credentials
                return {"error": "Invalid email or password."}, 401
        except Exception as e:
            # Return an error message for any unexpected errors
            return {"error": str(e)}, 500

# Define a resource for user logout
class LogoutResource(Resource):
    @jwt_required() 
    def post(self):
        try:
            user_id = get_jwt_identity() 
            # Perform logout actions if needed 
            return {"message": "Logout successful."}, 200
        except Exception as e:
            # Return an error message for any unexpected errors
            return {"error": str(e)}, 500
