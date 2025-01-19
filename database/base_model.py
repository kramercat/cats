from typing import List, Dict, Any
from database.db_manager import DatabaseManager


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        if "Meta" in attrs:
            meta = attrs["Meta"]
            table = getattr(meta, "table", None)
            columns = getattr(meta, "columns", None)
            if table and columns:
                new_class.table = table
                new_class.columns = columns
                new_class.db_manager = DatabaseManager()
                new_class.db_manager.create_table_if_not_exists(table, columns)
        return new_class


class BaseModel(metaclass=ModelMeta):
    table: str
    columns: Dict[str, str]
    db_manager = DatabaseManager()

    @classmethod
    def initialize(cls, table: str, columns: Dict[str, str]) -> None:
        cls.table = table
        cls.columns = columns
        cls.db_manager.create_table_if_not_exists(cls.table, cls.columns)

    @classmethod
    def create(cls, values: Dict[str, Any]) -> None:
        """Insert a new record into the database using the db_manager."""
        cls.db_manager.create(cls.table, list(cls.columns.keys()), values)

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
