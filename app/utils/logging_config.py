import logging
from logging.handlers import RotatingFileHandler

from app.config import LOG_FILE


def configure_logging(level: str = "INFO", console_log: bool = False) -> None:
    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s.%(msecs)03d "
            "%(levelname)-8s "
            "%(name)s "
            "[%(filename)s:%(lineno)d] "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handlers = []
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10_000_000,
        backupCount=5,
    )
    file_handler.setFormatter(formatter)
    handlers.append(file_handler)

    if console_log:
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        handlers.append(console)

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        handlers=handlers,
    )