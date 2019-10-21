import sqlite3


def _get_db_connection():
    from ..settings import DB_PATH
    return sqlite3.connect(DB_PATH)
