import os
import webbrowser
from dotenv import load_dotenv
from bot_types import MIMEType as mime, ContentType as content_type, ParseMode as pm

import telebot
from telebot import types

load_dotenv()
API_TOKEN = os.environ['API_TOKEN']

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def main(message):
    response = f"Hello, {message.from_user.first_name} {message.from_user.last_name}"

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    btn_site = types.KeyboardButton("site")
    markup.row(btn_site)

    btn_del = types.KeyboardButton("username")
    btn_edit = types.KeyboardButton("my id")
    markup.row(btn_del, btn_edit)

    image = open('resources/model.jpg', 'rb')

    bot.send_photo(message.chat.id, image, reply_markup=markup)
    # bot.send_message(message.chat.id, response, reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message: telebot.types.Message):
    print("It will works only 1 time after /start command")
    if message.text.lower() == 'site':
        bot.send_message(message.chat.id, "Website is open (on_click)")
    elif message.text.lower() == 'username':
        bot.send_message(message.chat.id, "Username (on_click)")
    elif message.text.lower() == 'my id':
        bot.send_message(message.chat.id, "Your ID (on_click)")


@bot.message_handler(commands=['site'])
def site(message: telebot.types.Message):
    webbrowser.open("https://github.com/xdpiqbx")


@bot.message_handler(commands=['help'])
def main(message: telebot.types.Message):
    bot.send_message(message.chat.id, '<b>Help</b> <em><u>info</u></em>', parse_mode=pm.HTML)


@bot.message_handler(content_types=[content_type.PHOTO])
def det_photo(message: telebot.types.Message):
    # Data to be sent in a callback query to the bot when button is pressed, 1-64 bytes
    markup = types.InlineKeyboardMarkup()

    btn_site = types.InlineKeyboardButton("Go to site", url="https://github.com/xdpiqbx")
    markup.row(btn_site)

    btn_del = types.InlineKeyboardButton("Delete photo", callback_data="delete")
    btn_edit = types.InlineKeyboardButton("Edit text", callback_data="edit")
    markup.row(btn_del, btn_edit)

    bot.reply_to(message, "So nice image =)", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(call: telebot.types.CallbackQuery):
    if call.data == 'delete':
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)
    elif call.data == 'edit':
        bot.edit_message_text("New text", call.message.chat.id, call.message.message_id)


@bot.message_handler()
def info(message: telebot.types.Message):
    if message.text.lower() == 'username':
        bot.send_message(message.chat.id, message.from_user.username)
    if message.text.lower() == 'my id':
        bot.reply_to(message, f"Your id is: <b>{message.from_user.id}</b>", parse_mode='html')
    if message.text.lower() == 'site':
        webbrowser.open("https://github.com/xdpiqbx")


bot.polling(none_stop=True)

# In BotFather
# /setcommands

# command1 - Description
# command2 - Another description

# start - Start bot
# site - Open github
