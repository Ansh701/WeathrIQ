import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report

print("Starting model training process...")

def read_historical_data(filename):
    print(f"Reading data from {filename}...")
    df = pd.read_csv(filename)
    df = df.dropna()
    df = df.drop_duplicates()
    print("Data cleaning complete.")
    return df

def prepare_classification_data(data):
    print("Preparing data for rain classification model...")
    le = LabelEncoder()
    data['WindGustDir'] = le.fit_transform(data['WindGustDir'].astype(str))
    data['RainTomorrow'] = le.fit_transform(data['RainTomorrow'].astype(str))
    X = data[['MinTemp', 'MaxTemp', 'WindGustDir', 'WindGustSpeed', 'Humidity', 'Pressure', 'Temp']]
    y = data['RainTomorrow']
    return X, y, le

def train_rain_model(X, y):
    print("Training rain classification model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    return model

def prepare_regression_data(data, feature):
    X, y = [], []
    for i in range(len(data) - 1):
        X.append(data[feature].iloc[i])
        y.append(data[feature].iloc[i+1])
    return np.array(X).reshape(-1, 1), np.array(y)

def train_regression_model(X, y, feature_name):
    print(f"Training regression model for {feature_name}...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X, y)
    return model

if __name__ == '__main__':
    CSV_PATH = 'weather.csv' 
    MODEL_DIR = os.path.join('main', 'forecast', 'static', 'models')
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    
    historical_data = read_historical_data(CSV_PATH)
    
    X_rain, y_rain, label_encoder = prepare_classification_data(historical_data.copy())
    rain_model = train_rain_model(X_rain, y_rain)
    joblib.dump(rain_model, os.path.join(MODEL_DIR, 'rain_model.joblib'))
    joblib.dump(label_encoder, os.path.join(MODEL_DIR, 'label_encoder.joblib'))
    
    X_temp, y_temp = prepare_regression_data(historical_data, 'Temp')
    temp_model = train_regression_model(X_temp, y_temp, 'Temperature')
    joblib.dump(temp_model, os.path.join(MODEL_DIR, 'temp_model.joblib'))
    
    X_hum, y_hum = prepare_regression_data(historical_data, 'Humidity')
    hum_model = train_regression_model(X_hum, y_hum, 'Humidity')
    joblib.dump(hum_model, os.path.join(MODEL_DIR, 'hum_model.joblib'))
    
    print("\nAll models have been trained and saved.")