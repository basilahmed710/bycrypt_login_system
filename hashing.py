import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a plaintext password securely using bcrypt.

    Args:
        password (str): The raw password provided by the user.

    Returns:
        str: A bcrypt hash (UTF-8 decoded) that can be safely stored in the database.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    # Convert input to bytes
    password_bytes = password.encode("utf-8")

    # Generate a random salt and hash the password
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)

    # bcrypt outputs bytes → convert to string for DB storage
    return hashed_bytes.decode("utf-8")


def validate_password(password: str, stored_hash: str) -> bool:
    """
    Validate a plaintext password against a stored bcrypt hash.

    Args:
        password (str): The user-provided plaintext password.
        stored_hash (str): The bcrypt hashed password from the database.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    if not isinstance(password, str) or not isinstance(stored_hash, str):
        raise TypeError("Both password and stored_hash must be strings.")

    # Convert to bytes for bcrypt comparison
    password_bytes = password.encode("utf-8")
    hash_bytes = stored_hash.encode("utf-8")

    # Compare password with stored hash securely
    return bcrypt.checkpw(password_bytes, hash_bytes)
