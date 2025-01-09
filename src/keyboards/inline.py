from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Инлайн-клавиатура для ролей
def get_role_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Аналитик", callback_data="role_analyst"))
    keyboard.add(InlineKeyboardButton("Писатель", callback_data="role_writer"))
    keyboard.add(InlineKeyboardButton("Консультант", callback_data="role_consultant"))
    return keyboard
