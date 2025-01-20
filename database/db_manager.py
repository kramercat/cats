from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import logging
from utils.logger_utils import CustomLogger


class DatabaseManager:
    def __init__(self, db_path: str = None, logger: CustomLogger = None):
        self.db_path = db_path or os.getenv("DB_PATH", "sqlite:///data/database.db")
        if not self.db_path.startswith("sqlite:///"):
            self.db_path = f"sqlite:///{self.db_path}"
        self.logger = logger or CustomLogger(
            name="sqlalchemy.engine", log_level=logging.DEBUG
        )
        self.engine = create_engine(self.db_path, echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        """Get a new SQLAlchemy session."""
        session = self.Session()
        return session

    def initialize_database(self, base):
        """Initialize the database by creating all tables."""
        self.logger.info("Checking if tables exist. Creating if not.")
        base.metadata.create_all(self.engine)
        self.logger.info("Database initialized.")
