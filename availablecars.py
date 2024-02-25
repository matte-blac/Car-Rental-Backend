from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
)
from models import db, User, AvailableCar, bcrypt


class AvailableCarResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "car_name", type=str, required=True, help="Car name cannot be blank"
    )
    parser.add_argument(
        "quantity", type=int, required=True, help="Quantity cannot be blank"
    )
    parser.add_argument("brand", type=str, required=True, help="brand cannot be blank")
    parser.add_argument(
        "image_url", type=str, required=True, help="Image cannot be blank"
    )
    parser.add_argument(
        "price", type=float, required=True, help="Price cannot be blank"
    )
    parser.add_argument(
        "number_plate", type=str, required=True, help="Number plate cannot be blank"
    )

    @jwt_required(True)
    def get(self, availablecar_id=None):
        if availablecar_id is None:
            availablecars = AvailableCar.query.all()
            cars_list = []
            for car in availablecars:
                car_dict = {
                    "id": car.id,
                    "brand": car.brand,
                    "price": car.price,
                    "car_name": car.car_name,
                    "quantity": car.quantity,
                    "image_url": car.image_url,
                    "number_plate": car.number_plate,
                    "category_id": car.category_id,
                }
                cars_list.append(car_dict)
            return jsonify(cars_list)

        availablecar = AvailableCar.query.get(availablecar_id)
        if not availablecar:
            return {"message": "Car not found."}, 404

        return {
            "id": availablecar.id,
            "car_name": availablecar.car_name,
            "quantity": availablecar.quantity,
            "brand": availablecar.brand,
            "image_url": availablecar.image_url,
            "price": availablecar.price,
            "number_plate": availablecar.number_plate,
            "category_id": availablecar.category_id,
        }

    @jwt_required()
    def post(self):
        try:
            current_user = User.query.filter_by(email=get_jwt_identity()).first()
            if not current_user:
                return {"error": "User not authenticated"}, 401
            if current_user.role != "admin":
                return {"error": "User not Admin"}, 403

            data = request.get_json()
            new_availablecar = AvailableCar(
                car_name=data["car_name"],
                quantity=data["quantity"],
                brand=data["brand"],
                image_url=data["image_url"],
                price=data["price"],
                number_plate=data["number_plate"],
                category_id=data["category_id"],
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
                    "category_id": new_availablecar.category_id,
                },
            }
        except Exception as e:
            return {"error": str(e)}, 500

    def delete(self, availablecar_id):
        car = AvailableCar.query.get(availablecar_id)
        if car:
            db.session.delete(car)
            db.session.commit()
            return jsonify({"message": "Available car has been deleted"})
        else:
            return jsonify({"message": "Error deleting car"})

    def put(self, availablecar_id):
        data = request.json
        car = AvailableCar.query.get(availablecar_id)
        if car:
            car.brand = data.get("brand", car.brand)
            car.price = data.get("price", car.price)
            car.car_name = data.get("car_name", car.car_name)
            car.quantity = data.get("quantity", car.quantity)
            car.image_url = data.get("image_url", car.image_url)
            car.number_plate = data.get("number_plate", car.number_plate)
            db.session.commit()
            return jsonify({"message": "Available car updated successfully"})
        else:
            return jsonify({"message": "Car not found. Failed to update."})
