from datetime import datetime
import sqlite3
from sqlite3 import Connection, Cursor
from types import TracebackType
from pathlib import Path
from bot.utils import days_until_birthday

USERS = """
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    happy_birthday_date date,
    unique(username)
);
"""


class Sqlite:
    def __init__(self, path: str | Path):
        self.path = path
        self.conn: Connection
        self.cursor: Cursor

    def __enter__(self):
        self.conn: Connection = sqlite3.connect(self.path)
        self.cursor: Cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_class: BaseException, exc: BaseException, traceback: TracebackType) -> None:
        self.conn.commit()
        self.conn.close()


class Q:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path: str | Path = db_path

    def create_tables(self) -> None:
        with Sqlite(self.db_path) as cursor:
            cursor.execute(USERS)

    def check_user_happy_birthday_is_exists(self, username: str) -> bool:
        with Sqlite(self.db_path) as cursor:
            cursor.execute("SELECT happy_birthday_date FROM users WHERE username = ?", (username,))
            return True if cursor.fetchone() else False

    def add_user_hb(self, username: str, happy_birthday_date: datetime) -> None:
        with Sqlite(self.db_path) as cursor:
            cursor.execute(
                "INSERT INTO users (username, happy_birthday_date) VALUES (?, ?)",
                (username, happy_birthday_date),
            )

    def get_user_hb(self, username: str) -> tuple[str, int]:
        with Sqlite(self.db_path) as cursor:
            cursor.execute("SELECT happy_birthday_date FROM users WHERE username = ?", (username,))
            return days_until_birthday(cursor.fetchone()[0])

    def update_user_hb(self, username: str, happy_birthday_date: datetime):
        with Sqlite(self.db_path) as cursor:
            cursor.execute(
                "UPDATE users SET happy_birthday_date = ? WHERE username = ?",
                (happy_birthday_date, username),
            )
