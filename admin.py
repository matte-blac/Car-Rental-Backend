from flask import request
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from models import db, User, AvailableCar, bcrypt

class AdminAvailableCarResource(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = User.query.filter_by(email=get_jwt_identity()).first()
            if not current_user:
                return {"error": "User not authenticated"}, 401

            data = request.get_json()
            new_availablecar = AvailableCar(
                car_name=data['name'],
                quantity=data['quantity'],
                brand=data['brand'],
                image_url=data['image_url'],
                price=data['price'],
                number_plate=data['number_plate'],
                category_id=data['category_id']
            )
            db.session.add(new_availablecar)
            db.session.commit()

            # Return the details of the created Car
            return {
                "message": "Car added successfully.",
                "product": {
                    "id": new_availablecar.id,
                    "name": new_availablecar.car_name,
                    "quantity": new_availablecar.quantity,
                    "brand": new_availablecar.brand,
                    "image_url": new_availablecar.image_url,
                    "price": new_availablecar.price,
                    "number_plate": new_availablecar.number_plate,
                    "category_id": new_availablecar.category_id
                }
            }
        except Exception as e:
            return {"error": str(e)}, 500

    @jwt_required()
    def patch(self, availablecar_id):
        try:
            current_user = User.query.filter_by(email=get_jwt_identity()).first()
            if current_user.role != 'admin':
                return {"message": "Access denied. Admins only."}, 403

            availablecar = AvailableCar.query.get(availablecar_id)
            if not availablecar:
                return {"message": "Car not found."}, 404

            data = request.get_json()
            availablecar.car_name = data['car_name']
            availablecar.quantity = data['quantity']
            availablecar.brand = data['brand']
            availablecar.image_url = data['image_url']
            availablecar.price = data['price']
            availablecar.number_plate =data['number_plate']
            availablecar.category_id = data['category_id']
            db.session.commit()

            # Return the details of the updated Car
            return {
                "message": "Car updated successfully.",
                "product": {
                    "id": availablecar.id,
                    "car_name": availablecar.car_name,
                    "quantity": availablecar.quantity,
                    "brand": availablecar.brand,
                    "image_url": availablecar.image_url,
                    "price": availablecar.price,
                    "number_plate":availablecar.number_plate,
                    "category_id": availablecar.category_id
                }
            }
        except Exception as e:
            return {"error": str(e)}, 500

    @jwt_required()
    def delete(self, availablecar_id):
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        if current_user.role != 'admin':
            return {"message": "Access denied. Admins only."}, 403

        availablecar = AvailableCar.query.get(availablecar_id)
        if not availablecar:
            return {"message": "Car not found."}, 404

        db.session.delete(availablecar)
        db.session.commit()
        return {"message": "Car deleted successfully."}

        #...........user role update by admin......................