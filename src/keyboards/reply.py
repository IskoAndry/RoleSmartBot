from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Reply-клавиатура для баланса и подписки
def get_main_menu():
    """func"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Баланс"), KeyboardButton("Подписка"))
    return keyboard
