from aiohttp import web
import psycopg
from config import DATABASE_URL
import json
import logging

routes = web.RouteTableDef()

@routes.get('/')
async def get_index(request):
    try:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return web.Response(text=html_content, content_type='text/html')
    except FileNotFoundError:
        return web.Response(text="Template not found", status=404)

@routes.post('/api/book')
async def book_appointment(request):
    try:
        data = await request.json()
        user_id = data.get('user_id')
        username = data.get('username')
        service = data.get('service')
        date = data.get('date')
        time = data.get('time')

        # Подключаемся к БД
        conn = await psycopg.AsyncConnection.connect(DATABASE_URL)
        
        # Вставляем запись
        await conn.execute(
            'INSERT INTO appointments (user_id, username, service, date, time) VALUES ($1, $2, $3, $4, $5)',
            [user_id, username, service, date, time]
        )
        
        await conn.commit()
        await conn.close()

        return web.json_response({'status': 'success'})
    except Exception as e:
        logging.error(f"Error: {e}")
        return web.json_response({'status': 'error', 'message': str(e)}, status=500)

app = web.Application()
app.add_routes(routes)
