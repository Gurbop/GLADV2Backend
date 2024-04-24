from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)

# Define your models here

@app.cli.command('loaddata')
def load_data():
    df = pd.read_csv('results.csv')
    # Assume Match is a model defined to match the CSV structure
    for index, row in df.iterrows():
        match = Match(
            date=row['date'],
            home_team=row['home_team'],
            away_team=row['away_team'],
            home_score=row['home_score'],
            away_score=row['away_score'],
            tournament=row['tournament'],
            city=row['city'],
            country=row['country'],
            neutral=row['neutral']
        )
        db.session.add(match)
    db.session.commit()
    print("Data loaded successfully.")

if __name__ == '__main__':
    app.run(debug=True)
