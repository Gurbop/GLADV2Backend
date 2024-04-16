import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression

class LacrosseScoreModel:
    _instance = None

    def __init__(self):
        self.model = None
        self.dt = None
        self.features = ['wins', 'losses', 'score_differential', 'two_point_goals', 'assists', 'shots',
                         'shots_on_goal', 'turnovers', 'caused_turnovers', 'groundballs', 'faceoff_pecentage',
                         'saves', 'save_percentage', 'penalties', 'penalty_minutes', 'power_play_pecentage',
                         'power_play_goals', 'power_play_shots', 'x2_point_goals_allowed', 'penalty_kill_pecentage']
        self.target = 'wins'
        self.lacrosse_data = None
        self._load_data()
        self._clean()
        self._train()

    def _clean(self):
        self.lacrosse_data.dropna(subset=self.features + [self.target], inplace=True)

    def _train(self):
        X = self.lacrosse_data[self.features]
        y = self.lacrosse_data[self.target]
        # Splitting the data for training and testing
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        self.dt = DecisionTreeRegressor()
        self.dt.fit(X_train, y_train)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_data(self):
        self.lacrosse_data = pd.read_csv('lacrosse.csv')
        self.lacrosse_data['wins'] = (self.lacrosse_data['score_differential'] > 0).astype(int)  # Assuming win based on positive score differential

    def predict_winner(self, team1, team2):
        team1_data = self.lacrosse_data[self.lacrosse_data['team'] == team1]
        team2_data = self.lacrosse_data[self.lacrosse_data['team'] == team2]

        team1_score = self.calculate_composite_score(team1_data)
        team2_score = self.calculate_composite_score(team2_data)

        total_score = team1_score + team2_score
        team1_chance = (team1_score / total_score) * 100
        team2_chance = (team2_score / total_score) * 100

        return {
            team1: f"{team1_chance:.2f}%",
            team2: f"{team2_chance:.2f}%"
        }

    def calculate_composite_score(self, team_data):
        # Calculate composite score based on various factors
        composite_score = team_data['score_differential'].mean() + \
                          team_data['two_point_goals'].mean() + \
                          team_data['assists'].mean() + \
                          team_data['shots'].mean() + \
                          team_data['shots_on_goal'].mean() + \
                          team_data['saves'].mean() + \
                          team_data['caused_turnovers'].mean() + \
                          team_data['groundballs'].mean() + \
                          team_data['faceoff_pecentage'].mean() + \
                          team_data['power_play_goals'].mean() - \
                          team_data['turnovers'].mean() - \
                          team_data['scores_against'].mean() - \
                          team_data['x2_point_goals_allowed'].mean() - \
                          team_data['penalties'].mean() - \
                          team_data['penalty_minutes'].mean() - \
                          team_data['power_play_pecentage'].mean() - \
                          team_data['penalty_kill_pecentage'].mean()

        return composite_score

# Composite score for each team based on score differential, goals, assists, shots, saves, turnovers, scores against, penalties, etc. 
# Deducts certain factors such as turnovers, scores against, penalties, etc., as they are expected to negatively impact performance.
# Considers a broader range of factors compared to just averaging the data resulting in a more accurate prediction.