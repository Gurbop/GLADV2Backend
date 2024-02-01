import os
import base64
import json
from datetime import date
from random import randrange
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

# Initialize Flask App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # SQLite database
app.config['SECRET_KEY'] = '09f26e402586e2faa8da4c98a35f1b20d6b033c60'  # Random secret key
app.config['UPLOAD_FOLDER'] = './uploads'  # Upload folder for images

db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, nullable=False)
    image = db.Column(db.String, nullable=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, user_id, note, image=None):
        self.userID = user_id
        self.note = note
        self.image = image

    def __repr__(self):
        return f"<Post {self.id}>"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        upload_folder = app.config['UPLOAD_FOLDER']
        image_path = os.path.join(upload_folder, self.image) if self.image else None
        image_data = None
        if image_path and os.path.isfile(image_path):
            with open(image_path, 'rb') as file:
                image_data = base64.b64encode(file.read()).decode('utf-8')
        return {
            "id": self.id,
            "userID": self.userID,
            "note": self.note,
            "image": self.image,
            "base64": image_data
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    _dob = db.Column(db.Date, nullable=True)
    _role = db.Column(db.String(20), default="User", nullable=False)
    
    posts = db.relationship('Post', backref='user', lazy=True)

    def __init__(self, name, uid, password, dob=None, role="User"):
        self._name = name
        self._uid = uid
        self._password = generate_password_hash(password)
        self._dob = dob
        self._role = role

    def set_password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self._name,
            "uid": self._uid,
            "dob": self._dob.isoformat() if self._dob else None,
            "role": self._role
        }

    @property
    def role(self):
        return self._role

    def is_admin(self):
        return self._role == "Admin"

def init_users():
    with app.app_context():
        db.create_all()
        # Sample users initialization
        users = [
            User(name='Thomas Edison', uid='edison', password='securepassword123', dob=date(1847, 2, 11), role="Admin"),
            # Add more sample users if needed
        ]
        for user in users:
            db.session.add(user)
            for i in range(randrange(1, 5)):
                post = Post(user_id=user.id, note=f'Sample note {i} for {user.name}')
                db.session.add(post)
            try:
                db.session.commit()
            except IntegrityError:
                print(f'Duplicate user or other database error for user: {user._uid}')
                db.session.rollback()
if __name__ == '__main__':
    init_users()