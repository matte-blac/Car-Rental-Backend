from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from models import db, User, AvailableCar, HiredCar
from datetime import datetime, timedelta

# Parser for hire requests
hire_parser = reqparse.RequestParser()
hire_parser.add_argument('user_id', type=int, required=True, help='User ID is required')
hire_parser.add_argument('car_id', type=int, required=True, help='Car ID is required')
hire_parser.add_argument('hired_date', type=str, required=True, help='Hired date is required (YYYY-MM-DD)')
hire_parser.add_argument('return_date', type=str, required=True, help='Return date is required (YYYY-MM-DD)')
hire_parser.add_argument('pickup_location', type=str, required=True, help='Pickup location is required')
hire_parser.add_argument('destination', type=str, required=True, help='Destination is required')

# Parser for approve and cancel requests
approve_cancel_parser = reqparse.RequestParser()
approve_cancel_parser.add_argument('hire_id', type=int, required=True, help='Hire ID is required')
approve_cancel_parser.add_argument('action', type=str, required=True, help='Action (approve/cancel) is required')

class HireResource(Resource):
    def post(self):
        args = hire_parser.parse_args()
        user_id = args['user_id']
        car_id = args['car_id']
        hired_date = datetime.strptime(args['hired_date'], '%Y-%m-%d')
        return_date = datetime.strptime(args['return_date'], '%Y-%m-%d')
        pickup_location = args['pickup_location']
        destination = args['destination']

        # Check if the car is available
        car = AvailableCar.query.get(car_id)
        if car is None:
            return {'message': 'Car not found'}, 404
        if car.quantity <= 0:
            return {'message': 'Car not available for hire'}, 400

        # Calculate hire duration
        hire_duration = (return_date - hired_date).days

        # Calculate total amount
        total_amount = car.price * hire_duration

        # Create hired car entry
        hired_car = HiredCar(
            hired_date=hired_date,
            return_date=return_date,
            pickup_location=pickup_location,
            destination=destination,
            users_id=user_id,
            availablecars_id=car_id
        )
        db.session.add(hired_car)
        db.session.commit()

        # Decrease car quantity
        car.quantity -= 1
        db.session.commit()

       
        return {
            'message': 'Car hired successfully',
            'total_amount': total_amount
        }, 200

class HireStatusResource(Resource):
    def get(self, user_id):
        # Get hire status for a user
        hires = HiredCar.query.filter_by(users_id=user_id).all()
        if not hires:
            return {'message': 'No hires found for this user'}, 404

        hire_status = []
        for hire in hires:
            car = AvailableCar.query.get(hire.availablecars_id)
            status = {
                'car_id': car.id,
                'car_name': car.car_name,
                'hired_date': hire.hired_date.strftime('%Y-%m-%d'),
                'return_date': hire.return_date.strftime('%Y-%m-%d'),
                'pickup_location': hire.pickup_location,
                'destination': hire.destination,
                'status': hire.status
            }
            hire_status.append(status)

        return {'hire_status': hire_status}, 200
    
#admin
class AdminActionResource(Resource):
    def post(self):
        args = approve_cancel_parser.parse_args()
        hire_id = args['hire_id']
        action = args['action']

        # Check if the action is valid
        if action not in ['approve', 'cancel']:
            return {'message': 'Invalid action'}, 400

        # Retrieve the hired car
        hired_car = HiredCar.query.get(hire_id)
        if hired_car is None:
            return {'message': 'Hire request not found'}, 404

        # Check if the car is available
        car = AvailableCar.query.get(hired_car.availablecars_id)
        if car is None:
            return {'message': 'Car not found'}, 404

        if action == 'approve':
            # Check if the car is available for hire
            if car.quantity <= 0:
                return {'message': 'Car not available for hire'}, 400

            # Approve hire by decreasing car quantity and updating hire status
            car.quantity -= 1
            hired_car.status = 'approved'
            db.session.commit()
            return {'message': 'Hire request approved successfully'}, 200

        elif action == 'cancel':
            # Cancel hire by increasing car quantity and updating hire status
            car.quantity += 1
            hired_car.status = 'cancelled'
            db.session.commit()
            return {'message': 'Hire request cancelled successfully'}, 200
