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
from api.titanic import titanic_api
from api.diamonds import diamonds_api
from api.NBA import NBA_api
from api.Soccer import soccer_api
from api.Lacrosse import Lacrosse_api
from api.decks import decks_api
from api.book import books_api

# database migrations
from model.users import initUsers
from model.players import initPlayers
from model.clashroyal import initCards
from model.Books import init_books


# setup App pages
# Blueprint directory import projects definition
from projects.projects import app_projects

# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)
initCards()
initUsers()
init_books()

# register URIs
app.register_blueprint(user_api)  # register api routes
app.register_blueprint(player_api)
app.register_blueprint(app_projects)  # register app pages
app.register_blueprint(cards_api)
app.register_blueprint(titanic_api)
app.register_blueprint(diamonds_api)
app.register_blueprint(NBA_api)
app.register_blueprint(soccer_api)
app.register_blueprint(Lacrosse_api)
app.register_blueprint(decks_api)
app.register_blueprint(books_api)


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
    init_books()


# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)

# this runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8050")