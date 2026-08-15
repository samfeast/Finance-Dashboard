import logging

from app.database.repository import Repository
from app.integrations.truelayer.client import TrueLayerClient

logger = logging.getLogger(__name__)


def sync_account_transactions(
    repo: Repository,
    truelayer: TrueLayerClient,
    account_id: str,
    start_timestamp: int,
    end_timestamp: int,
):
    transactions = truelayer.get_account_transactions(
        account_id, start_timestamp, end_timestamp
    )
    logger.info("Storing balance snapshot for account id %r", account_id)
    with repo.transaction():
        repo.store_transactions(transactions)
