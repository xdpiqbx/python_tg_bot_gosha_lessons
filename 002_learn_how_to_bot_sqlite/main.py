import os
import telebot
from telebot import types
from dotenv import load_dotenv

from db.database import Database

from user_dto import UserDTO

load_dotenv()
API_TOKEN = os.environ['API_TOKEN']

bot = telebot.TeleBot(API_TOKEN)

user = UserDTO()


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    db = Database()
    db.create_table()
    db.close()

    bot.send_message(message.chat.id, "BD was created.\nSend me your name")
    bot.register_next_step_handler(message, user_name)


def user_name(message: telebot.types.Message):
    user.set_name(message.text.strip())
    bot.send_message(message.chat.id, "Send me Password")
    bot.register_next_step_handler(message, user_password)


def user_password(message: telebot.types.Message):
    user.set_pass(message.text.strip())

    db = Database()
    db.add_new_user((user.get_name(), user.get_pass()))
    db.close()

    user.clear()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("List of users", callback_data='users_list'))

    bot.send_message(message.chat.id, "You have been registered", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'users_list')
def call_users_list(call: telebot.types.CallbackQuery):
    db = Database()
    users = db.get_all_users()
    db.close()

    content = ''
    for u in users:
        content += f"Name: {u[0]}\n"

    bot.send_message(call.message.chat.id, content)
    bot.answer_callback_query(call.id)


bot.polling(none_stop=True)

# @bot.message_handler(commands=['start'])
# def main(message):
#     response = f"Hello, {message.from_user.first_name} {message.from_user.last_name}"
#
#     markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
#
#     btn_site = types.KeyboardButton("site")
#     markup.row(btn_site)
#
#     btn_del = types.KeyboardButton("username")
#     btn_edit = types.KeyboardButton("my id")
#     markup.row(btn_del, btn_edit)
#
#     image = open('db/model.jpg', 'rb')
#
#     bot.send_photo(message.chat.id, image, reply_markup=markup)
#     # bot.send_message(message.chat.id, response, reply_markup=markup)
#     bot.register_next_step_handler(message, on_click)
#
#
# def on_click(message: telebot.types.Message):
#     print("It will work only 1 time after /start command")
#     if message.text.lower() == 'site':
#         bot.send_message(message.chat.id, "Website is open (on_click)")
#     elif message.text.lower() == 'username':
#         bot.send_message(message.chat.id, "Username (on_click)")
#     elif message.text.lower() == 'my id':
#         bot.send_message(message.chat.id, "Your ID (on_click)")
#
#
# @bot.message_handler(commands=['site'])
# def site(message: telebot.types.Message):
#     webbrowser.open("https://github.com/xdpiqbx")
#
#
# @bot.message_handler(commands=['help'])
# def main(message: telebot.types.Message):
#     bot.send_message(message.chat.id, '<b>Help</b> <em><u>info</u></em>', parse_mode=pm.HTML)
#
#
# @bot.message_handler(content_types=[content_type.PHOTO])
# def det_photo(message: telebot.types.Message):
#     # Data to be sent in a callback query to the bot when button is pressed, 1-64 bytes
#     markup = types.InlineKeyboardMarkup()
#
#     btn_site = types.InlineKeyboardButton("Go to site", url="https://github.com/xdpiqbx")
#     markup.row(btn_site)
#
#     btn_del = types.InlineKeyboardButton("Delete photo", callback_data="delete")
#     btn_edit = types.InlineKeyboardButton("Edit text", callback_data="edit")
#     markup.row(btn_del, btn_edit)
#
#     bot.reply_to(message, "So nice image =)", reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda callback: True)
# def callback_message(call: telebot.types.CallbackQuery):
#     if call.data == 'delete':
#         bot.delete_message(call.message.chat.id, call.message.message_id - 1)
#     elif call.data == 'edit':
#         bot.edit_message_text("New text", call.message.chat.id, call.message.message_id)
#
#
# @bot.message_handler()
# def info(message: telebot.types.Message):
#     if message.text.lower() == 'username':
#         bot.send_message(message.chat.id, message.from_user.username)
#     if message.text.lower() == 'my id':
#         bot.reply_to(message, f"Your id is: <b>{message.from_user.id}</b>", parse_mode='html')
#     if message.text.lower() == 'site':
#         webbrowser.open("https://github.com/xdpiqbx")

# In BotFather
# /setcommands

# command1 - Description
# command2 - Another description

# start - Start bot
# site - Open github
