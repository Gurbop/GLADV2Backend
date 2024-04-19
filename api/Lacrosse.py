from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.Lacrossemodel import LacrosseScoreModel 

Lacrosse_api = Blueprint('Lacrosse_api', __name__, url_prefix='/api/Lacrosse')
api = Api(Lacrosse_api)

atlas_players = {
    "Matt Rambo": {
        "team": "Atlas LC",
        "position": "Attack",
        "jersey_number": 1,
        "college": "University of Maryland"
    },
}

archers_players = {
    "Connor Fields": {
        "team": "Archers LC",
        "position": "Attack",
        "jersey_number": 5,
        "college": "University at Albany"
    },
}

class Predict(Resource):
    def post(self):
        # Get the team data from the request
        data = request.get_json()
        # Get the team names from the data
        team1 = data.get('team1')
        team2 = data.get('team2')
        
        if not team1 or not team2:
            return {'error': 'Team names must not be empty'}, 400
        if team1 == team2:
            return {'error': 'A team cannot play against itself'}, 400
    
        # Get the singleton instance of the LacrosseScoreModel
        lacrosse_model = LacrosseScoreModel.get_instance()
        # Predict the winner likelihood of the lacrosse game
        prediction = lacrosse_model.predict_winner(team1, team2)
        return jsonify(prediction)
    

# Add the Predict resource to the API with the /predict endpoint
api.add_resource(Predict, '/predict')

