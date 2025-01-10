from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("admin"))
async def admin_panel_handler(message: Message):
    """Обработчик команды /admin"""
    # Здесь можно добавить проверку на админа
    admin_ids = [4444]  # Замените на реальные ID администраторов

    if message.from_user.id in admin_ids:
        await message.answer("Добро пожаловать в панель администратора!")
    else:
        await message.answer("У вас нет доступа к панели администратора.")


def register_admin_handlers(dp):
    """Регистрация обработчиков админ-панели"""
    dp.include_router(router)
