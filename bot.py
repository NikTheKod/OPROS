import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, WEBAPP_URL
from database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    # Кнопка для открытия Mini App
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📅 Записаться онлайн",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ],
            [
                InlineKeyboardButton(text="💰 Прайс", callback_data="price"),
                InlineKeyboardButton(text="📍 Контакты", callback_data="contacts")
            ]
        ]
    )
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Добро пожаловать в салон красоты NailArt 💅\n"
        "Здесь ты можешь записаться на маникюр, педикюр и другие услуги.\n\n"
        "Нажми кнопку ниже, чтобы выбрать удобное время:",
        reply_markup=keyboard
    )

@dp.callback_query()
async def handle_callbacks(callback: types.CallbackQuery):
    """Обработчик callback кнопок"""
    if callback.data == "price":
        await callback.message.answer(
            "💰 Прайс-лист:\n\n"
            "💅 Маникюр:\n"
            "• Маникюр + покрытие: 1500₽\n"
            "• Маникюр без покрытия: 800₽\n\n"
            "✨ Дизайн:\n"
            "• Дизайн (1 ноготь): от 100₽\n"
            "• Френч/градиент: +300₽\n\n"
            "📏 Наращивание:\n"
            "• Наращивание (типсы): 2000₽\n"
            "• Коррекция: 1500₽"
        )
    elif callback.data == "contacts":
        await callback.message.answer(
            "📍 Наш адрес: ул. Ленина, д. 1\n"
            "🚇 Метро: Центральная (5 мин пешком)\n"
            "📞 Телефон: +7 (999) 123-45-67\n"
            "🕐 Режим работы: ежедневно 10:00-21:00"
        )
    await callback.answer()

async def main():
    """Главная функция запуска бота"""
    try:
        await init_db()
        logger.info("Bot started")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
