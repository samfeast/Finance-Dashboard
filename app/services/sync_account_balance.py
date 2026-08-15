import logging

from app.database.repository import Repository
from app.integrations.truelayer.client import TrueLayerClient

logger = logging.getLogger(__name__)


def sync_account_balance(repo: Repository, truelayer: TrueLayerClient, account_id: str):
    balance_snapshot = truelayer.get_account_balance(account_id)
    logger.info("Storing balance snapshot for account id %r", account_id)
    with repo.transaction():
        repo.store_balance_snapshot(balance_snapshot)
