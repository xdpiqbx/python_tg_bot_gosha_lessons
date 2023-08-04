import os
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.callback_query import CallbackQuery
from bot_types import ContentType

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.environ['API_TOKEN']

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)


# @dp.message_handler() <- Ok
@dp.message_handler(commands=['start'], content_types=[ContentType.TEXT])
async def start(message: Message):
    # await bot.send_message(message.chat.id, 'Hello')
    # await message.answer("Hello! =)")
    # await message.reply('Just reply')
    photo = open('resources/have-a-wonderful-day.jpg', 'rb')
    await message.answer_photo(photo)


@dp.message_handler(commands=['inline'], content_types=[ContentType.TEXT])
async def inline(message: Message):
    # InlineKeyboardMarkup, InlineKeyboardButton
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Site", url="https://github.com/xdpiqbx"))
    markup.add(InlineKeyboardButton("Hello", callback_data="hello"))
    await message.reply('Keyboard', reply_markup=markup)


@dp.callback_query_handler()
async def _(call: CallbackQuery):
    await call.message.answer(call.data)
    await bot.answer_callback_query(call.id)


@dp.message_handler(commands=['reply'])
async def reply(message: Message):
    # ReplyKeyboardMarkup, KeyboardButton
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(KeyboardButton("Google"))
    markup.add(KeyboardButton("Mail"))
    await message.answer('It is ReplyKeyboardMarkup', reply_markup=markup)


executor.start_polling(dp)
