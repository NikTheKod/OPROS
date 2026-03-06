import asyncpg
from config import DATABASE_URL

async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
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
    await conn.close()
