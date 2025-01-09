from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Команда /start
async def start_handler(message: types.Message):
    text = (
        "Добро пожаловать в Telegram-бот!\n"
        "Вот доступные команды:\n"
        "/help - Получить список команд\n"
        "/role - Выбор роли\n"
        "/balance - Проверить баланс\n"
        "/buy - Купить подписку\n"
        "/admin - Панель администратора (для админов)"
    )
    await message.reply(text)


# Команда /help
async def help_handler(message: types.Message):
    text = (
        "Список доступных команд:\n"
        "/start - Начало работы с ботом\n"
        "/help - Список команд\n"
        "/role - Выбор роли\n"
        "/balance - Проверить баланс\n"
        "/buy - Купить подписку\n"
        "/admin - Панель администратора (для админов)"
    )
    await message.reply(text)


# Регистрация обработчиков
def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(help_handler, commands=["help"])
