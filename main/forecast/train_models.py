import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error

print("Starting model training process...")

# --- 1. Read and Prepare Historical Data ---
def read_historical_data(filename):
    print(f"Reading data from {filename}...")
    df = pd.read_csv(filename)
    df = df.dropna()
    df = df.drop_duplicates()
    print("Data cleaning (dropna, drop_duplicates) complete.")
    return df

# --- 2. Prepare Data for Rain Classification Model ---
def prepare_classification_data(data):
    print("Preparing data for rain classification model...")
    le = LabelEncoder()
    # Important: Ensure the columns exist in your CSV
    data['WindGustDir'] = le.fit_transform(data['WindGustDir'].astype(str))
    data['RainTomorrow'] = le.fit_transform(data['RainTomorrow'].astype(str))
    
    # Define features and target
    X = data[['MinTemp', 'MaxTemp', 'WindGustDir', 'WindGustSpeed', 'Humidity', 'Pressure', 'Temp']]
    y = data['RainTomorrow']
    
    print("LabelEncoder created and data transformed.")
    return X, y, le

# --- 3. Train Rain Prediction Model ---
def train_rain_model(X, y):
    print("Training rain classification model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1) # Use all CPU cores
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    # Use classification metrics instead of regression metrics
    print("\n--- Rain Model Evaluation ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("--- End of Report ---\n")
    
    return model

# --- 4. Prepare Data for Regression Models (Temp/Humidity) ---
def prepare_regression_data(data, feature):
    print(f"Preparing regression data for feature: {feature}...")
    X, y = [], []
    # Create sequences: use previous day's value to predict next day's
    for i in range(len(data) - 1):
        X.append(data[feature].iloc[i])
        y.append(data[feature].iloc[i+1])
        
    X = np.array(X).reshape(-1, 1)
    y = np.array(y)
    return X, y

# --- 5. Train a Regression Model ---
def train_regression_model(X, y, feature_name):
    print(f"Training regression model for {feature_name}...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X, y)
    print(f"Model for {feature_name} trained successfully.")
    return model

# --- Main Execution ---
if __name__ == '__main__':
    # Define paths
    # IMPORTANT: Make sure 'weather.csv' is in the root directory 'WeathrIQ'
    CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'weather.csv')
    MODEL_DIR = os.path.join(os.path.dirname(__file__), 'static', 'models')

    # Create directory for models if it doesn't exist
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        print(f"Created directory: {MODEL_DIR}")

    # Load data
    historical_data = read_historical_data(CSV_PATH)
    
    # --- Train and Save Rain Model ---
    X_rain, y_rain, label_encoder = prepare_classification_data(historical_data.copy()) # Use copy to avoid side effects
    rain_model = train_rain_model(X_rain, y_rain)
    joblib.dump(rain_model, os.path.join(MODEL_DIR, 'rain_model.joblib'))
    joblib.dump(label_encoder, os.path.join(MODEL_DIR, 'label_encoder.joblib'))
    print("Rain model and LabelEncoder saved successfully.")

    # --- Train and Save Temperature Model ---
    X_temp, y_temp = prepare_regression_data(historical_data, 'Temp')
    temp_model = train_regression_model(X_temp, y_temp, 'Temperature')
    joblib.dump(temp_model, os.path.join(MODEL_DIR, 'temp_model.joblib'))
    print("Temperature model saved successfully.")
    
    # --- Train and Save Humidity Model ---
    X_hum, y_hum = prepare_regression_data(historical_data, 'Humidity')
    hum_model = train_regression_model(X_hum, y_hum, 'Humidity')
    joblib.dump(hum_model, os.path.join(MODEL_DIR, 'hum_model.joblib'))
    print("Humidity model saved successfully.")
    
    print("\nAll models have been trained and saved to the 'forecast/static/models' directory.")