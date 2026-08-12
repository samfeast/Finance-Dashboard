import logging
from pathlib import Path
import sqlite3

logger = logging.getLogger(__name__)


class DatabaseConnection:
    def __init__(self, path: Path):
        self.path = path

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        # Enforce foreign key constraints
        self.conn.execute("PRAGMA foreign_keys = ON")
        # Allow column names to be addressable
        self.conn.row_factory = sqlite3.Row

        logger.info("Database connection established")
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.error(
                "Database connection exited with exception",
                exc_info=True,
            )

        self.conn.close()
        logger.info("Database connection closed")
