from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

# Создаем роутер для регистрации обработчиков
router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    """
    Обработчик команды /start.
    """
    await message.answer("Привет! Я бот, готовый вам помочь!")


@router.message(Command(commands=["help"]))
async def help_command(message: Message):
    """
    Обработчик команды /help.
    """
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
    """
    Регистрация обработчиков команд в диспетчере.
    """
    dispatcher.include_router(router)
