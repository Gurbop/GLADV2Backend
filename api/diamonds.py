from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api, Resource
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

diamonds_api = Blueprint('diamonds_api', __name__, url_prefix='/api/diamonds')
api = Api(diamonds_api)

class DiamondsAPI(Resource):
    def __init__(self):
        # Preprocess the diamonds dataset on initialization
        diamonds_data = sns.load_dataset('diamonds')
        self.model = self.setup_model(diamonds_data)
        
    def setup_model(self, dataset):
        """Prepare the dataset and train the RandomForestRegressor model."""
        diamonds = dataset.copy()
        # Convert categorical columns to numerical
        diamonds['cut'] = diamonds['cut'].map({'Fair': 0, 'Good': 1, 'Very Good': 2, 'Premium': 3, 'Ideal': 4})
        diamonds['color'] = diamonds['color'].map({'J': 0, 'I': 1, 'H': 2, 'G': 3, 'F': 4, 'E': 5, 'D': 6})
        diamonds['clarity'] = diamonds['clarity'].map({'I1': 0, 'SI2': 1, 'SI1': 2, 'VS2': 3, 'VS1': 4, 'VVS2': 5, 'VVS1': 6, 'IF': 7})
        # Split features and target
        X = diamonds.drop('price', axis=1)
        y = diamonds['price']
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Train the RandomForestRegressor model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        # Evaluate model
        train_rmse = mean_squared_error(y_train, model.predict(X_train), squared=False)
        test_rmse = mean_squared_error(y_test, model.predict(X_test), squared=False)
        print(f'Train RMSE: {train_rmse:.2f}, Test RMSE: {test_rmse:.2f}')
        return model
        
    def predict_price(self, data):
        """Predict price of a diamond based on its characteristics."""
        try:
            diamond_data = pd.DataFrame([data])
            # Convert categorical columns to numerical
            diamond_data['cut'] = diamond_data['cut'].map({'Fair': 0, 'Good': 1, 'Very Good': 2, 'Premium': 3, 'Ideal': 4})
            diamond_data['color'] = diamond_data['color'].map({'J': 0, 'I': 1, 'H': 2, 'G': 3, 'F': 4, 'E': 5, 'D': 6})
            diamond_data['clarity'] = diamond_data['clarity'].map({'I1': 0, 'SI2': 1, 'SI1': 2, 'VS2': 3, 'VS1': 4, 'VVS2': 5, 'VVS1': 6, 'IF': 7})
            # Predict price
            predicted_price = self.model.predict(diamond_data)[0]
            return {'price': round(predicted_price, 2)}  # Return in the expected format
        except Exception as e:
            return {'error': str(e)}
            
    def post(self):
        """Handle POST request and return prediction."""
        try:
            data = request.get_json()
            result = self.predict_price(data)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)})

api.add_resource(DiamondsAPI, '/predict')