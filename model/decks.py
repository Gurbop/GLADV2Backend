from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///decks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Deck(db.Model):
    __tablename__ = 'decks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cards = db.Column(db.String(300), nullable=False)  # Storing card IDs in a comma-separated string

    def __init__(self, name, cards):
        self.name = name
        self.cards = cards

    def __repr__(self):
        return f'<Deck {self.name}>'

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Failed to add deck: {e}")
            return None

def init_db():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        init_db()
        print('Database initialized.')
