import requests
import pandas as pd
import numpy as np
import pytz
import os
import joblib
from datetime import datetime, timedelta
from django.shortcuts import render
from dotenv import load_dotenv

# --- Load Environment Variables and API Key ---
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5/'

# --- Load Pre-trained Models and Encoder ---
# This happens only once when the server starts, making it very fast.
try:
    MODEL_DIR = os.path.join(os.path.dirname(__file__), 'static', 'models')
    rain_model = joblib.load(os.path.join(MODEL_DIR, 'rain_model.joblib'))
    temp_model = joblib.load(os.path.join(MODEL_DIR, 'temp_model.joblib'))
    hum_model = joblib.load(os.path.join(MODEL_DIR, 'hum_model.joblib'))
    label_encoder = joblib.load(os.path.join(MODEL_DIR, 'label_encoder.joblib'))
except FileNotFoundError:
    # Handle case where models are not trained yet
    rain_model = temp_model = hum_model = label_encoder = None
    print("MODELS NOT FOUND. Please run train_models.py first.")


# --- 1. Fetch Current Weather Data (with Error Handling) ---
def get_current_weather(city):
    """Fetches current weather data from OpenWeatherMap API with error handling."""
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return None  # Return None if city not found or API error

    data = response.json()
    
    # Use .get() to avoid KeyErrors if a field is missing
    main_data = data.get('main', {})
    wind_data = data.get('wind', {})

    return {
        'city': data.get('name', 'N/A'),
        'current_temp': main_data.get('temp', 0),
        'feels_like': main_data.get('feels_like', 0),
        'temp_min': main_data.get('temp_min', 0),
        'temp_max': main_data.get('temp_max', 0),
        'humidity': main_data.get('humidity', 0),
        'pressure': main_data.get('pressure', 0),
        'wind_gust_speed': wind_data.get('speed', 0), # Use 'speed' as 'gust' is often missing
        'wind_gust_dir': wind_data.get('deg', 0),
        'description': data.get('weather', [{}])[0].get('description', 'N/A').title(),
        'country': data.get('sys', {}).get('country', 'N/A'),
        'clouds': data.get('clouds', {}).get('all', 0),
        'visibility': data.get('visibility', 0) / 1000, # Convert to km
    }

# --- 2. Predict Future Values ---
def predict_future(model, current_value, steps=5):
    """Predicts future values using a trained regression model."""
    predictions = [current_value]
    for _ in range(steps):
        next_value = model.predict(np.array([[predictions[-1]]]))
        predictions.append(next_value[0])
    return predictions[1:] # Return only the 5 future predictions

# --- 3. Main Django View ---
def weather_view(request):
    context = {}
    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            current_weather = get_current_weather(city)

            # If city is invalid or API fails, render with an error message
            if current_weather is None:
                context['error'] = f"Could not find weather data for '{city}'. Please try another city."
                return render(request, 'weather.html', context)
            
            # --- Prepare Data for Rain Prediction ---
            wind_deg = current_weather['wind_gust_dir'] % 360
            compass_points = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
            compass_direction = compass_points[int((wind_deg + 11.25) / 22.5)]
            
            try:
                compass_direction_encoded = label_encoder.transform([compass_direction])[0]
            except ValueError:
                # If direction is not in training data, use a default value (e.g., -1 or mode)
                compass_direction_encoded = -1 

            # Create a DataFrame for prediction
            current_df = pd.DataFrame([{
                'MinTemp': current_weather['temp_min'],
                'MaxTemp': current_weather['temp_max'],
                'WindGustDir': compass_direction_encoded,
                'WindGustSpeed': current_weather['wind_gust_speed'],
                'Humidity': current_weather['humidity'],
                'Pressure': current_weather['pressure'],
                'Temp': current_weather['current_temp'],
            }])

            # --- Make Predictions ---
            # Check if models are loaded before trying to predict
            if all([rain_model, temp_model, hum_model]):
                rain_prediction_code = rain_model.predict(current_df)[0]
                rain_prediction = 'Yes' if rain_prediction_code == 1 else 'No'

                future_temp = predict_future(temp_model, current_weather['current_temp'])
                future_humidity = predict_future(hum_model, current_weather['humidity'])
            else:
                # Set default values if models aren't loaded
                rain_prediction, future_temp, future_humidity = "N/A", [0]*5, [0]*5

            # --- Prepare Time for Forecast ---
            timezone = pytz.timezone('Asia/Kolkata') # Changed to standard timezone name for Delhi
            now = datetime.now(timezone)
            next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
            future_times = [(next_hour + timedelta(hours=i)).strftime("%H:00") for i in range(5)]
            
            # --- Build Context for Template ---
            context = {
                'location': city,
                'current_temp': f"{current_weather['current_temp']:.0f}°C",
                'MinTemp': f"{current_weather['temp_min']:.0f}°",
                'MaxTemp': f"{current_weather['temp_max']:.0f}°",
                'feels_like': f"{current_weather['feels_like']:.0f}°C",
                'humidity': f"{current_weather['humidity']}%",
                'clouds': f"{current_weather['clouds']}%",
                'description': current_weather['description'],
                'city': current_weather['city'],
                'country': current_weather['country'],
                'date': now.strftime("%A, %B %d, %Y"),
                'time': now.strftime("%I:%M %p"),
                'wind': f"{current_weather['wind_gust_speed']:.1f}",
                'pressure': f"{current_weather['pressure']}",
                'visibility': f"{current_weather['visibility']:.1f}",
                'rain_tomorrow': rain_prediction,

                # Unpack future forecasts for the template
                'forecast_data': zip(future_times, future_temp, future_humidity)
            }

    return render(request, 'weather.html', context)