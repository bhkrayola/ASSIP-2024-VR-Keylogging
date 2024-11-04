import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

file_path = "output.csv"
data = pd.read_csv(file_path, header=None, names=['Keystroke', 'X', 'Y', 'Z'])

#Encode keystrokes as integers
keystrokes = data['Keystroke'].unique()
keystroke_to_int = {key: idx for idx, key in enumerate(keystrokes)}
int_to_keystroke = {idx: key for key, idx in keystroke_to_int.items()}
data['Keystroke'] = data['Keystroke'].map(keystroke_to_int)

X = data[['X', 'Y', 'Z']].values
y = data['Keystroke'].values

#Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Train
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

#Evaluate
y_pred = knn.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

#Function to predict keystrokes for new data
def predict_keystroke(X_new):
    y_new_pred = knn.predict(X_new)
    return [int_to_keystroke[keystroke] for keystroke in y_new_pred]

import joblib
joblib.dump(knn, 'knn_model.joblib')
