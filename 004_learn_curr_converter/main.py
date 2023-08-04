import os
from currency_converter import CurrencyConverter
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.environ['API_TOKEN']

bot = telebot.TeleBot(API_TOKEN)
currency = CurrencyConverter()
amount = 0

curr_pairs = ('USD/EUR', 'EUR/USD', 'USD/GBP')


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Hi!\nSend me amount")
    bot.register_next_step_handler(message, summ)


def summ(message: telebot.types.Message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Are you idiot?\nDo not respond...')
        bot.register_next_step_handler(message, summ)
        return

    if amount < 1:
        bot.send_message(message.chat.id, 'Do not play with me')
        bot.register_next_step_handler(message, summ)
        return

    markup = InlineKeyboardMarkup(row_width=2)

    usd_eur = InlineKeyboardButton('USD/EUR', callback_data='USD/EUR')
    eur_usd = InlineKeyboardButton('EUR/USD', callback_data='EUR/USD')
    usd_gbp = InlineKeyboardButton('USD/GBP', callback_data='USD/GBP')
    other = InlineKeyboardButton('Other value', callback_data='OTHER')

    markup.add(usd_eur, eur_usd, usd_gbp, other)

    bot.send_message(message.chat.id, 'Choose pair:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in curr_pairs)
def callback(call: telebot.types.CallbackQuery):
    base_curr, quote_curr = call.data.split('/')
    result = currency.convert(amount, base_curr, quote_curr)
    bot.send_message(
        call.message.chat.id,
        f"Result is: {round(result, 2)} {quote_curr}.\n"
        f"You can give me another amount for {base_curr}/{quote_curr}"
    )
    # bot.register_next_step_handler(call.message, summ)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'OTHER')
def callback(call: telebot.types.CallbackQuery):
    bot.send_message(call.message.chat.id, 'Write you pair like [EUR/USD]:')
    bot.register_next_step_handler(call.message, other_curr)
    bot.answer_callback_query(call.id)


def other_curr(message: telebot.types.Message):
    try:
        base_curr, quote_curr = message.text.split('/')
        result = currency.convert(amount, base_curr, quote_curr)
        bot.send_message(
            message.chat.id,
            f"Result is: {round(result, 2)} {quote_curr}.\n"
            f"You can give me another amount for {base_curr}/{quote_curr}"
        )
    except Exception:
        bot.send_message(
            message.chat.id,
            f"Error. Next time try to do all correct"
        )


bot.polling(none_stop=True)
