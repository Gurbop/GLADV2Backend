from flask import Blueprint, jsonify
from flask_restful import Api, request, Resource
import requests  # used for testing
from __init__ import app, db
import sqlite3

decks_api = Blueprint('decks_api', __name__, url_prefix='/api/decks')
api = Api(decks_api)

class deck(db.Model):
    _tablename_ = "decks"
    
    id = db.Column(db.Integer, primary_key=True)

    _deckname = db.Column(db.Text, nullable=False)
    _winrate = db.Column(db.Numeric, nullable=False)
    _popularity = db.Column(db.Numeric, nullable=False)
    _image = db.Column(db.Text, nullable=False)
    

# constructor of a User object, initializes the instance variables within object (self) def __init__(self, price, beds, baths, address, lat, long, sqfeet, image="image"):
def __init__(self,deckname,winrate,popularity,image="image"):
    self._deckname = deckname
    self._winrate = winrate
    self._popularity = popularity
    self._image = image

# Route to fetch deck data
@app.route('/api/decks')
def get_decks():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('instance/volumes/decks.db')
        cursor = conn.cursor()

        # Execute query to fetch deck data
        cursor.execute("SELECT deckname, image, winrate, popularity FROM decks")

        # Fetch all rows
        rows = cursor.fetchall()

        # Close connection
        conn.close()

        # Convert rows to list of dictionaries
        decks_data = []
        for row in rows:
            deck = {
                "deckname": row[0],
                "image": row[1],
                "winrate": row[2],
                "popularity": row[3]
            }
            decks_data.append(deck)

        return jsonify(decks_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 