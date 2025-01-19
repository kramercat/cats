from typing import List, Dict, Any
from database.db_manager import DatabaseManager


class BaseModel:
    table: str
    columns: List[str]
    # Initialize the database manager with the path to the database
    db_manager = DatabaseManager()

    @classmethod
    def initialize(cls, table: str, columns: List[str]) -> None:
        cls.table = table
        cls.columns = columns
        cls.db_manager.create_table_if_not_exists(cls.table, cls.columns)

    @classmethod
    def _get_column_names(cls) -> List[str]:
        return cls.columns

    @classmethod
    def _get_table_name(cls) -> str:
        return cls.table

    @classmethod
    def create(cls, values: Dict[str, Any]) -> None:
        """Insert a new record into the database using the db_manager."""
        cls.db_manager.create(cls.table, cls.columns, values)

    @classmethod
    def fetch_all(cls) -> List[tuple]:
        """Fetch all rows from the table."""
        return cls.db_manager.fetch_all(cls.table)

    @classmethod
    def fetch_one(cls, where_values: Dict[str, Any]) -> tuple:
        """Fetch a single row from the table based on conditions."""
        return cls.db_manager.fetch_one(cls.table, where_values)

    @classmethod
    def update(cls, set_values: Dict[str, Any], where_values: Dict[str, Any]) -> None:
        """Update a record in the table."""
        cls.db_manager.update(cls.table, set_values, where_values)
