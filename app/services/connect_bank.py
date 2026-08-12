import logging

from app.database.repository import Repository
from app.integrations.truelayer.client import TrueLayerClient
from app.models.anonymous_tokens import AnonymousTokens
from app.models.tokens import Tokens

logger = logging.getLogger(__name__)


def connect_bank(
    repo: Repository, truelayer: TrueLayerClient, anon_tokens: AnonymousTokens
) -> None:
    connection_metadata = truelayer.get_connection_metadata()
    account_metadata = truelayer.get_all_account_metadata()

    tokens = Tokens(
        provider_id=connection_metadata.provider_id,
        access_token=anon_tokens.access_token,
        access_token_expiry=anon_tokens.access_token_expiry,
        refresh_token=anon_tokens.refresh_token,
        refresh_token_expired=False,
    )

    with repo.transaction():
        repo.store_tokens(tokens)

        for account in account_metadata:
            repo.store_account_metadata(account)
