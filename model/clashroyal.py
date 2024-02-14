from __init__ import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
import pandas as pd

class ClashRoyaleCard(db.Model, UserMixin):
    __tablename__ = 'clash_royale_cards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    max_level = db.Column(db.Integer, nullable=True)
    max_evolution_level = db.Column(db.Integer, nullable=True)
    elixir_cost = db.Column(db.Integer, nullable=True)
    icon_url_medium = db.Column(db.String, nullable=True)
    icon_url_evolution_medium = db.Column(db.String, nullable=True)
    rarity = db.Column(db.String(64), nullable=True)

    collections = relationship("Collection", back_populates="card")

    def __init__(self, name, max_level, max_evolution_level, elixir_cost, icon_url_medium, icon_url_evolution_medium, rarity):
        self.name = name
        self.max_level = max_level
        self.max_evolution_level = max_evolution_level
        self.elixir_cost = elixir_cost
        self.icon_url_medium = icon_url_medium
        self.icon_url_evolution_medium = icon_url_evolution_medium
        self.rarity = rarity

    def _allDetails(self):
        return {
            "id": self.id,
            "name": self.name,
            "max_level": self.max_level,
            "max_evolution_level": self.max_evolution_level,
            "elixir_cost": self.elixir_cost,
            "icon_url_medium": self.icon_url_medium,
            "icon_url_evolution_medium": self.icon_url_evolution_medium,
            "rarity": self.rarity
        }
    
    def fewDetails(self):
        return {
            "id": self.id,
            "name": self.name,
            "elixir_cost": self.elixir_cost,
            "icon_url_medium": self.icon_url_medium,
            "rarity": self.rarity
        }
    
class Collection(db.Model):
    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('clash_royale_cards.id'))

    user = relationship("User", back_populates="collections")
    card = relationship("ClashRoyaleCard", back_populates="collections")

    def __init__(self, user_id, card_id):
        self.user_id = user_id
        self.card_id = card_id

def initCards():
    with app.app_context():
        print("Initializing Clash Royale Cards")
        """Create database and tables"""
        db.create_all()
        card_count = db.session.query(ClashRoyaleCard).count()
        if card_count > 0:
            return
        
        basedir = os.path.abspath(os.path.dirname(__file__))
        # Specify the file path
        file_path = basedir + "/../static/data/clashroyal.csv"
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        for index, row in df.iterrows():
            try:
                card = ClashRoyaleCard(
                    name=row['name'] if pd.notna(row['name']) else None,
                    max_level=row['maxLevel'] if pd.notna(row['maxLevel']) else None,
                    max_evolution_level=row['maxEvolutionLevel'] if pd.notna(row['maxEvolutionLevel']) else None,
                    elixir_cost=row['elixirCost'] if pd.notna(row['elixirCost']) else None,
                    icon_url_medium=row['iconUrls__medium'] if pd.notna(row['iconUrls__medium']) else None,
                    icon_url_evolution_medium=row['iconUrls__evolutionMedium'] if pd.notna(row['iconUrls__evolutionMedium']) else None,
                    rarity=row['rarity'] if pd.notna(row['rarity']) else None
                )
                db.session.add(card)
                db.session.commit()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.rollback()
                print(f"Records exist, duplicate card, or error: {card.name}")
            except Exception as e_inner:
                print(f"Error adding card at index {index}: {str(e_inner)}")
