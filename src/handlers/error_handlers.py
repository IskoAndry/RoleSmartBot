from aiogram import Router, Dispatcher
from aiogram import types
from aiogram.exceptions import TelegramAPIError

router = Router()


@router.errors()
async def handle_telegram_api_error(update: types.Update, exception: TelegramAPIError):
    if update.message:
        await update.message.reply(
            "Произошла ошибка при взаимодействии с Telegram API. Пожалуйста, попробуйте позже."
        )
    print(f"Telegram API Error: {exception}")


@router.errors()
async def handle_general_error(update: types.Update, exception: Exception):
    if update.message:
        await update.message.reply("Произошла ошибка. Пожалуйста, попробуйте позже.")
    print(f"General Error: {exception}")


def register_error_handlers(dp: Dispatcher):
    dp.include_router(router)
