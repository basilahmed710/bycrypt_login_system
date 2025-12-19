import sqlite3
from sqlite3 import Connection
from typing import Optional, List, Tuple


def add_user(conn: Connection, username: str, password_hash: str) -> None:
    """
    Insert a new user into the database.

    Args:
        conn (Connection): SQLite database connection.
        username (str): Username to add.
        password_hash (str): Hashed password.

    Raises:
        RuntimeError: If insertion fails.
    """
    try:
        cur = conn.cursor()
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        cur.execute(sql, (username, password_hash))
        conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to add user '{username}': {e}")


def migrate_users(conn: Connection, filepath: str = "DATA/user.txt") -> None:
    """
    Load users from a text file and insert them into the database.

    Expected file format (one per line):
        username,password_hash

    Args:
        conn (Connection): SQLite DB connection.
        filepath (str): Path to user seed file.

    Raises:
        RuntimeError: If migration fails.
    """
    try:
        with open(filepath, "r") as f:
            users = f.readlines()

        for line in users:
            line = line.strip()
            if not line:
                continue

            try:
                username, password_hash = line.split(",")
            except ValueError:
                raise RuntimeError(f"Invalid user entry in file: '{line}'")

            add_user(conn, username.strip(), password_hash.strip())

    except FileNotFoundError:
        raise RuntimeError(f"User seed file not found: {filepath}")


def get_all_users(conn: Connection) -> List[Tuple]:
    """
    Retrieve all users from the database.

    Args:
        conn (Connection): SQLite DB connection.

    Returns:
        List[Tuple]: A list of rows representing users.

    Raises:
        RuntimeError: If the query fails.
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        return cur.fetchall()
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to retrieve users: {e}")


def get_user(conn: Connection, username: str) -> Optional[Tuple]:
    """
    Retrieve a single user by username.

    Args:
        conn (Connection): SQLite DB connection.
        username (str): Username to look up.

    Returns:
        Optional[Tuple]: The user row if found, otherwise None.

    Raises:
        RuntimeError: If the query fails.
    """
    try:
        cur = conn.cursor()
        sql = "SELECT * FROM users WHERE username = ?"
        cur.execute(sql, (username,))
        return cur.fetchone()
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to retrieve user '{username}': {e}")


def update_user(conn: Connection, old_username: str, new_username: str) -> None:
    """
    Update an existing user's username.

    Args:
        conn (Connection): SQLite DB connection.
        old_username (str): Current username.
        new_username (str): Updated username.

    Raises:
        RuntimeError: If update fails.
    """
    try:
        cur = conn.cursor()
        sql = "UPDATE users SET username = ? WHERE username = ?"
        cur.execute(sql, (new_username, old_username))
        conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to update username from '{old_username}' to '{new_username}': {e}")


def delete_user(conn: Connection, username: str) -> None:
    """
    Delete a user by username.

    Args:
        conn (Connection): SQLite DB connection.
        username (str): Username to delete.

    Raises:
        RuntimeError: If deletion fails.
    """
    try:
        cur = conn.cursor()
        sql = "DELETE FROM users WHERE username = ?"
        cur.execute(sql, (username,))
        conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to delete user '{username}': {e}")
