# user.py
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("profile"))
async def profile_handler(message: types.Message):
    """Handle user profile command"""
    user_id = message.from_user.id
    username = message.from_user.username
    await message.answer(
        f"Your Profile:\n"
        f"ID: {user_id}\n"
        f"Username: @{username}"
    )