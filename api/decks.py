from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///decks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cards = db.Column(db.String(300), nullable=False)  # Card IDs stored as a comma-separated string

    def __repr__(self):
        return f'<Deck {self.name}>'

@app._got_first_request
def create_tables():
    db.create_all()

@app.route('/save_deck', methods=['POST'])
def save_deck():
    data = request.get_json()
    name = data.get('name')
    cards = ','.join(data.get('cards', []))  # Convert list of cards to a comma-separated string

    if not name or not cards:
        return jsonify({'error': 'Deck name and cards are required'}), 400

    new_deck = Deck(name=name, cards=cards)
    db.session.add(new_deck)
    db.session.commit()

    return jsonify({'message': f'Deck "{name}" saved successfully'}), 201

@app.route('/get_decks', methods=['GET'])
def get_decks():
    decks = Deck.query.all()
    decks_data = [{'name': deck.name, 'cards': deck.cards.split(',')} for deck in decks]
    return jsonify(decks_data), 200

if __name__ == '__main__':
    app.run(debug=True)