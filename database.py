from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# База данных (берем URL из переменных окружения)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///nail_bot.db')

# Для PostgreSQL на Render нужно заменить postgres:// на postgresql://
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Appointment(Base):
    __tablename__ = 'appointments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String, nullable=True)
    name = Column(String, nullable=False)          # Имя клиента
    phone = Column(String, nullable=False)         # Телефон
    service = Column(String, nullable=False)       # Услуга
    date = Column(DateTime, nullable=False)        # Дата и время записи
    notified_1h = Column(Boolean, default=False)   # Отправили ли уведомление
    created_at = Column(DateTime, default=datetime.now)

# Создаем таблицы
Base.metadata.create_all(bind=engine)
