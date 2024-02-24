from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
)
from models import db, User


class UserResource(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            user = User.query.filter_by(email=current_user).first()

            if user:
                return {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone_number": user.phone_number,
                    "email": user.email,
                    "role": user.role,
                }, 200
            else:
                return {"message": "User not found."}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def patch(self):
        try:
            current_user = get_jwt_identity()
            user = User.query.filter_by(email=current_user).first()

            if user:
                # parse the JSON patch document from the request
                parser = reqparse.RequestParser()
                parser.add_argument("first_name", type=str)
                parser.add_argument("last_name", type=str)
                parser.add_argument("phone_number", type=int)
                parser.add_argument("email", type=str)
                args = parser.parse_args()

                # apply the changes to the user
                if args["first_name"]:
                    user.first_name = args["first_name"]
                if args["last_name"]:
                    user.last_name = args["last_name"]
                if args["phone_number"]:
                    user.phone_number = args["phone_number"]
                if args["email"]:
                    user.email = args["email"]

                db.session.commit()

                return {"message": "User updated successfully."}, 200
            else:
                return {"message": "User not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500


class UserRoleResource(Resource):
    @jwt_required()
    def patch(self, user_id):
        try:
            # Check if the current user is an admin
            current_user = User.query.filter_by(email=get_jwt_identity()).first()
            if not current_user or current_user.role != "admin":
                return {"error": "Access denied. Admins only."}, 403

            # Retrieve the user to update
            user_to_update = User.query.get(user_id)
            if not user_to_update:
                return {"error": "User not found."}, 404

            # Parse the request data
            data = request.get_json()

            # Check if the role field is provided in the request
            if "role" not in data:
                return {"error": "Role field is required."}, 400

            # Check if the role is either 'admin' or 'user'
            new_role = data["role"]
            if new_role not in ["admin", "user"]:
                return {
                    "error": "Invalid role. Role must be either 'admin' or 'user'."
                }, 400

            # Update the user's role
            user_to_update.role = new_role
            db.session.commit()

            # Return success message
            return {
                "message": f"User role updated successfully. New role: {new_role}.",
                "user": {
                    "id": user_to_update.id,
                    "email": user_to_update.email,
                    "role": user_to_update.role,
                },
            }, 200

        except Exception as e:
            return {"error": str(e)}, 500
