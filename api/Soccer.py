import pandas as pd
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.Soccermodel import SoccerScoreModel  # Import the soccer model class

soccer_api = Blueprint('soccer_api', __name__, url_prefix='/api/soccer')
api = Api(soccer_api)

class Predict(Resource):
    def post(self):
        # Get the team data from the request
        data = request.get_json()

        # Get the team names from the data
        team1 = data.get('team1')
        team2 = data.get('team2')

        # Validate the team names
        if not team1 or not team2:
            return {'error': 'Team names must not be empty'}, 400
        if team1 == team2:
            return {'error': 'A team cannot play against itself'}, 400

        # Get the singleton instance of the SoccerScoreModel
        soccer_model = SoccerScoreModel.get_instance()

        # Predict the winner likelihood of the soccer game
        likelihood = soccer_model.predict_winner_likelihood(team1, team2)

        # Check if the model returned an error
        if "error" in likelihood:
            return likelihood, 400

        # If no error, return the likelihood scores
        return likelihood

api.add_resource(Predict, '/predict')