import psycopg2
from psycopg2.extras import DictCursor
from config import DATABASE_URL
from aiogram import Bot

bot = Bot(token="YOUR_TELEGRAM_BOT_TOKEN")


async def handle_payment(user_id: int, amount: int):
    """func"""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(
        """
    UPDATE users
    SET balance = balance + %s
    WHERE user_id = %s;
    """,
        (amount, user_id),
    )

    cur.execute(
        """
    INSERT INTO payments (user_id, amount)
    VALUES (%s, %s);
    """,
        (user_id, amount),
    )

    conn.commit()
    cur.close()
    conn.close()


async def notify_low_balance(user_id: int):
    """func"""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    cur = conn.cursor()

    cur.execute(
        """
    SELECT balance FROM users WHERE user_id = %s;
    """,
        (user_id,),
    )

    user = cur.fetchone()

    if user and user["balance"] <= 1:
        await bot.send_message(
            user_id,
            "⚠️ Your balance is low. Please top up to continue using the service.",
        )

    cur.close()
    conn.close()
