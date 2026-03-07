from aiohttp import web
from database import save_appointment
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

routes = web.RouteTableDef()

# CORS заголовки для всех ответов
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With',
    'Access-Control-Max-Age': '3600'
}

@routes.options('/api/book')
async def options_handler(request):
    """Обработка CORS preflight запросов - это критически важно!"""
    logger.info("🔵 OPTIONS request received")
    return web.Response(
        status=200,
        headers=CORS_HEADERS
    )

@routes.options('/api/test')
async def options_test_handler(request):
    """OPTIONS для тестового endpoint"""
    return web.Response(status=200, headers=CORS_HEADERS)

@routes.post('/api/book')
async def book_appointment(request):
    """Обработка записи из Mini App"""
    logger.info("🔵 POST request received to /api/book")
    
    try:
        # Логируем заголовки для отладки
        logger.info(f"Headers: {dict(request.headers)}")
        
        # Получаем данные
        data = await request.json()
        logger.info(f"✅ Received booking data: {data}")
        
        user_id = data.get('user_id')
        username = data.get('username', '')
        service = data.get('service')
        date = data.get('date')
        time = data.get('time')
        
        # Валидация
        if not all([user_id, service, date, time]):
            missing = []
            if not user_id: missing.append('user_id')
            if not service: missing.append('service')
            if not date: missing.append('date')
            if not time: missing.append('time')
            
            logger.warning(f"❌ Missing fields: {missing}")
            return web.json_response(
                {'status': 'error', 'message': f'Missing: {missing}'},
                status=400,
                headers=CORS_HEADERS
            )
        
        # Сохраняем в БД
        logger.info(f"💾 Saving to DB: {user_id}, {service}, {date}, {time}")
        success = await save_appointment(
            user_id=user_id,
            username=username,
            service=service,
            date=date,
            time=time
        )
        
        if success:
            logger.info("✅ Appointment saved successfully!")
            return web.json_response(
                {'status': 'success', 'message': 'Запись создана'},
                headers=CORS_HEADERS
            )
        else:
            logger.error("❌ Database save failed")
            return web.json_response(
                {'status': 'error', 'message': 'Database error'},
                status=500,
                headers=CORS_HEADERS
            )
            
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON decode error: {e}")
        return web.json_response(
            {'status': 'error', 'message': 'Invalid JSON'},
            status=400,
            headers=CORS_HEADERS
        )
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}", exc_info=True)
        return web.json_response(
            {'status': 'error', 'message': str(e)},
            status=500,
            headers=CORS_HEADERS
        )

@routes.get('/api/test')
async def test_handler(request):
    """Тестовый endpoint для проверки"""
    logger.info("🔵 GET request to /api/test")
    return web.json_response(
        {
            'status': 'ok', 
            'message': 'API is working',
            'cors': 'enabled'
        },
        headers=CORS_HEADERS
    )

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=8080)
