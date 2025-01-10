# import psycopg2
# from aiogram import Bot, Dispatcher, types
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# import asyncio
# import logging
# from config import TELEGRAM_BOT_TOKEN

# # Database configuration
# DB_CONFIG = {
#     "host": "127.0.0.1",
#     "user": "postgres",
#     "password": "rutrut",
#     "db_name": "dbrolebot",
# }

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Initialize bot and dispatcher
# bot = Bot(token=TELEGRAM_BOT_TOKEN)
# dp = Dispatcher()


# def setup_database():
#     """Initialize database tables"""
#     try:
#         connection = psycopg2.connect(
#             database=DB_CONFIG["db_name"],
#             user=DB_CONFIG["user"],
#             password=DB_CONFIG["password"],
#             host=DB_CONFIG["host"],
#         )
#         cursor = connection.cursor()

#         # Create roles table if not exists
#         cursor.execute(
#             """
#             CREATE TABLE IF NOT EXISTS roles (
#                 id SERIAL PRIMARY KEY,
#                 name VARCHAR(50) UNIQUE NOT NULL,
#                 description TEXT
#             );
#         """
#         )

#         # Create user_roles table if not exists
#         cursor.execute(
#             """
#             CREATE TABLE IF NOT EXISTS user_roles (
#                 user_id BIGINT,
#                 role_id INTEGER REFERENCES roles(id),
#                 assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 PRIMARY KEY (user_id, role_id)
#             );
#         """
#         )

#         # Insert default roles if they don't exist
#         default_roles = [
#             ("analyst", "Data analysis and reporting"),
#             ("writer", "Content creation and editing"),
#             ("consultant", "Business consulting and advisory"),
#         ]

#         for role, description in default_roles:
#             cursor.execute(
#                 """
#                 INSERT INTO roles (name, description)
#                 VALUES (%s, %s)
#                 ON CONFLICT (name) DO NOTHING;
#             """,
#                 (role, description),
#             )

#         connection.commit()
#         logger.info("Database setup completed successfully")

#     except Exception as error:
#         logger.error(f"Error setting up database: {error}")
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()


# def get_role_keyboard():
#     """Create inline keyboard for role selection"""
#     keyboard = InlineKeyboardMarkup(row_width=1)
#     keyboard.add(
#         InlineKeyboardButton("Аналитик 📊", callback_data="role_analyst"),
#         InlineKeyboardButton("Писатель ✍️", callback_data="role_writer"),
#         InlineKeyboardButton("Консультант 💼", callback_data="role_consultant"),
#     )
#     return keyboard


# @dp.message(commands=["role"])
# async def role_command(message: types.Message):
#     """Handle /role command"""
#     await message.reply("Выберите свою роль:", reply_markup=get_role_keyboard())


# @dp.callback_query(lambda c: c.data.startswith("role_"))
# async def process_role_selection(callback_query: types.CallbackQuery):
#     """Handle role selection callback"""
#     try:
#         user_id = callback_query.from_user.id
#         role_name = callback_query.data.split("_")[1]

#         connection = psycopg2.connect(**DB_CONFIG)
#         cursor = connection.cursor()

#         # Get role ID
#         cursor.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
#         role_id = cursor.fetchone()

#         if role_id:
#             # Assign role to user
#             cursor.execute(
#                 """
#                 INSERT INTO user_roles (user_id, role_id)
#                 VALUES (%s, %s)
#                 ON CONFLICT (user_id, role_id) DO NOTHING
#             """,
#                 (user_id, role_id[0]),
#             )

#             connection.commit()

#             role_names = {
#                 "analyst": "Аналитик 📊",
#                 "writer": "Писатель ✍️",
#                 "consultant": "Консультант 💼",
#             }

#             await callback_query.message.edit_text(
#                 f"✅ Вы успешно выбрали роль: {role_names.get(role_name, role_name)}"
#             )

#     except Exception as error:
#         logger.error(f"Error processing role selection: {error}")
#         await callback_query.message.edit_text("❌ Произошла ошибка при выборе роли")
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()


# async def main():
#     """Main function to run the bot"""
#     # Setup database
#     setup_database()

#     # Start polling
#     try:
#         logger.info("Bot started")
#         await dp.start_polling(bot)
#     finally:
#         await bot.session.close()


# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except (KeyboardInterrupt, SystemExit):
#         logger.info("Bot stopped")
