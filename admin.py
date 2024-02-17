from flask import request
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from models import db, User, AvailableCar, bcrypt


class AvailableCarResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('car_name', type=str, required=True, help='Car name cannot be blank')
    parser.add_argument('quantity', type=int, required=True, help='Quantity cannot be blank')
    parser.add_argument('brand', type=int,required=True, help='brand cannot be blank')
    parser.add_argument('image_url', type=int,required=True, help='Image cannot be blank')
    parser.add_argument('price', type=float, required=True, help='Price cannot be blank')
    parser.add_argument('number_plate', type=str, required=True, help='Number plate cannot be blank')
    @jwt_required(True)
    def get(self, availablecar_id=None):
        if availablecar_id is None:
            availablecars = AvailableCar.query.all()
            return [{"id": availablecar.id, "name": availablecar.car_name, "quantity": availablecar.quantity, "category": availablecar.brand, "image_url": availablecar.image_url,"price": availablecar.price,"Number Plate": availablecar.number_plate} for availablecar in availablecars]

        availablecar = AvailableCar.query.get(availablecar_id)
        if not availablecar:
            return {"message": "Car not found."}, 404

        return {
            "id": availablecar.id,
            "car_name": availablecar.car_name,
            "quantity": availablecar.quantity,
            "category": availablecar.brand,
            "image_url": availablecar.image_url,
            "price": availablecar.price,
            "number_plate": availablecar.number_plate
        }

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
                number_plate=data['number_plate']
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
                    "number_plate": new_availablecar.number_plate
                }
            }
        except Exception as e:
            return {"error": str(e)}, 500

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
                number_plate=data['number_plate']
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
                    "number_plate": new_availablecar.number_plate
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
            availablecar.car_name = data['name']
            availablecar.quantity = data['quantity']
            availablecar.brand = data['brand']
            availablecar.image_url = data['image_url']
            availablecar.price = data['price']
            availablecar.number_plate =data['number_plate']
            db.session.commit()

            # Return the details of the updated Car
            return {
                "message": "Car updated successfully.",
                "product": {
                    "id": availablecar.id,
                    "name": availablecar.car_name,
                    "quantity": availablecar.quantity,
                    "brand": availablecar.brand,
                    "image_url": availablecar.image_url,
                    "price": availablecar.price,
                    "number_plate":availablecar.number_plate
                }
            }
        except Exception as e:
            return {"error": str(e.message)}, 500

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


class UserResource(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            user = User.query.filter_by(email=current_user).first()

            if user:
                return {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                }, 200
            else:
                return {"message": "User not found."}, 404
        except Exception as e:
            return {"error": str(e)}, 500
        


#         {
#   "name": "Audi",
#   "quantity": "2",
#   "brand": "Q7",
#   "image_url": "https://media.ed.edmunds-media.com/audi/q7/2022/oem/2022_audi_q7_4dr-suv_prestige_fq_oem_1_1280.jpg",
#   "price": "8000",
#   "number_plate": "KDG 085K"
#                 }


# {
#   "message": "Internal Server Error"
# }