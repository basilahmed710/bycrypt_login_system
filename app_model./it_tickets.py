import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def migrate_it_tickets(conn: Engine, csv_path: str = "DATA/it_tickets.csv") -> None:
    """
    Load IT ticket data from a CSV file and migrate it into the database.

    Args:
        conn (Engine): SQLAlchemy database connection/engine.
        csv_path (str): Path to the IT tickets CSV file.

    Raises:
        FileNotFoundError: If the CSV file cannot be found.
        RuntimeError: If writing to the database fails.
    """
    # Load data from CSV into a DataFrame
    data = pd.read_csv(csv_path)

    try:
        # Write to the database table
        data.to_sql(
            "it_tickets",
            conn,
            if_exists="replace",   # Prevent duplicates during development
            index=False            # Avoid storing pandas index as a column
        )
    except SQLAlchemyError as e:
        raise RuntimeError(f"Failed to migrate IT tickets: {e}")


def get_all_it_tickets(conn: Engine) -> pd.DataFrame:
    """
    Retrieve all IT ticket records from the database.

    Args:
        conn (Engine): SQLAlchemy engine or connection.

    Returns:
        pd.DataFrame: Full dataset of IT tickets.

    Raises:
        RuntimeError: If the SQL query fails.
    """
    sql = "SELECT * FROM it_tickets"

    try:
        return pd.read_sql(sql, conn)
    except SQLAlchemyError as e:
        raise RuntimeError(f"Failed to retrieve IT tickets: {e}")
