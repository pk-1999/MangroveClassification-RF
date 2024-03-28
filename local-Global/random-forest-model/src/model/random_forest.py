import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class RandomForestModel:
    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self, data_file):
        # Read the data from the CSV file
        data = pd.read_csv(data_file)

        # Split the data into features and target variable
        X = data[['red', 'nir', 'swir1', 'swir2']]
        y = data['landcover']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the random forest model
        self.model.fit(X_train, y_train)

        # Evaluate the model's performance on the testing set
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy}")

    def predict(self, features):
        # Make predictions using the trained model
        predictions = self.model.predict(features)
        return predictions