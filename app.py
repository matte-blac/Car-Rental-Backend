from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from models import db
from users import UsersResource
from login import LoginResource, UserRegistrationResource
from flask_jwt_extended import JWTManager
from admin import AvailableCarResource,AdminAvailableCarResource
from hire import AdminActionResource, HireResource, HireStatusResource

# Create Flask application instance
app = Flask(__name__)

# Configure SQLAlchemy to use SQLite database located at 'app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)
# Set the secret key for JWT token
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Initialize Flask-RESTful API
api = Api(app)
migrate = Migrate(app, db)

# Add Users resource to the Flask-RESTful API with the endpoint '/users'
api.add_resource(UsersResource, '/users')

# Add Login resource to the Flask-RESTful API with the endpoint '/login'
api.add_resource(LoginResource, '/login')

# Add User Registration resource to the Flask-RESTful API with the endpoint '/register'
api.add_resource(UserRegistrationResource, '/register')

api.add_resource(AvailableCarResource, '/availablecars', '/availablecars/<int:availablecar_id>', '/public/availablecars')
api.add_resource(AdminAvailableCarResource, '/availablecars/<int:availablecar_id>') 

api.add_resource(HireResource, '/hire')
api.add_resource(HireStatusResource, '/hire_status/<int:user_id>')
api.add_resource(AdminActionResource, '/admin/action')

# Start the Flask application if this script is executed directly
if __name__ == '__main__':
    app.run(port=5555, debug=True)
