import sqlite3
from typing import List, Dict, Any
import os
import pathlib
import logging
from utils.logger_utils import CustomLogger


class DatabaseManager:
    def __init__(
        self,
        db_path: str = None,
        logger: CustomLogger = None,
    ):
        self.db_path = db_path or os.getenv("DB_PATH", "data/database.db")
        self.logger = logger or CustomLogger(name="database", log_level=logging.DEBUG)
        self._initialize_database()

    def _get_db_connection(self) -> sqlite3.Connection:
        """Establish and return a database connection."""
        return sqlite3.connect(self.db_path)

    def _execute_query(
        self, query: str, params: List[Any] = [], commit: bool = False
    ) -> List[tuple]:
        """Execute a query (INSERT, SELECT, UPDATE, etc.)."""
        self.logger.info(f" > Query: {query}")
        self.logger.info(f" > Params: {params}")
        self.logger.info(f" > Commit: {commit}")
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                if commit:
                    conn.commit()
                result = cursor.fetchall()
                self.logger.info(f" > Result: {result}")
                return result
        except Exception as e:
            self.logger.error(e)
            return []

    def _initialize_database(self):
        """Ensure the database is set up (tables created) when the program starts."""
        # Create the database file if it doesn't exist
        if not os.path.exists(self.db_path):
            pathlib.Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            open(self.db_path, "a").close()
        self.logger.info("Checking if tables exist. Creating if not.")

    def create_table_if_not_exists(self, table_name: str, columns: List[str]) -> None:
        """Create the table if it does not exist."""
        # Check if the table already exists in the database
        self.logger.info(f"Checking if tables exist. Creating if not.")
        query = (
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        )
        result = self._execute_query(query)

        if not result:
            # Table does not exist, create it
            self.logger.info(f"Creating table ({table_name}) with {columns}...")

            # Modify this part to set datetime fields explicitly
            columns_definition = []
            for col in columns:
                if "date" in col.lower():
                    columns_definition.append(f"{col} DATETIME")
                else:
                    columns_definition.append(f"{col} TEXT")

            # Create the table with appropriate column types
            create_table_query = (
                f"CREATE TABLE {table_name} ({', '.join(columns_definition)})"
            )
            self._execute_query(create_table_query, commit=True)
            self.logger.info(f"Table ({table_name}) created.")
        else:
            self.logger.info(f"Table ({table_name}) already exists.")

    def create(self, table: str, columns: List[str], values: Dict[str, Any]) -> None:
        """Insert a new record into the table."""
        placeholders = ", ".join(["?" for _ in columns])
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        self._execute_query(query, list(values.values()), commit=True)

    def fetch_all(self, table: str) -> List[tuple]:
        """Fetch all rows from the table."""
        query = f"SELECT * FROM {table}"
        return self._execute_query(query, params=[])

    def fetch_one(self, table: str, where_values: Dict[str, Any]) -> tuple:
        """Fetch a single row from the table based on conditions."""
        where_clause = " AND ".join([f"{col} = ?" for col in where_values])
        query = f"SELECT * FROM {table} WHERE {where_clause}"
        return self._execute_query(query, list(where_values.values()))[
            0
        ]  # Return the first result

    def update(
        self, table: str, set_values: Dict[str, Any], where_values: Dict[str, Any]
    ) -> None:
        """Update a record in the table."""
        set_clause = ", ".join([f"{col} = ?" for col in set_values])
        where_clause = " AND ".join([f"{col} = ?" for col in where_values])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = list(set_values.values()) + list(where_values.values())
        self._execute_query(query, params, commit=True)
