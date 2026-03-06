import asyncio
from bot import main as bot_main
from web_app import app
from aiohttp import web
import logging

async def run_web():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    logging.info("Web server started on port 8080")
    await asyncio.Event().wait()  # держим сервер запущенным

async def main():
    # Запускаем бота и веб-сервер параллельно
    await asyncio.gather(
        bot_main(),
        run_web()
    )

if __name__ == "__main__":
    asyncio.run(main())
