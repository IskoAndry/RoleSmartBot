from aiogram import Bot, Dispatcher, executor
from config import TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# Регистрация обработчиков
from handlers.start import register_start_handlers

register_start_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
