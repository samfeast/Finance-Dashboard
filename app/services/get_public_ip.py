import os

from dotenv import load_dotenv

from app.config import ENV_PATH
from app.database.repository import Repository
from app.integrations.ipify import IPifyClient

load_dotenv(ENV_PATH)


def get_public_ip(repo: Repository, ipify: IPifyClient) -> str:
    ip = _try_get_cached_ip(repo) or ipify.try_get_ip()
    if ip is None:
        raise RuntimeError("Could not determine public IP address")
    return ip


def _try_get_cached_ip(repo: Repository) -> str | None:
    # TODO: Implement caching logic for IP through repository
    return os.getenv("FALLBACK_IP_TEMP")
