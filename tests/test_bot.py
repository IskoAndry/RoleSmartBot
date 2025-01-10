import psycopg2

host = "127.0.0.1"
user = "postgres"
password = "rutrut"
db_name = "dbrolebot"

# Подключение к базе данных
try:
    connection = psycopg2.connect(
        database=db_name, user=user, password=password, host=host
    )
    # psycopg2.connect("postgresql://username:rutrut@127.0.0.1/dbrolebot")
    cursor = connection.cursor()

    # Выполнение запроса (пример)
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print("Вы подключены к - ", db_version)

except Exception as error:
    print("Ошибка при подключении к базе данных:", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
