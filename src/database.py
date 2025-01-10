import psycopg2
from psycopg2.extras import DictCursor
from config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from db_config import Base, engine
from models import user



# Создаём подключение к базе данных
engine = create_engine(DATABASE_URL, echo=True)

# Создаём базовый класс для моделей
Base = declarative_base()

# Создаём фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def setup_database():
    """Инициализация базы данных: создание таблиц, если они не существуют."""
    conn = None
    cur = None
    try:
        # Подключаемся к базе данных
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        Base.metadata.create_all(bind=engine)

        # Создаем таблицу пользователей
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                user_id BIGINT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                balance INTEGER DEFAULT 3,
                subscription BOOLEAN DEFAULT FALSE
            );
            """
        )

        # Создаем таблицу ролей
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS roles (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            );
            """
        )

        # Создаем таблицу администраторов
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS admins (
                id SERIAL PRIMARY KEY,
                user_id BIGINT UNIQUE NOT NULL,
                name TEXT NOT NULL
            );
            """
        )

        # Создаем таблицу платежей
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS payments (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                amount INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            );
            """
        )

        # Создаем таблицу запросов
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS requests (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                role_id INTEGER NOT NULL,
                request_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (role_id) REFERENCES roles (id)
            );
            """
        )

        # Сохраняем изменения
        conn.commit()
        print("База данных успешно настроена!")

    except psycopg2.Error as e:
        print(f"Ошибка при настройке базы данных: {e.pgerror}")
    except UnicodeDecodeError as e:
        print(f"Ошибка кодировки: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
    finally:
        # Закрываем соединение, если оно было успешно открыто
        if cur:
            cur.close()
        if conn:
            conn.close()


# Вызываем функцию настройки базы данных при запуске
if __name__ == "__main__":
    setup_database()
