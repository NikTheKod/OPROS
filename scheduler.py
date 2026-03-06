import asyncio
import logging
from datetime import datetime, timedelta
from database import SessionLocal, Appointment
from aiogram import Bot
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)

async def check_and_send_reminders():
    """Проверяет записи и отправляет напоминания за час"""
    db = SessionLocal()
    
    try:
        # Текущее время
        now = datetime.now()
        # Время через час
        reminder_time = now + timedelta(hours=1)
        
        logger.info(f"Проверка записей на {reminder_time.strftime('%d.%m.%Y %H:%M')}")
        
        # Ищем записи через час (±5 минут)
        appointments = db.query(Appointment).filter(
            Appointment.date >= reminder_time - timedelta(minutes=5),
            Appointment.date <= reminder_time + timedelta(minutes=5),
            Appointment.notified_1h == False
        ).all()
        
        if appointments:
            logger.info(f"Найдено {len(appointments)} записей для уведомления")
        
        for apt in appointments:
            try:
                # Отправляем уведомление
                text = (
                    f"⏰ Напоминание о записи!\n\n"
                    f"💅 Через час у тебя:\n"
                    f"• {apt.service}\n"
                    f"📅 {apt.date.strftime('%d.%m.%Y')}\n"
                    f"⏰ {apt.date.strftime('%H:%M')}\n\n"
                    f"🚗 Не опаздывай!\n"
                    f"📍 Адрес: ул. Примерная, д. 123"
                )
                await bot.send_message(apt.user_id, text)
                
                # Отмечаем, что уведомление отправлено
                apt.notified_1h = True
                db.commit()
                
                logger.info(f"✅ Уведомление отправлено пользователю {apt.user_id}")
                
            except Exception as e:
                logger.error(f"❌ Ошибка отправки уведомления для записи {apt.id}: {e}")
                
    except Exception as e:
        logger.error(f"Ошибка в планировщике: {e}")
    finally:
        db.close()

async def main():
    """Основной цикл планировщика"""
    logger.info("🚀 Планировщик уведомлений запущен")
    
    while True:
        try:
            await check_and_send_reminders()
            # Проверяем каждую минуту
            await asyncio.sleep(60)
        except Exception as e:
            logger.error(f"❌ Критическая ошибка: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
