import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def migrate_datasets_metadata(conn: Engine, csv_path: str = "DATA/datasets_metadata.csv") -> None:
    """
    Load dataset metadata from a CSV file and migrate it into the database.

    Args:
        conn (Engine): SQLAlchemy database engine/connection.
        csv_path (str): Path to the datasets metadata CSV file.

    Raises:
        FileNotFoundError: If the CSV file cannot be found.
        RuntimeError: If writing to the database fails.
    """
    # Read metadata CSV into a DataFrame
    data = pd.read_csv(csv_path)

    try:
        data.to_sql(
            "datasets_metadata",
            conn,
            if_exists="replace",   # Replace table on every migration (safe for dev)
            index=False            # Prevent pandas index from being saved as a column
        )
    except SQLAlchemyError as e:
        raise RuntimeError(f"Failed to migrate datasets metadata: {e}")


def get_all_datasets_metadata(conn: Engine) -> pd.DataFrame:
    """
    Retrieve all dataset metadata records from the database.

    Args:
        conn (Engine): SQLAlchemy engine or connection.

    Returns:
        pd.DataFrame: All metadata records as a DataFrame.

    Raises:
        RuntimeError: If the query fails.
    """
    sql = "SELECT * FROM datasets_metadata"

    try:
        return pd.read_sql(sql, conn)
    except SQLAlchemyError as e:
        raise RuntimeError(f"Failed to retrieve datasets metadata: {e}")
