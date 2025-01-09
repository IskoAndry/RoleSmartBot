import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
PAYMENT_API_KEY = os.getenv("PAYMENT_API_KEY")

host = "127.0.0.1"
user = "postgres"
password = "123"
db_name = "bot_user"

#DATABASE_URL=postgresql://username:password@localhost/dbname