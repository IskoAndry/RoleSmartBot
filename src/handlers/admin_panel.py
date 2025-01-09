from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.orm import Session
from models.user import User
from database import SessionLocal


# Панель администратора
async def admin_panel_handler(message: types.Message):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    if user and user.is_admin:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(
                "Управление пользователями", callback_data="manage_users"
            )
        )
        keyboard.add(InlineKeyboardButton("Статистика", callback_data="statistics"))
        await message.reply(
            "Добро пожаловать в панель администратора.", reply_markup=keyboard
        )
    else:
        await message.reply("У вас нет прав администратора.")


# Регистрация обработчиков
def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_panel_handler, commands=["admin"])
