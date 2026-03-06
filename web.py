from aiohttp import web
import os
import json
from datetime import datetime

async def serve_index(request):
    """Главная страница Mini App"""
    return web.FileResponse('./templates/index.html')

async def serve_prices(request):
    """Страница с прайсом"""
    return web.FileResponse('./templates/index.html')  # Одна и та же страница

async def get_prices(request):
    """API для получения прайс-листа"""
    prices = {
        'services': [
            {'name': 'Маникюр + покрытие', 'price': 1500, 'duration': 90},
            {'name': 'Наращивание ногтей', 'price': 2500, 'duration': 120},
            {'name': 'Дизайн ногтей (1 ноготь)', 'price': 500, 'duration': 30},
            {'name': 'Снятие лака', 'price': 300, 'duration': 15},
            {'name': 'Педикюр', 'price': 2000, 'duration': 90},
            {'name': 'Ремонт ногтя', 'price': 200, 'duration': 15}
        ]
    }
    return web.json_response(prices)

async def book_appointment(request):
    """API для записи (для теста без Telegram)"""
    try:
        data = await request.json()
        # В реальности данные уходят через Telegram Web App
        return web.json_response({
            'status': 'success',
            'message': 'Запись получена!',
            'data': data
        })
    except Exception as e:
        return web.json_response({
            'status': 'error',
            'message': str(e)
        }, status=400)

def setup_web_app():
    """Настройка веб-приложения"""
    app = web.Application()
    app.router.add_get('/', serve_index)
    app.router.add_get('/prices', serve_prices)
    app.router.add_get('/api/prices', get_prices)
    app.router.add_post('/api/book', book_appointment)
    return app
