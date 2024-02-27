# import threading

# import "packages" from flask
# import render_template from "public" flask libraries
from flask import render_template, request
from flask.cli import AppGroup

     
# import "packages" from "this" project
# from __init__ import app, db, cors  # Definitions initializatio
from __init__ import app, db, cors


# setup APIs
from api.user import user_api  # Blueprint import api definition
from api.clashRoyal import cards_api
from api.player import player_api
# database migrations
from model.users import initUsers
from model.players import initPlayers
from model.clashroyal import initCards

# setup App pages
# Blueprint directory import projects definition
from projects.projects import app_projects

# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)
initCards()
initUsers()

# register URIs
app.register_blueprint(user_api)  # register api routes
app.register_blueprint(player_api)
app.register_blueprint(app_projects)  # register app pages
app.register_blueprint(cards_api)

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")


@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")

"""@app.before_first_request
def activate_job():  # activate these items 
    initCards()
    initUsers()"""

'''
@app.before_request
def before_request():
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:4100', 'http://127.0.0.1:4100', 'https://nighthawkcoders.github.io', 'https://real-estate-analyzation.github.io']:
        cors._origins = allowed_origin
    

@app.after_request
def after_request(response):
    #response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    #allowed_origins = ['http://localhost:8080', 'http://localhost:4200', 'http://127.0.0.1:4200', 'https://nighthawkcoders.github.io', 'https://real-estate-analyzation.github.io']

    #origin = request.headers.get('Origin')
    #if origin and origin in allowed_origins:
    #    response.headers.add('Access-Control-Allow-Origin', origin)

    response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin'))
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
'''

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data


@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initCards()
    initPlayers()


# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)
from flask import Flask, jsonify
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImJjOWNhYTM0LTQ0MzUtNDc4ZC04MDViLTFkMGJmYTFjMWQ0NSIsImlhdCI6MTcwNzg4MDIxMiwic3ViIjoiZGV2ZWxvcGVyL2RkMDFmNzBiLTgzNGEtNzYyOC05ZGU3LWMxNWZjOWMxMGIxZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI0NC4yMzYuMTE2LjkzIl0sInR5cGUiOiJjbGllbnQifV19.T_P7gbpb8ZKsGUj2_1FmZx-2h7nEtn4rkfyxhse_Ky28lSVNpo2I9ohZ_lGDBU9q-AHfKA6J-JGIKafamHgYyg"
# API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjVlODJjNmViLTYwMmMtNGVlMy04YTAyLTEzODViMzdiY2Y2NCIsImlhdCI6MTcwODA2MDQzNywic3ViIjoiZGV2ZWxvcGVyLzRjNzAwZDc4LWQzNjUtYTZlYS1jMjNiLTlhYjY5M2JiNzA1OSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMDQuMzUuMjcuNzYiLCIwLjAuMC4wIl0sInR5cGUiOiJjbGllbnQifV19.1jtGW1R8VwviHEcymktxn7AEKC-kQTpWJdCgOh_2mfbz792-PXrVH4BmN76Tm_v5YMBal43iAZsX4p1vjbOijg"
API_BASE_URL = 'https://api.clashroyale.com/v1'
@app.route('/')
def home():
    return "Clash Royale Dashboard Backend"
@app.route('/challenges')
def fetch_challenges():
    url = f"https://api.clashroyale.com/v1/challenges"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(url, headers=headers)
    if response.ok:
        data = response.json()
        challenges_list = []
        for item in data:
            challenges_list.extend(item.get('challenges', []))
        return jsonify(challenges_list)
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code
@app.route('/tournaments')
def get_tournaments():
    tournament_name = request.args.get('name', 'ydkv')  # Default value 'ydkv' if name parameter not provided
    url = f'https://api.clashroyale.com/v1/tournaments?name={tournament_name}'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(url, headers=headers)
    if response.ok:
        return jsonify(response.json().get('items', []))  # Send back a list of items
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code

@app.route('/players')
def get_players():
    player_name = request.args.get('name', 'LLUU0LVC')  # Default value 'ydkv' if name parameter not provided
    url = f'https://api.clashroyale.com/v1/players?name={player_name}'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(url, headers=headers)
    if response.ok:
        return jsonify(response.json().get('items', []))  # Send back a list of items
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code
@app.route('/leaderboard')
def get_leaderboard():
    season = request.args.get('season', '1')  # Default to season 1 if not specified
    url = f'https://api.clashroyale.com/v1/locations/global/seasons/{season}/rankings/players?limit=10'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(url, headers=headers)
    if response.ok:
        return jsonify(response.json().get('items', []))  # Send back a list of items
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code
      
# this runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8086")
