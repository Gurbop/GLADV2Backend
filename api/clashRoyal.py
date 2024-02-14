from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, request, Resource # used for REST API building
import requests  # used for testing
import random
from __init__ import app, db
from model.clashroyal import ClashRoyaleCard, Collection
from model.users import User
import os
from cryptography.fernet import Fernet
from sqlalchemy.sql.expression import func

cards_api = Blueprint('house', __name__, url_prefix='/api/card')


api = Api(cards_api)

class Card:

    class _CardList(Resource):
        def get(self):
            cards = [card.fewDetails() for card in ClashRoyaleCard.query.all()]
            return jsonify(cards)
        
    class _commonChest(Resource):
        def get(self):
            # Query for cards with "common" or "rare" rarity and get a random selection of 8
            cards = db.session.query(ClashRoyaleCard).filter(ClashRoyaleCard.rarity.in_(["common", "rare", "epic"])).order_by(func.random()).limit(8).all()
            for card in cards:
                collectionCard = Collection(user_id=request.args.get("id"), card_id=card.id)
                db.session.add(collectionCard)
                db.session.commit()
            # Serialize the cards and return them as JSON
            return jsonify([card.fewDetails() for card in cards])
    
    class _legendaryChest(Resource):
        def get(self):
            cards = db.session.query(ClashRoyaleCard).filter(ClashRoyaleCard.rarity.in_(["epic", "legendary"])).order_by(func.random()).limit(4).all()
            for card in cards:
                collectionCard = Collection(user_id=request.args.get("id"), card_id=card.id)
                db.session.add(collectionCard)
                db.session.commit()
            # Serialize the cards and return them as JSON
            return jsonify([card.fewDetails() for card in cards])
    
    class _getCollection(Resource):
        def get(self):
            cards_id = set([collection.card_id for collection in db.session.query(Collection).filter(Collection.user_id == request.args.get("id")).all()])
            cards = [db.session.query(ClashRoyaleCard).filter(ClashRoyaleCard.id == card).first() for card in cards_id]
            return jsonify([card.fewDetails() for card in cards])

    api.add_resource(_CardList, "/cards")
    api.add_resource(_commonChest, "/commonChest")
    api.add_resource(_legendaryChest, "/legendaryChest")
    api.add_resource(_getCollection, "/getCollection")