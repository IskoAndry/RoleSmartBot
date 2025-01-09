from aiogram import Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Command
from services.subscription_service import purchase_subscription


def async def handle_subscription(user_id: int):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute('''
    UPDATE users
    SET subscription = TRUE
    WHERE user_id = %s;
    ''', (user_id,))

    conn.commit()
    cur.close()
    conn.close()

async def purchase_subscription(call: types.CallbackQuery):
    user_id = call.from_user.id

    # Simulate payment
    await handle_payment(user_id, 10)
    await handle_subscription(user_id)

    await call.message.answer("✅ Subscription purchased successfully!")

# Inline keyboard example
def get_payment_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Pay Now", callback_data="pay"))
    return keyboard

# Integration example in a handler
async def subscription_handler(message: types.Message):
    await message.answer(
        "Please choose a payment option:",
        reply_markup=get_payment_keyboard()
    )

def register_payment_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(purchase_subscription, text="pay")

def register_subscription_handlers(dp: Dispatcher):
    dp.register_message_handler(subscription_handler, Command("buy"))
