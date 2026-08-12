import logging

from app.config import DATABASE_PATH
from app.database.connection import DatabaseConnection
from app.database.repository import Repository
from app.integrations.ipify import IPifyClient
from app.integrations.truelayer.client import TrueLayerClient
from app.services.get_public_ip import get_public_ip
from app.utils.logging_config import configure_logging
from app.services.sync_provider import sync_provider

logger = logging.getLogger(__name__)


def main():
    logger.info("Running sync_banks script")
    with DatabaseConnection(DATABASE_PATH) as conn:
        repo = Repository(conn)
        ipify = IPifyClient()

        ip_addr = get_public_ip(repo, ipify)

        all_tokens = repo.get_all_provider_tokens()

        for provider_tokens in all_tokens:
            logger.info("Syncing account data for %r", provider_tokens.provider_id)
            truelayer = TrueLayerClient(ip_addr, provider_tokens.access_token)
            sync_provider(repo, truelayer, provider_tokens)


if __name__ == "__main__":
    configure_logging(level="DEBUG", console_log=True)
    main()
