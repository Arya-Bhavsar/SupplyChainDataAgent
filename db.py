from pathlib import Path
import sqlite3
import re

from langchain_core.tools import tool

DB_PATH = Path(__file__).parent / "chinook.db"

@tool
def get_schema() -> str:
    """
    Fetches the entire database schema, including table names, and their respective columns and their details.
    """
    try:
        conn = sqlite3.connect(f"file:{DB_PATH.resolve()}?mode=ro", uri=True)
        cursor = conn.cursor()

        # Get the table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [row[0] for row in cursor.fetchall()]

        # Get all the columns for all the tables
        schema = []
        for table in tables:
            # PRAGMA table_info returns table structure: (cid, name, type, notnull, dflt_value, pk)
            cursor.execute(f"PRAGMA table_info('{table}');")
            columns = cursor.fetchall()
            # Gets column name and type
            col_info = [f"{col[1]} {col[2]}" for col in columns]
            schema.append(f"Table: {table}\nColumns: {", ".join(col_info)}")

        return "\n\n".join(schema)
    except sqlite3.Error as e:
        return f"Error retrieving database schema: {str(e)}"
    finally:
        conn.close()

@tool
def run_query(query: str) -> str:
    """
    Executes a SQL query against the SQLite database.
    Returns string formatted query results for SELECT statements, or execution metadata for non-SELECT statements.
    """
    query = query.strip()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        # If the query yielded rows (SELECT statement)
        if cursor.description:
            col_names = [desc[0] for desc in cursor.description]
            formatted_results = [dict(zip(col_names, row)) for row in rows]
            return str(formatted_results)

        # Non-SELECT operations (INSERT, UPDATE, DELETE)
        conn.commit()
        return (
            f"Query executed successfully. "
            f"Rows affected: {cursor.rowcount}. "
            f"Last inserted row ID: {cursor.lastrowid if cursor.lastrowid else 'N/A'}."
        )
    except sqlite3.Error as e:
        conn.rollback()
        return f"SQLite Execution Error: {str(e)}"
    finally:
        conn.close()