from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///decks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cards = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f"<Deck {self.name}>"

@app.route('/saveDeck', methods=['POST'])
def handle_save_deck():
    data = request.json
    deck_name = data['name']
    card_ids = data['cards']
    if not deck_name or not card_ids:
        return jsonify({'error': 'Missing name or cards'}), 400

    try:
        save_deck(deck_name, card_ids)
        return jsonify({'message': 'Deck saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def save_deck(deck_name, card_ids):
    new_deck = Deck(name=deck_name, cards=','.join(map(str, card_ids)))
    db.session.add(new_deck)
    db.session.commit()

def init_db():
    db.create_all()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)  # Make sure to use debug=False in production