from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import psycopg2
from psycopg2.extras import DictCursor
from config import DATABASE_URL
import os



# Database setup
def setup_database():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

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

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS roles (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        description TEXT
    );
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS admins (
        id SERIAL PRIMARY KEY,
        user_id BIGINT UNIQUE NOT NULL,
        name TEXT NOT NULL
    );
    """
    )

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

    conn.commit()
    cur.close()
    conn.close()


setup_database()


