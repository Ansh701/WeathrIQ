WeathrIQ 🌦️
An intelligent real-time weather forecasting application powered by Django and Machine Learning.
<p align="center">
<a href="https://weathriq.onrender.com" target="_blank">
<img src="https://img.shields.io/badge/Live%20Demo-Visit%20WeathrIQ-brightgreen?style=for-the-badge&logo=render" alt="Live Demo">
</a>
</p>

<p align="center">
<a href="https://weathriq.onrender.com" target="_blank">
<!-- IMPORTANT: Replace this with a real screenshot or GIF of your application -->
<img src="https://i.imgur.com/your-screenshot-id.png" alt="WeathrIQ Application Screenshot" width="80%">
</a>
</p>

🚀 About The Project
WeathrIQ is more than just a weather app. It's a full-stack web application demonstrating the integration of a robust Django backend with a dynamic, visually appealing frontend. The project leverages machine learning models to provide not just current weather data, but also insightful predictions for future conditions.

From live weather data fetched from the OpenWeatherMap API to AI-powered rain predictions, WeathrIQ is designed to be both functional and beautiful.

🌟 Core Features
Live Weather Data: Fetches up-to-the-minute weather conditions for any city in the world.

5-Hour Future Forecast: Uses AI to predict temperature and humidity for the next five hours.

AI-Powered Rain Prediction: A trained RandomForestClassifier predicts the likelihood of rain for the following day.

Dynamic & Immersive UI: The interface background and elements change based on the current weather, providing a unique experience for each location.

Interactive Data Visualization: Hourly forecast data is beautifully rendered using Chart.js.

Responsive Design: Looks and works great on all devices, from mobile phones to desktops.

🛠️ Technology Stack
The project is built with a modern and powerful stack:

Backend

Frontend

Deployment & Tooling































⚙️ Setup & Installation
To get a local copy up and running, follow these simple steps.

Prerequisites
Python 3.9+

pip

Installation
Clone the repository:

git clone https://github.com/your-username/WeathrIQ.git

Navigate to the project directory:

cd WeathrIQ

Navigate to the Django project root:

cd main

Install dependencies:

pip install -r requirements.txt

Set up environment variables:

Create a .env file inside the main directory.

Add your API key: OPENWEATHER_API_KEY='your_key_here'

Train the ML Models:

This is a one-time step to generate the model files. Make sure weather.csv is present in the main directory.

python train_models.py

Run the Django Server:

python manage.py runserver

Your application will be available at http://127.0.0.1:8000/.

🌐 Live Demo
Check out the live, deployed version of the application:

https://weathriq.onrender.com
