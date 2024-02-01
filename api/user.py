import json
import jwt
from datetime import datetime
from flask import Flask, Blueprint, request, jsonify, current_app, Response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import os

# Initialize Flask App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = '09f26e402586e2faa8da4c98a35f1b20d6b033c60'

db = SQLAlchemy(app)

# User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.Date)
    _role = db.Column(db.String(20), default="User", nullable=False)

    def __init__(self, name, uid, password, dob, role="User"):
        self._name = name
        self._uid = uid
        self._password = generate_password_hash(password)
        self._dob = dob
        self._role = role

    def check_password(self, password):
        return check_password_hash(self._password, password)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self._name,
            "uid": self._uid,
            "dob": self._dob.strftime("%Y-%m-%d") if self._dob else None,
            "role": self._role
        }

# Blueprint for user routes
user_api = Blueprint('user_api', __name__, url_prefix='/api/users')
api = Api(user_api)

# User CRUD class
class _CRUD(Resource):
    def post(self): 
        body = request.get_json()
        name = body.get('name')
        uid = body.get('uid')
        password = body.get('password')
        dob = body.get('dob', '')
        role = body.get('role', 'User')

        if not all([name, uid, password]):
            return jsonify({'message': 'Missing required fields'}), 400

        try:
            dob_parsed = datetime.strptime(dob, '%Y-%m-%d').date() if dob else None
            user = User(name=name, uid=uid, password=password, dob=dob_parsed, role=role)
            db.session.add(user)
            db.session.commit()
            return jsonify(user.as_dict()), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify({'message': 'User already exists'}), 409
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    def get(self):
        users = User.query.all()
        return jsonify([user.as_dict() for user in users]), 200

# User Security class
class _Security(Resource):
    def post(self):
        body = request.get_json()
        uid = body.get('uid')
        password = body.get('password')

        user = User.query.filter_by(_uid=uid).first()
        if user and user.check_password(password):
            token = jwt.encode({"_uid": user._uid}, app.config["SECRET_KEY"], algorithm="HS256")
            return jsonify({"token": token}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401

# Add resources to the API
api.add_resource(_CRUD, '/')
api.add_resource(_Security, '/authenticate')

# Register Blueprint
app.register_blueprint(user_api)

# Database initialization
@app.before_first_request
def initialize_database():
    db.create_all()

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)