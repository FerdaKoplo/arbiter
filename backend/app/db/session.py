from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.lib.get_env import get_env_variable
from dotenv import load_dotenv

# from dotenv import load_dotenv
# import os
#
load_dotenv()
#
#
# def get_env_variable(name):
#     try:
#         return os.environ[name]
#     except KeyError:
#         raise EnvironmentError(f"Gagal memuat variabel lingkungan wajib: {name}")


DATABASE_URL = get_env_variable("DATABASE_URL")
engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
