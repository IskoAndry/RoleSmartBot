from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Инлайн-клавиатура для выбора роли
async def role_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Аналитик", callback_data="role_analyst"))
    keyboard.add(InlineKeyboardButton("Писатель", callback_data="role_writer"))
    keyboard.add(InlineKeyboardButton("Консультант", callback_data="role_consultant"))
    await message.reply("Выберите свою роль:", reply_markup=keyboard)


# Регистрация обработчиков
def register_role_handlers(dp: Dispatcher):
    dp.register_message_handler(role_handler, commands=["role"])
