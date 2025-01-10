import asyncio
import logging
from typing import NoReturn

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramUnauthorizedError

from config import TELEGRAM_BOT_TOKEN
from handlers.start import register_start_handlers
from handlers.admin_panel import register_admin_handlers

# Add more handler imports as needed

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


async def register_all_handlers() -> None:
    """Register all handlers"""
    register_start_handlers(dp)
    register_admin_handlers(dp)
    # Add more handlers registration here


async def start_bot() -> None:
    """Start bot polling"""
    try:
        logger.info("Starting bot...")
        await register_all_handlers()
        await dp.start_polling(bot)
    except TelegramUnauthorizedError:
        logger.critical("Invalid bot token! Please check your configuration.")
        exit(1)
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        exit(1)


async def main() -> NoReturn:
    """Main function"""
    try:
        await start_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped manually")
    finally:
        await bot.session.close()
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
