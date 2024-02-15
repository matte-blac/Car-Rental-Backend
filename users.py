from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User

# Define the UsersResource class to handle user-related operations
class UsersResource(Resource):
    # Define method to retrieve users
    @jwt_required()  # Require JWT authentication to access this endpoint
    def get(self):
        # Get the identity of the current user from the JWT token
        current_user = get_jwt_identity()

        # Check if the current user is an admin
        if current_user == 'admin':
            # Retrieve all users from the database
            users = User.query.all()
            # Convert users to dictionary format
            users_data = [{'id': user.id, 'username': user.username, 'is_admin': user.is_admin} for user in users]
            return {'users': users_data}, 200
        else:
            return {'error': 'Access denied. Admin privilege required.'}, 403
