from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy.orm import Session
from models.user import User
from database import SessionLocal

# Клавиатура для выбора роли
role_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
role_keyboard.add(KeyboardButton("Пользователь"), KeyboardButton("Администратор"))


# Регистрация
async def register_handler(message: types.Message):
    await message.reply("Выберите роль для регистрации:", reply_markup=role_keyboard)


# Аутентификация
async def auth_handler(message: types.Message):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    if user:
        role = "администратор" if user.is_admin else "пользователь"
        await message.reply(f"Вы успешно аутентифицированы как {role}.")
    else:
        await message.reply(
            "Вы не зарегистрированы. Используйте /register для регистрации."
        )


# Регистрация обработчиков
def register_auth_handlers(dp: Dispatcher):
    dp.register_message_handler(register_handler, commands=["register"])
    dp.register_message_handler(auth_handler, commands=["auth"])
