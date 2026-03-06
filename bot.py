import asyncio
import logging
import json
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from database import SessionLocal, Appointment
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL')

if not BOT_TOKEN:
    raise ValueError("Нет BOT_TOKEN в переменных окружения!")
if not WEBAPP_URL:
    raise ValueError("Нет WEBAPP_URL в переменных окружения!")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    # Создаем кнопку для открытия Mini App
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="💅 Записаться на маникюр",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )],
            [InlineKeyboardButton(
                text="💰 Прайс-лист",
                web_app=WebAppInfo(url=f"{WEBAPP_URL}?page=prices")
            )]
        ]
    )
    
    await message.answer(
        "🌸 Добро пожаловать в Nail Studio!\n\n"
        "✨ Здесь ты можешь:\n"
        "• Записаться на маникюр и педикюр\n"
        "• Посмотреть прайс-лист\n"
        "• Выбрать удобное время\n\n"
        "👇 Нажми кнопку ниже, чтобы открыть приложение:",
        reply_markup=keyboard
    )

@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    await message.answer(
        "📋 Доступные команды:\n\n"
        "/start - Начать работу\n"
        "/help - Показать эту справку\n"
        "/my_appointments - Мои записи\n"
        "/cancel_booking - Отменить запись\n"
        "/contact - Связаться с мастером"
    )

@dp.message(Command('my_appointments'))
async def cmd_my_appointments(message: types.Message):
    """Показать записи пользователя"""
    db = SessionLocal()
    appointments = db.query(Appointment).filter(
        Appointment.user_id == message.from_user.id,
        Appointment.date >= datetime.now()
    ).order_by(Appointment.date).all()
    db.close()
    
    if not appointments:
        await message.answer("📭 У тебя пока нет активных записей.")
        return
    
    text = "📅 Твои записи:\n\n"
    for i, apt in enumerate(appointments, 1):
        text += f"{i}. {apt.service}\n"
        text += f"   📆 {apt.date.strftime('%d.%m.%Y')}\n"
        text += f"   ⏰ {apt.date.strftime('%H:%M')}\n\n"
    
    await message.answer(text)

@dp.message(Command('contact'))
async def cmd_contact(message: types.Message):
    """Контакты мастера"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📞 Позвонить", callback_data="call")],
            [InlineKeyboardButton(text="💬 Написать в поддержку", url="https://t.me/nail_studio_support")]
        ]
    )
    
    await message.answer(
        "📱 Контакты:\n\n"
        "☎️ Телефон: +7 (999) 123-45-67\n"
        "📍 Адрес: ул. Примерная, д. 123\n"
        "⏰ Работаем: 10:00 - 20:00 ежедневно",
        reply_markup=keyboard
    )

@dp.message()
async def handle_webapp_data(message: types.Message):
    """Обработка данных из Mini App"""
    if not message.web_app_data:
        await message.answer("Используй /start для начала работы")
        return
    
    try:
        # Получаем данные из Mini App
        data = json.loads(message.web_app_data.data)
        logger.info(f"Получены данные: {data}")
        
        # Проверяем обязательные поля
        required_fields = ['name', 'phone', 'service', 'date', 'time']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Отсутствует поле {field}")
        
        # Объединяем дату и время
        datetime_str = f"{data['date']} {data['time']}"
        appointment_date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        
        # Сохраняем в базу данных
        db = SessionLocal()
        
        new_appointment = Appointment(
            user_id=message.from_user.id,
            username=message.from_user.username,
            name=data['name'],
            phone=data['phone'],
            service=data['service'],
            date=appointment_date
        )
        
        db.add(new_appointment)
        db.commit()
        
        # Получаем ID записи
        appointment_id = new_appointment.id
        db.close()
        
        # Отправляем подтверждение
        await message.answer(
            f"✅ Запись подтверждена!\n\n"
            f"💅 Услуга: {data['service']}\n"
            f"📅 Дата: {data['date']}\n"
            f"⏰ Время: {data['time']}\n"
            f"👤 Имя: {data['name']}\n"
            f"📞 Телефон: {data['phone']}\n\n"
            f"🔔 Номер записи: #{appointment_id}\n\n"
            f"Мы напомним тебе за час до визита!\n"
            f"Если хочешь отменить запись, используй /cancel_booking"
        )
        
    except json.JSONDecodeError:
        await message.answer("❌ Ошибка при обработке данных. Пожалуйста, попробуй снова.")
    except ValueError as e:
        await message.answer(f"❌ Ошибка в данных: {str(e)}")
    except Exception as e:
        logger.error(f"Ошибка сохранения записи: {e}")
        await message.answer("❌ Произошла ошибка при сохранении записи. Попробуй позже.")

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    """Обработка нажатий на кнопки"""
    if callback.data == "call":
        await callback.message.answer("📞 Звони: +7 (999) 123-45-67")
    await callback.answer()

async def main():
    """Запуск бота"""
    logger.info("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
