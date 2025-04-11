from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from flasgger import Swagger, swag_from
import os

load_dotenv()
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get('SQLALCHEMY_DATABASE_URI','sqlite:///users.db') 
app.config['JWT_SECRET_KEY'] =os.environ.get('JWT_SECRET_KEY')
app.config['SWAGGER'] = {
    'title': 'Your API',
    'securityDefinitions': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
        }
    },
    'security': [
        {
            'Bearer': []
        }
    ]
}

# Extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
swagger = Swagger(app)  # Initialize Swagger UI

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

@app.before_request
def create_tables():
    db.create_all()

# Register endpoint
@app.route('/api/auth/v1/register', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        201: {'description': 'User registered successfully'},
        400: {'description': 'Username already exists'}
    }
})
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'Username already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

# Login endpoint
@app.route('/api/auth/v1/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        200: {'description': 'Access token returned'},
        401: {'description': 'Invalid credentials'}
    }
})
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user is None or not check_password_hash(user.password_hash, password):
        return jsonify({'msg': 'Bad username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# Protected endpoint
@app.route('/api/auth/v1/user/profile', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Protected'],
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {'description': 'Access granted'},
         401: {'description': 'Unauthorized - Invalid token or no token provided'},
    }
})
def protected():
    return jsonify(message="This is a protected route."), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)


