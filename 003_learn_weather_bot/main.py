import os
import telebot
from bot_types import ContentType
from open_weather_map import OpenWeatherMap
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.environ['API_TOKEN']

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Hi? nice to see you.\nSend me city name.")


@bot.message_handler(content_types=[ContentType.TEXT])
def get_weather(message: telebot.types.Message):
    city = message.text.strip().lower()
    weather = OpenWeatherMap(city)
    weather.requests_weather()
    data = weather.get_weather()
    if data.get('cod') == 200:
        bot.reply_to(
            message,
            f"Temperature: {data.get('temp')} °C\n"
            f"Feels like: {data.get('feels_like')} °C\n"
            f"Other: {data.get('main_weather')} / {data.get('weather_description')}"
        )
        lat = data.get('location').get('lat')
        lon = data.get('location').get('lon')
        bot.send_location(message.chat.id, lat, lon)
    else:
        bot.reply_to(message, f"Error: {data.get('message')}")
    image = open('resources/have-a-wonderful-day.jpg', 'rb')
    bot.send_photo(message.chat.id, image)

bot.polling(none_stop=True)
