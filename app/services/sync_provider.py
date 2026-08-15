import logging
import time

from app.database.repository import Repository
from app.integrations.truelayer.client import (
    AuthExpiredException,
    TrueLayerClient,
)
from app.models.tokens import Tokens
from app.services.rotate_access_token import rotate_access_token
from app.services.sync_account_balance import sync_account_balance
from app.services.sync_account_transactions import sync_account_transactions

TOKEN_REFRESH_BUFFER_SECONDS = 300

logger = logging.getLogger(__name__)


def sync_provider(repo: Repository, truelayer: TrueLayerClient, tokens: Tokens) -> None:
    # If both the access and refresh tokens have expired the user must reauthenticate
    if (
        _access_token_invalid(tokens.access_token_expiry)
        and tokens.refresh_token_expired
    ):
        logger.warning(
            "Refresh token was logged as expired at %s, user must reauthenticate",
            tokens.last_updated,
        )
        # Don't attempt refresh if token is already logged as expired
        raise AuthExpiredException(
            (
                "Refresh token was logged as expired at %s, user must reauthenticate",
                tokens.last_updated,
            )
        )

    # Refresh access token if it's expired
    if _access_token_invalid(tokens.access_token_expiry):
        logger.info("Access token has expired, attempting to refresh")
        rotate_access_token(repo, truelayer, tokens)

    logger.info("Getting account metadata for provider %r", tokens.provider_id)
    accounts = repo.get_provider_accounts(tokens.provider_id)
    for account in accounts:
        sync_account_balance(repo, truelayer, account.account_id)
        sync_account_transactions(
            repo, truelayer, account.account_id, 1784051194, 1786733202
        )


def _access_token_invalid(access_token_expiry: int) -> bool:
    return access_token_expiry < time.time() + TOKEN_REFRESH_BUFFER_SECONDS
