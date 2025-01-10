from aiogram import Router, types
from aiogram import Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Command

# from services.subscription_service import purchase_subscription
from config import DATABASE_URL
import psycopg2
from payment_servise import handle_payment


router = Router()


@router.message(Command("buy"))
async def handle_subscription(user_id: int):
    """func"""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(
        """
    UPDATE users
    SET subscription = TRUE
    WHERE user_id = %s;
    """,
        (user_id,),
    )

    conn.commit()
    cur.close()
    conn.close()


async def purchase_subscription(call: types.CallbackQuery):
    """func"""
    user_id = call.from_user.id

    # Simulate payment
    await handle_payment(user_id, 10)
    await handle_subscription(user_id)

    await call.message.answer("✅ Subscription purchased successfully!")


def get_payment_keyboard():
    """func # Inline keyboard example"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Pay Now", callback_data="pay"))
    return keyboard


async def subscription_handler(message: types.Message):
    """func # Integration example in a handler"""
    await message.answer(
        "Please choose a payment option:", reply_markup=get_payment_keyboard()
    )


def register_payment_handlers(dp: Dispatcher):
    """func"""
    dp.register_callback_query_handler(purchase_subscription, text="pay")


def register_subscription_handlers(dp: Dispatcher):
    """Обработчик /buy"""
    dp.register_message_handler(subscription_handler, Command("buy"))
