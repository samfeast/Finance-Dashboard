import logging
import time

from app.database.repository import Repository
from app.integrations.truelayer.client import TrueLayerClient
from app.integrations.truelayer.exceptions import AuthExpiredException
from app.models.tokens import Tokens

logger = logging.getLogger(__name__)


def rotate_access_token(
    repo: Repository, truelayer: TrueLayerClient, tokens: Tokens
) -> None:
    try:
        refreshed = truelayer.refresh_access_token(tokens.refresh_token)
    except AuthExpiredException:
        with repo.transaction():
            repo.log_refresh_token_expiry(tokens.provider_id)
        logger.info("Refresh token expiry logged for %r", tokens.provider_id)
        raise AuthExpiredException(
            "Refresh token has expired, user must reauthenticate"
        ) from None

    refreshed_tokens = Tokens(
        provider_id=tokens.provider_id,
        access_token=refreshed.access_token,
        access_token_expiry=refreshed.access_token_expiry,
        refresh_token=refreshed.refresh_token,
        refresh_token_expired=False,
        last_updated=int(time.time()),
    )

    with repo.transaction():
        repo.store_tokens(refreshed_tokens)

    logger.info("Updated access tokens stored for %r", tokens.provider_id)
