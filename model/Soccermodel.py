import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression

class SoccerScoreModel:
    """A class used to represent the Soccer Score Prediction Model."""
    
    _instance = None
    
    def __init__(self):
        self.model = None
        self.dt = None
        self.features = ['home_score', 'tournament', 'city', 'country', 'neutral']
        self.target = None
        self.soccer_data = None
    
    def _clean(self):
        # Drop rows with missing values in relevant columns
        self.soccer_data.dropna(subset=self.features, inplace=True)
        # Convert categorical columns to appropriate data types if needed
    
    def _train(self):
        X = self.soccer_data[self.features]
        y = self.soccer_data[self.target]
        self.model = LinearRegression()
        self.model.fit(X, y)
        self.dt = DecisionTreeRegressor()
        self.dt.fit(X, y)
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._load_data()
            cls._instance._clean()
            cls._instance._set_target()
            cls._instance._train()
        return cls._instance
    
    def _load_data(self):
        self.soccer_data = pd.read_csv('results.csv')
    
    def _set_target(self):
        # Assuming the team with higher score wins, we can create a target based on home_score and away_score
        self.soccer_data['home_wins'] = (self.soccer_data['home_score'] > self.soccer_data['away_score']).astype(int)
        self.target = 'home_wins'
    
    def predict_winner_likelihood(self, team1, team2):
        # Filter past data for matches involving the two teams
        team1_matches = self.soccer_data[(self.soccer_data['home_team'] == team1) | (self.soccer_data['away_team'] == team1)]
        team2_matches = self.soccer_data[(self.soccer_data['home_team'] == team2) | (self.soccer_data['away_team'] == team2)]
        # Concatenate the filtered data to get all matches involving both teams
        matches = pd.concat([team1_matches, team2_matches])
        # Check if matches DataFrame is empty
        if matches.empty:
            return {"error": "No past matches found for the given teams."}
        # Calculate the average goals scored by each team in past matches
        team1_avg_score = (matches[matches['home_team'] == team1]['home_score'].mean() or 0) + (matches[matches['away_team'] == team1]['away_score'].mean() or 0)
        team2_avg_score = (matches[matches['home_team'] == team2]['home_score'].mean() or 0) + (matches[matches['away_team'] == team2]['away_score'].mean() or 0)
        # Calculate the total goals scored in past matches involving both teams
        total_score = team1_avg_score + team2_avg_score
        # Calculate the percentage likelihood for each team to win
        team1_likelihood = (team1_avg_score / total_score) * 100
        team2_likelihood = (team2_avg_score / total_score) * 100
        return {team1: team1_likelihood, team2: team2_likelihood}
    
    def feature_weights(self):
        return {feature: importance for feature, importance in zip(self.features, self.dt.feature_importances_)}
