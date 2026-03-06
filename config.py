import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL')  # URL, который выдаст Railway
DATABASE_URL = os.getenv('DATABASE_URL')
