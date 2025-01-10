import os
from dotenv import load_dotenv
from os import getenv

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
PAYMENT_API_KEY = os.getenv("PAYMENT_API_KEY")


# Проверка наличия токена
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Bot token not found! Please set BOT_TOKEN in your .env file")
