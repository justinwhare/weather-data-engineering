import requests
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="weather-data-project/.env")

api_key = os.getenv('api_key')
api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query=Halifax"

def fetch_data():
    print("Fetching weather data from Weatherstack API...")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print("API called successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        raise