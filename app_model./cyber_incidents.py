import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def migrate_cyber_incidents(conn: Engine, csv_path: str = "DATA/cyber_incidents.csv") -> None:
    """
    Load cyber incident data from a CSV file and migrate it into the database.

    Args:
        conn (Engine): SQLAlchemy database connection/engine.
        csv_path (str): Path to the source CSV file.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        SQLAlchemyError: If writing to the database fails.
    """
    # Load CSV — this may raise FileNotFoundError, which is desired for clarity
    data = pd.read_csv(csv_path)

    try:
        # Write the DataFrame into a SQL table
        data.to_sql(
            "cyber_incidents",
            conn,
            if_exists="replace",   # avoid duplicate tables during development
            index=False            # do not store pandas default index as column
        )
    except SQLAlchemyError as e:
        raise RuntimeError(f"Failed to migrate cyber incidents: {e}")


def get_all_cyber_incidents(conn: Engine) -> pd.DataFrame:
    """
    Retrieve all cyber incident records from the database.

    Args:
        conn (Engine): SQLAlchemy database connection/engine.

    Returns:
        pd.DataFrame: A DataFrame containing all cyber incident records.

    Raises:
        SQLAlchemyError: If the query fails.
    """
    sql = "SELECT * FROM cyber_incidents"

    try:
        return pd.read_sql(sql, conn)
    except SQLAlchemyError as e:
        raise RuntimeError(f"Failed to retrieve cyber incidents: {e}")
