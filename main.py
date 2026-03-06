import asyncio
import logging
from bot import main as bot_main
from web_app import app
from aiohttp import web

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_web():
    """Запуск веб-сервера"""
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    logger.info("Web server started on port 8080")
    
    # Держим сервер запущенным
    await asyncio.Event().wait()

async def main():
    """Запуск бота и веб-сервера параллельно"""
    try:
        await asyncio.gather(
            bot_main(),
            run_web()
        )
    except Exception as e:
        logger.error(f"Main error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
