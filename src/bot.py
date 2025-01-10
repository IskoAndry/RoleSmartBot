import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties

from config import TELEGRAM_BOT_TOKEN
from handlers.start import register_start_handlers
from handlers.error_handlers import register_error_handlers

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    """
    Основная функция запуска бота.
    """
    # Создаем HTTP-сессию для бота
    session = AiohttpSession()

    # Создаем объект бота с указанием `default` параметров
    bot = Bot(
        token=TELEGRAM_BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Создаем диспетчер с хранилищем
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрируем обработчики
    register_start_handlers(dp)
    register_error_handlers(dp)

    logger.info("Бот запущен...")

    try:
        # Запускаем бота
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        # Закрываем HTTP-сессию
        await bot.session.close()
        logger.info("Бот остановлен")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен вручную")
