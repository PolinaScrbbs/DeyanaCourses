# dotenv - библиотека для получения данных из виртуального окружения
from dotenv import load_dotenv
import os

os.environ.pop("DB_USER", None)
os.environ.pop("DB_PASSWORD", None)
os.environ.pop("DB_NAME", None)

os.environ.pop("SECRET_KEY", None)

# Загружаем данные
load_dotenv()

# Создаём перменные для дальнейшего использования
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@localhost:5432/{DB_NAME}"
SECRET_KEY = os.getenv("SECRET_KEY")
