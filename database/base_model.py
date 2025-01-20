from typing import List, Dict, Any
from sqlalchemy.ext.declarative import declarative_base
from database.db_manager import DatabaseManager

Base = declarative_base()


class BaseModel:
    db_manager = DatabaseManager()

    @property
    def session(cls):
        return cls.db_manager.get_session()

    @classmethod
    def initialize(cls, base):
        cls.db_manager.initialize_database(base)

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
