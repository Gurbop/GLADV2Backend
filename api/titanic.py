from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api, Resource
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
import numpy as np
titanic_api = Blueprint('titanic_api', __name__, url_prefix='/api/titanic')
api = Api(titanic_api)
class TitanicAPI(Resource):
    def __init__(self):
        # Preprocess the Titanic dataset on initialization
        titanic_data = sns.load_dataset('titanic')
        self.logreg, self.enc, self.encoded_cols = self.setup_model(titanic_data)
    def setup_model(self, dataset):
        """Prepare the dataset and train the logistic regression model."""
        td = dataset.copy()
        # Drop unnecessary columns and rows with missing values
        td.drop(['alive', 'who', 'adult_male', 'class', 'embark_town', 'deck'], axis=1, inplace=True)
        td.dropna(inplace=True)
        # Convert categorical columns to numerical
        td['sex'] = td['sex'].apply(lambda x: 1 if x == 'male' else 0)
        td['alone'] = td['alone'].apply(lambda x: 1 if x else 0)
        # One-hot encode 'embarked' column
        enc = OneHotEncoder(handle_unknown='ignore')
        embarked_encoded = enc.fit_transform(td[['embarked']].values.reshape(-1, 1))
        encoded_cols = enc.get_feature_names_out(['embarked'])
        td[encoded_cols] = embarked_encoded.toarray()
        td.drop(['embarked'], axis=1, inplace=True)
        # Train the logistic regression model
        logreg = LogisticRegression(max_iter=1000)
        X = td.drop('survived', axis=1)
        y = td['survived']
        logreg.fit(X, y)
        return logreg, enc, encoded_cols
    def predict_survival(self, data):
        """Predict survival probability of a given passenger data."""
        try:
            passenger = pd.DataFrame([data])
            passenger['sex'] = passenger['sex'].apply(lambda x: 1 if x == 'male' else 0)
            passenger['alone'] = passenger['alone'].apply(lambda x: 1 if x else 0)
            # Apply the same preprocessing for 'embarked'
            embarked_encoded = self.enc.transform(passenger[['embarked']].values.reshape(-1, 1))
            passenger[self.encoded_cols] = embarked_encoded.toarray()
            passenger.drop(['embarked', 'name'], axis=1, inplace=True)
            # Predict probabilities
            dead_proba, alive_proba = np.squeeze(self.logreg.predict_proba(passenger))
            return {
                'Death probability': f'{dead_proba:.2%}',
                'Survival probability': f'{alive_proba:.2%}'
            }
        except Exception as e:
            return {'error': str(e)}
    def post(self):
        """Handle POST request and return prediction."""
        try:
            data = request.get_json()
            result = self.predict_survival(data)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)})
api.add_resource(TitanicAPI, '/predict')