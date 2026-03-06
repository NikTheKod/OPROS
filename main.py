import asyncio
import threading
import logging
from bot import main as bot_main
from web import setup_web_app
from aiohttp import web
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_web():
    """Запуск веб-сервера в отдельном потоке"""
    app = setup_web_app()
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🌐 Веб-сервер запущен на порту {port}")
    web.run_app(app, port=port)

def run_bot():
    """Запуск бота"""
    logger.info("🤖 Telegram бот запускается...")
    asyncio.run(bot_main())

if __name__ == "__main__":
    logger.info("✨ Запуск Nail Studio Bot")
    
    # Запускаем веб-сервер в фоне
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    
    # Запускаем бота (он будет работать в основном потоке)
    run_bot()
