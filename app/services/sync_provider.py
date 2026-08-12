import logging
import time

from app.database.repository import Repository
from app.integrations.truelayer.client import (
    AuthExpiredException,
    TrueLayerClient,
)
from app.models.tokens import Tokens
from app.services.rotate_access_token import rotate_access_token

TOKEN_REFRESH_BUFFER_SECONDS = 300

logger = logging.getLogger(__name__)


def sync_provider(repo: Repository, truelayer: TrueLayerClient, tokens: Tokens) -> None:
    if _access_token_valid(tokens.access_token_expiry):
        _get_account_data(repo, truelayer, tokens.provider_id)

    # If access token has expired but refresh token is valid, first rotate the access token
    # The access token is updated inside TrueLayerClient
    elif not tokens.refresh_token_expired:
        # May throw AuthExpiredException if refresh token has expired
        logger.info("Access token has expired, attempting to refresh")
        rotate_access_token(repo, truelayer, tokens)
        _get_account_data(repo, truelayer, tokens.provider_id)

    else:
        logger.warning("Refresh token has expired, user must reauthenticate")
        # Don't attempt refresh if token is already logged as expired
        raise AuthExpiredException(
            "Refresh token has expired, user must reauthenticate"
        )


def _access_token_valid(access_token_expiry: int) -> bool:
    return access_token_expiry > time.time() + TOKEN_REFRESH_BUFFER_SECONDS


def _get_account_data(repo: Repository, truelayer: TrueLayerClient, provider_id: str):
    logger.info("Getting all account data for %r", provider_id)
