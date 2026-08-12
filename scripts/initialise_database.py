import logging

from app.database.connection import DatabaseConnection
from app.config import DATABASE_SCHEMA_PATH, DATABASE_PATH
from app.utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


def main():
    logger.info("Running initialise_database script")
    with DatabaseConnection(DATABASE_PATH) as conn:
        schema_sql = DATABASE_SCHEMA_PATH.read_text()
        conn.executescript(schema_sql)
        logger.info(
            "%r initialised with %r", DATABASE_PATH.name, DATABASE_SCHEMA_PATH.name
        )


if __name__ == "__main__":
    configure_logging(level="DEBUG", console_log=True)
    main()
