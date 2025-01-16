from typing import List, Dict, Any
import logging
from utils.logger_utils import CustomLogger

logger = CustomLogger(name="db_models", log_level=logging.DEBUG)


class BaseModel:
    table: str
    columns: List[str]

    @classmethod
    def _get_column_names(cls) -> List[str]:
        return cls.columns

    @classmethod
    def _get_table_name(cls) -> str:
        return cls.table

    @classmethod
    def create(cls, db_manager, values: Dict[str, Any]) -> None:
        """Insert a new record into the database using the db_manager."""
        db_manager.create(cls.table, cls.columns, values)

    @classmethod
    def fetch_all(cls, db_manager) -> List[tuple]:
        """Fetch all rows from the table."""
        return db_manager.fetch_all(cls.table)

    @classmethod
    def fetch_one(cls, db_manager, where_values: Dict[str, Any]) -> tuple:
        """Fetch a single row from the table based on conditions."""
        return db_manager.fetch_one(cls.table, where_values)

    @classmethod
    def update(
        cls, db_manager, set_values: Dict[str, Any], where_values: Dict[str, Any]
    ) -> None:
        """Update a record in the table."""
        db_manager.update(cls.table, set_values, where_values)

    @classmethod
    def log_info(cls, message):
        logger.info(message)
