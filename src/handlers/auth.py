from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from database import SessionLocal
from db_config import SessionLocal

router = Router()

# Шаги для регистрации
REGISTER_STEP_NAME = "register_name"
REGISTER_STEP_PHONE = "register_phone"
REGISTER_STEP_PASSWORD = "register_password"

# Хранилище для временных данных регистрации
user_data = {}

# Клавиатура для отмены
cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_keyboard.add(KeyboardButton("Отмена"))

def get_user_by_telegram_id(telegram_id: int) -> User | None:
    with SessionLocal() as db:  # Создаём сессию
        return db.query(User).filter(User.telegram_id == telegram_id).first()
    
    
@router.message(Command("register"))
async def start_registration(message: types.Message):
    """Начало регистрации."""
    user_data[message.from_user.id] = {}
    await message.answer("Введите ваше имя:", reply_markup=cancel_keyboard)


@router.message(lambda msg: msg.from_user.id in user_data and REGISTER_STEP_NAME not in user_data[msg.from_user.id])
async def register_name(message: types.Message):
    """Запрос имени."""
    user_data[message.from_user.id][REGISTER_STEP_NAME] = message.text
    await message.answer("Введите ваш номер телефона (только цифры):", reply_markup=cancel_keyboard)


@router.message(lambda msg: msg.from_user.id in user_data and REGISTER_STEP_PHONE not in user_data[msg.from_user.id])
async def register_phone(message: types.Message):
    """Запрос телефона."""
    if not message.text.isdigit():
        await message.answer("Номер телефона должен содержать только цифры. Попробуйте снова.")
        return

    user_data[message.from_user.id][REGISTER_STEP_PHONE] = message.text
    await message.answer("Введите ваш пароль:", reply_markup=cancel_keyboard)


@router.message(lambda msg: msg.from_user.id in user_data and REGISTER_STEP_PASSWORD not in user_data[msg.from_user.id])
async def register_password(message: types.Message):
    """Сохранение данных и завершение регистрации."""
    db: Session = SessionLocal()
    try:
        user_data[message.from_user.id][REGISTER_STEP_PASSWORD] = message.text

        # Сохраняем пользователя в базе данных
        new_user = User(
            telegram_id=message.from_user.id,
            name=user_data[message.from_user.id][REGISTER_STEP_NAME],
            phone=user_data[message.from_user.id][REGISTER_STEP_PHONE],
            password=user_data[message.from_user.id][REGISTER_STEP_PASSWORD],
            is_admin=False,  # По умолчанию не админ
        )
        db.add(new_user)
        db.commit()

        await message.answer("Вы успешно зарегистрированы!")
    except Exception as e:
        db.rollback()
        await message.answer("Ошибка при регистрации. Попробуйте позже.")
        raise e
    finally:
        db.close()
        user_data.pop(message.from_user.id, None)


@router.message(Command("auth"))
async def start_auth(message: types.Message):
    """Начало авторизации."""
    user_data[message.from_user.id] = {"step": "auth_name"}
    await message.answer("Введите ваше имя:", reply_markup=cancel_keyboard)


@router.message(lambda msg: msg.from_user.id in user_data and user_data[msg.from_user.id]["step"] == "auth_name")
async def auth_name(message: types.Message):
    """Запрос имени для авторизации."""
    user_data[message.from_user.id]["name"] = message.text
    user_data[message.from_user.id]["step"] = "auth_password"
    await message.answer("Введите ваш пароль:", reply_markup=cancel_keyboard)


@router.message(lambda msg: msg.from_user.id in user_data and user_data[msg.from_user.id]["step"] == "auth_password")
async def auth_password(message: types.Message):
    """Проверка имени и пароля."""
    db: Session = SessionLocal()
    try:
        name = user_data[message.from_user.id]["name"]
        password = message.text

        user = db.query(User).filter(User.name == name, User.password == password).first()
        if user:
            role = "администратор" if user.is_admin else "пользователь"
            await message.answer(f"Добро пожаловать, {user.name}! Вы успешно вошли как {role}.")
        else:
            await message.answer("Неверное имя или пароль. Попробуйте снова.")
    finally:
        db.close()
        user_data.pop(message.from_user.id, None)
        

