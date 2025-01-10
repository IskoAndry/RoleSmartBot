import logging
from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import psycopg2

import inline
import role_based
from config import DATABASE_URL

router = Router()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def role_handler(message: types.Message):
    """func # Инлайн-клавиатура для выбора роли"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Аналитик", callback_data="role_analyst"))
    keyboard.add(InlineKeyboardButton("Писатель", callback_data="role_writer"))
    keyboard.add(InlineKeyboardButton("Консультант", callback_data="role_consultant"))
    await message.reply("Выберите свою роль:", reply_markup=keyboard)


def register_role_handlers(dp: Dispatcher):
    """func  # Регистрация обработчиков"""
    dp.register_message_handler(role_handler, commands=["role"])


@router.message(Command("role"))
async def role_command(message: Message):
    """Handler for /role command"""
    try:
        await message.answer("Выберите свою роль:", reply_markup=get_role_keyboard())
    except Exception as e:
        logger.error(f"Error in role command: {e}")
        await message.answer("Произошла ошибка при выборе роли. Попробуйте позже.")


@router.callback_query(lambda c: c.data.startswith("role_"))
async def process_role_selection(callback_query: types.CallbackQuery):
    """Handle role selection callback"""
    try:
        user_id = callback_query.from_user.id
        role_name = callback_query.data.split("_")[1]

        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # First, check if role exists
        cur.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
        role_id = cur.fetchone()

        if role_id:
            # Update or insert user role
            cur.execute(
                """
                INSERT INTO user_roles (user_id, role_id)
                VALUES (%s, %s)
                ON CONFLICT (user_id) DO UPDATE 
                SET role_id = EXCLUDED.role_id
            """,
                (user_id, role_id[0]),
            )

            conn.commit()

            role_names = {
                "analyst": "Аналитик 📊",
                "writer": "Писатель ✍️",
                "consultant": "Консультант 💼",
            }

            await callback_query.message.edit_text(
                f"✅ Вы успешно выбрали роль: {role_names.get(role_name, role_name)}\n"
                f"Используйте /help для просмотра доступных команд."
            )
        else:
            await callback_query.message.edit_text("❌ Выбранная роль не существует")

    except Exception as e:
        logger.error(f"Error processing role selection: {e}")
        await callback_query.message.edit_text("❌ Произошла ошибка при выборе роли")
    finally:
        if "conn" in locals():
            cur.close()
            conn.close()


async def main():
    """Main function to run the bot"""
    try:
        # Setup database connection
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Create necessary tables if they don't exist
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS roles (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL,
                description TEXT
            );
            
            CREATE TABLE IF NOT EXISTS user_roles (
                user_id BIGINT PRIMARY KEY,
                role_id INTEGER REFERENCES roles(id),
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )

        # Insert default roles
        default_roles = [
            ("analyst", "Аналитик данных"),
            ("writer", "Писатель контента"),
            ("consultant", "Бизнес консультант"),
        ]

        for role, description in default_roles:
            cur.execute(
                """
                INSERT INTO roles (name, description)
                VALUES (%s, %s)
                ON CONFLICT (name) DO NOTHING
            """,
                (role, description),
            )

        conn.commit()
        logger.info("Database initialized successfully")

    except Exception as e:
        logger.error(f"Database initialization error: {e}")
    finally:
        if "conn" in locals():
            cur.close()
            conn.close()
