import os
import psycopg2  # type: ignore
from dotenv import load_dotenv  # type: ignore

load_dotenv()


def get_connection():
    """Open and return a PostgreSQL database connection using .env credentials."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        return conn
    except Exception as e:
        raise ConnectionError(f"Could not connect to the database: {e}")


def test_connection():
    """Quick check to verify the database connection is working."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"Connected to PostgreSQL: {version[0]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")


if __name__ == "__main__":
    test_connection()
