# Car Rental Service

## Description
This project is a car rental service implemented using Flask. It allows users to register, login, hire cars, and view their hire status. Admin users can manage available cars and approve or cancel hire requests. The application is designed to provide a seamless car hiring experience for users and easy management for administrators.

## Tech Stack
The application is built using the following technologies:
- **Python**: The backend code is written in Python.
- **Flask**: The application uses Flask, a lightweight WSGI web application framework.
- **Flask-SQLAlchemy**: This is used for handling database operations.
- **Flask-JWT-Extended**: This is used for handling JWT-based authentication.
- **Flask-Mail**: This is used for sending emails.
- **Flask-Bcrypt**: This is used for hashing passwords.
- **Flask-RESTful**: This is used for building the REST API.

## Design
The application is a backend service with a RESTful API. It does not have a user interface but interacts with clients through HTTP requests and responses. The API endpoints are designed to be intuitive and easy to use.

## Features
- **User Registration and Login**: Users can register with their email and password, and login to the system.
- **Car Hiring**: Users can hire available cars.
- **Hire Status**: Users can view the status of their hires.
- **Admin Panel**: Admin users can manage available cars and approve or cancel hire requests.

## How to Run the Project
1. Clone the repository: `git clone git@github.com:matte-blac/Car-Rental-Frontend.git`
2. Install the dependencies: `pip install -r requirements.txt`
3. Set up the database: `flask db init`
4. Run the server: `python app.py or flask run`
