import sqlite3
from sqlite3 import Connection


DB_PATH = "DATA/intelligence_platform.db"


def get_connection(db_path: str = DB_PATH) -> Connection:
    """
    Create and return a SQLite database connection.

    Args:
        db_path (str): Path to the SQLite database file.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.

    Notes:
        - `check_same_thread=False` allows the connection to be shared across
          Streamlit's multi-threaded environment.
        - The caller is responsible for closing the connection when done.
    """
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to connect to database at '{db_path}': {e}")
