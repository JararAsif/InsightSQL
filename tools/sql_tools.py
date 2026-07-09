import os
from langchain_community.utilities import SQLDatabase

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'company.db')

def get_db() -> SQLDatabase:
    """Initializes and returns the LangChain SQLDatabase wrapper."""
    return SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

def get_schema() -> str:
    """
    Returns the database schema
    """
    db = get_db()
    return db.get_table_info()

def execute_query(query: str) -> str:
    """
    Executes a raw SQL query against the database and returns the result as a string.
    """
    db = get_db()
    try:
        return db.run(query)
    except Exception as e:
        return f"Error executing query: {str(e)}"
