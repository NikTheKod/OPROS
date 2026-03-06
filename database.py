import psycopg
from psycopg.rows import dict_row
from config import DATABASE_URL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    """Инициализация базы данных - создание таблиц"""
    try:
        conn = await psycopg.AsyncConnection.connect(DATABASE_URL)
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                username VARCHAR(255),
                service VARCHAR(255),
                date DATE,
                time TIME,
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        await conn.commit()
        await conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise

async def get_connection():
    """Получить соединение с БД"""
    return await psycopg.AsyncConnection.connect(DATABASE_URL)

async def save_appointment(user_id, username, service, date, time):
    """Сохранить запись в БД"""
    conn = None
    try:
        conn = await psycopg.AsyncConnection.connect(DATABASE_URL)
        await conn.execute(
            'INSERT INTO appointments (user_id, username, service, date, time) VALUES (%s, %s, %s, %s, %s)',
            [user_id, username, service, date, time]
        )
        await conn.commit()
        logger.info(f"Appointment saved for user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error saving appointment: {e}")
        return False
    finally:
        if conn:
            await conn.close()
