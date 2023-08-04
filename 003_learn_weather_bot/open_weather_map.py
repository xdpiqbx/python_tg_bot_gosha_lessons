import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ['OPEN_WEATHER_MAP_API_KEY']

endpoint = "https://api.openweathermap.org/data/2.5/weather"

class OpenWeatherMap:
    def __init__(self, city):
        self.city = city
        self.weather = dict()
        self.response_code = 0

    def requests_weather(self):
        params = {
            'q': self.city,
            'units': 'metric',
            'appid': API_KEY
        }
        response = requests.get(endpoint, params=params)
        print(response.url)
        result = response.json()
        self.response_code = int(result.get('cod'))
        self.weather = result

    def get_weather(self):
        if self.response_code == 200:
            return {
                'cod': self.response_code,
                'temp': self.weather.get('main').get('temp'),
                'feels_like': self.weather.get('main').get('feels_like'),
                'main_weather': self.weather.get('weather')[0].get('main'),
                'weather_description': self.weather.get('weather')[0].get('description'),
                'location': self.weather.get('coord')
            }
        return {
            'cod': self.response_code,
            'message': self.weather.get('message') if self.weather.get('message') else "Unknown ERROR"
        }
