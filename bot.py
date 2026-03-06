import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, WEBAPP_URL
from database import init_db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    # Кнопка для открытия Mini App
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Записаться онлайн",
                    web_app=WebAppInfo(url=WEBAPP_URL)  # Ссылка на наше Mini App
                )
            ],
            [
                InlineKeyboardButton(text="Прайс", callback_data="price"),
                InlineKeyboardButton(text="Контакты", callback_data="contacts")
            ]
        ]
    )
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Добро пожаловать в салон красоты NailArt.\n"
        "Нажми кнопку ниже, чтобы записаться через приложение:",
        reply_markup=keyboard
    )

@dp.callback_query()
async def handle_callbacks(callback: types.CallbackQuery):
    if callback.data == "price":
        await callback.message.answer(
            "💰 Прайс-лист:\n"
            "- Маникюр + покрытие: 1500 руб.\n"
            "- Наращивание: 2000 руб.\n"
            "- Дизайн (1 ноготь): от 100 руб."
        )
    elif callback.data == "contacts":
        await callback.message.answer(
            "📍 Наш адрес: ул. Ленина, д. 1\n"
            "📞 Телефон: +7 (999) 123-45-67"
        )
    await callback.answer()

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
