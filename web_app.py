from aiohttp import web
from database import save_appointment
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

routes = web.RouteTableDef()

@routes.get('/')
async def get_index(request):
    """Раздаем HTML страницу Mini App"""
    try:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return web.Response(text=html_content, content_type='text/html')
    except FileNotFoundError:
        logger.error("Template file not found")
        return web.Response(text="Template not found", status=404)
    except Exception as e:
        logger.error(f"Error reading template: {e}")
        return web.Response(text="Internal server error", status=500)

@routes.post('/api/book')
async def book_appointment(request):
    """Обработка записи из Mini App"""
    try:
        data = await request.json()
        logger.info(f"Received booking data: {data}")
        
        user_id = data.get('user_id')
        username = data.get('username', '')
        service = data.get('service')
        date = data.get('date')
        time = data.get('time')
        
        # Валидация
        if not all([user_id, service, date, time]):
            return web.json_response({
                'status': 'error', 
                'message': 'Missing required fields'
            }, status=400)
        
        # Сохраняем в БД
        success = await save_appointment(
            user_id=user_id,
            username=username,
            service=service,
            date=date,
            time=time
        )
        
        if success:
            return web.json_response({'status': 'success'})
        else:
            return web.json_response({
                'status': 'error', 
                'message': 'Database error'
            }, status=500)
            
    except json.JSONDecodeError:
        logger.error("Invalid JSON")
        return web.json_response({
            'status': 'error', 
            'message': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return web.json_response({
            'status': 'error', 
            'message': str(e)
        }, status=500)

@routes.get('/health')
async def health_check(request):
    """Health check для Railway"""
    return web.json_response({'status': 'healthy'})

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=8080)
