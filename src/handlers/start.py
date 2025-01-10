from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from keyboards.inline import get_role_keyboard
from handlers.admin_panel import admin_panel_handler

# Создаем роутер для регистрации обработчиков
router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    """Обработчик /start"""
    await message.answer(
        "Привет! Я бот, готовый вам помочь!\n"
        "Используйте /role чтобы выбрать свою роль.\n"
        "Используйте /help чтобы выбрать доступные команды."
    )


@router.message(Command(commands=["role"]))
async def role_command(message: Message):
    """Обработчик /role"""
    await message.answer("Выберите свою роль:", reply_markup=get_role_keyboard())


@router.message(Command(commands=["help"]))
async def help_command(message: Message):
    """Обработчик /help."""
    text = (
        "Добро пожаловать в Telegram-бот!\n"
        "Вот доступные команды:\n"
        "/help - Получить список команд\n"
        "/role - Выбор роли\n"
        "/balance - Проверить баланс\n"
        "/buy - Купить подписку\n"
        "/admin - Панель администратора (для админов)"
    )
    await message.answer(text)


def register_start_handlers(dispatcher):
    """Регистрация обработ команд в диспетчере"""
    dispatcher.include_router(router)
