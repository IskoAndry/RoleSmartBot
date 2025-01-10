from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Инлайн-клавиатура для ролей
def get_role_keyboard():
    """func"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("Аналитик", callback_data="role_analyst"),
        InlineKeyboardButton("Писатель", callback_data="role_writer"),
        InlineKeyboardButton("Консультант", callback_data="role_consultant")
    )
    return keyboard
