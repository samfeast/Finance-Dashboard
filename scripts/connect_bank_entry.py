import logging

from app.config import DATABASE_PATH
from app.database.connection import DatabaseConnection
from app.database.repository import Repository
from app.integrations.ipify import IPifyClient
from app.integrations.truelayer.auth import exchange_auth_code
from app.integrations.truelayer.client import TrueLayerClient
from app.services.get_public_ip import get_public_ip
from app.utils.logging_config import configure_logging
from app.services.connect_bank import connect_bank

logger = logging.getLogger(__name__)

# Auth URL
print(
    "https://auth.truelayer.com/?response_type=code&client_id=personalfinance-e44367&redirect_uri=https://console.truelayer.com/redirect-page&scope=info%20accounts%20balance%20transactions%20offline_access&providers=uk-cs-mock"
)


def main():
    logger.info("Running connect_bank_entry script")
    auth_code = input("Auth code: ")
    anon_tokens = exchange_auth_code(auth_code)
    with DatabaseConnection(DATABASE_PATH) as conn:
        repo = Repository(conn)
        ipify = IPifyClient()

        ip_addr = get_public_ip(repo, ipify)

        truelayer = TrueLayerClient(ip_addr, anon_tokens.access_token)

        connect_bank(repo, truelayer, anon_tokens)


if __name__ == "__main__":
    configure_logging(level="DEBUG", console_log=True)
    main()
