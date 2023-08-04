import os
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, LabeledPrice, ContentType
# from bot_types import ContentType

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.environ['API_TOKEN']
TEST_PORTMONE_CARD = os.environ['TEST_PORTMONE_CARD']
TEST_PORTMONE_TOKEN = os.environ['TEST_PORTMONE_TOKEN']

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)

ONE_USD_PRICE = 38


# @dp.message_handler() <- Ok
@dp.message_handler(commands=['start'], content_types=[ContentType.TEXT])
async def start(message: Message):
    await bot.send_invoice(
        message.chat.id,
        "Buy Image",
        "AI Generated image",
        "invoice",
        TEST_PORTMONE_TOKEN,
        "UAH",
        [LabeledPrice("Buy Image", 199 * ONE_USD_PRICE)]
    )


@dp.message_handler(content_types=[ContentType.SUCCESSFUL_PAYMENT])
async def success(message: Message):
    await message.answer(
        f"Success: {message.successful_payment.order_info}"
    )


executor.start_polling(dp)
