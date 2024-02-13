import threading
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask.cli import AppGroup

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and methods

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///decks.db'  # Use your actual database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Initialize the SQLAlchemy db instance

# New Deck model
class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    cards = db.Column(db.String(255), nullable=False)  # Storing card IDs in a comma-separated string

    def __repr__(self):
        return f'<Deck {self.name}>'

@app.route('/save_deck', methods=['POST'])
def save_deck():
    data = request.json
    deck_name = data.get('name')
    cards = ','.join(map(str, data.get('cards')))  # Convert card IDs list to a comma-separated string

    if not deck_name or not cards:
        return jsonify({'error': 'Deck name and card IDs are required'}), 400

    new_deck = Deck(name=deck_name, cards=cards)
    db.session.add(new_deck)
    db.session.commit()

    return jsonify({'message': 'Deck saved successfully'}), 201

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to render index() function
def index():
    return render_template("index.html")

@app.route('/table/')  # connects /table/ URL to render table() function
def table():
    return render_template("table.html")

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    # Generate data here (This function should be defined or imported)
    pass

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)

with app.app_context():
    db.create_all()  # Create tables

# this runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8086")