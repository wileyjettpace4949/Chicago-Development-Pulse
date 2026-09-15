import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    """Create and return a PostgreSQL database connection."""

    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

if __name__ == "__main__":
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT current_database(), current_user, version();"
            )

            result = cursor.fetchone()

            print(f"Database: {result[0]}")
            print(f"User: {result[1]}")
            print(f"PostgreSQL: {result[2]}")