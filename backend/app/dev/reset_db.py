from sqlalchemy import text
from app.db.session import engine


def nuke_postgres():
    print("RESETTING POSTGRES DATABASE...")
    with engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")

        connection.execute(text("DROP SCHEMA public CASCADE;"))
        connection.execute(text("CREATE SCHEMA public;"))

        connection.execute(text("GRANT ALL ON SCHEMA public TO public;"))

    print("Database is now empty and clean.")


if __name__ == "__main__":
    nuke_postgres()
