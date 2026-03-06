from aiohttp import web
import asyncpg
from config import DATABASE_URL
import json

routes = web.RouteTableDef()

# Раздаем HTML-страницу Mini App
@routes.get('/')
async def get_index(request):
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    return web.Response(text=html_content, content_type='text/html')

# API для сохранения записи
@routes.post('/api/book')
async def book_appointment(request):
    data = await request.json()
    user_id = data.get('user_id')
    username = data.get('username')
    service = data.get('service')
    date = data.get('date')
    time = data.get('time')

    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute(
        'INSERT INTO appointments (user_id, username, service, date, time) VALUES ($1, $2, $3, $4, $5)',
        user_id, username, service, date, time
    )
    await conn.close()

    return web.json_response({'status': 'success'})

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=8080)
