import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join("database", "sample.db")

def execute_query(sql: str) -> tuple[pd.DataFrame | None, str]:
    """
    Executes SQL and returns (DataFrame, error_message).
    On success, error_message is empty string.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df, ""
    except Exception as e:
        return None, str(e)