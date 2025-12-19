import streamlit as st
from hashing import hash_password, validate_password
from app_model.db import get_connection
from app_model.users import add_user, get_user

# --- Helpers -----------------------------------------------------------------


def is_strong_password(password: str) -> tuple[bool, str]:
    """
    Very basic password strength checker.
    Returns (is_valid, message).
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if password.isdigit() or password.isalpha():
        return False, "Password must contain both letters and numbers."
    return True, ""


# --- App Setup ----------------------------------------------------------------

st.set_page_config(
    page_title="Home Page",
    page_icon="🏠",
    layout="wide"
)

st.title("Welcome to the Main Page")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

# If already logged in, send user to dashboard immediately
if st.session_state["logged_in"]:
    st.s
