from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_cors import CORS

"""
These object can be used throughout project.
1.) Objects from this file can be included in many blueprints
2.) Isolating these object definitions avoids duplication and circular dependencies
"""

# Setup of key Flask object (app)
app = Flask(__name__)
cors = CORS(app, 
    resources={r"/api/*": {"origins": ["http://localhost:4100", "http://127.0.0.1:4100", 
                                   "http://localhost:8050"]}},
    supports_credentials=True, 
    methods=["GET", "POST", "PUT", "DELETE"])

# Setup SQLAlchemy object and properties for the database (db)
dbURI = 'sqlite:///volumes/sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET_KEY'
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy()
Migrate(app, db)

# Images storage
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # maximum size of uploaded content
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']  # supported file types
app.config['UPLOAD_FOLDER'] = 'volumes/uploads/'  # location of user uploaded content
