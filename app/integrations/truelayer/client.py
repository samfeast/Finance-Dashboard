import logging
import os
import time
import requests
from dotenv import load_dotenv
from datetime import datetime

from app.config import ENV_PATH
from app.integrations.truelayer.exceptions import AuthExpiredException, TrueLayerError
from app.models.account_metadata import AccountMetadata
from app.models.anonymous_tokens import AnonymousTokens
from app.models.connection_metadata import ConnectionMetadata

load_dotenv(ENV_PATH)

logger = logging.getLogger(__name__)


class TrueLayerClient:
    def __init__(self, ip_addr: str, access_token: str):
        self.ip_addr = ip_addr
        self.access_token = access_token

    def refresh_access_token(self, refresh_token: str) -> AnonymousTokens:
        logger.info("Refreshing access token")
        try:
            response = requests.post(
                "https://auth.truelayer.com/connect/token",
                json={
                    "grant_type": "refresh_token",
                    "client_id": os.getenv("CLIENT_ID"),
                    "client_secret": os.getenv("CLIENT_SECRET"),
                    "refresh_token": refresh_token,
                },
            )

            if response.status_code == 400:
                logger.warning("Token refresh returned 400 - user must reauthenticate")
                raise AuthExpiredException(
                    "Unable to acquire access token, user must reauthenticate"
                )

            response.raise_for_status()

            data = response.json()

            self.access_token = data["access_token"]

            logger.info("Successfully refreshed access token")
            return AnonymousTokens(
                access_token=self.access_token,
                access_token_expiry=int(data["expires_in"] + time.time()),
                refresh_token=data["refresh_token"],
            )
        except requests.RequestException as e:
            raise TrueLayerError("Failed to refresh access token") from e

    def get_connection_metadata(self) -> ConnectionMetadata:
        logger.info("Fetching connection metadata")
        try:
            response = requests.get(
                "https://api.truelayer.com/data/v1/me",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "X-PSU-IP": self.ip_addr,
                },
            )
            if response.status_code == 400:
                logger.warning(
                    "Failed to get connection metadata - access token has expired"
                )
                raise AuthExpiredException(
                    "Failed to get connection metadata - access token has expired"
                )

            response.raise_for_status()
        except requests.RequestException as e:
            raise TrueLayerError("Failed to get connection metadata") from e

        data = response.json()

        if len(data["results"]) != 1:
            logger.error(
                "Unexpected number of metadata results: %s", len(data["results"])
            )
            raise RuntimeError("Unexpected number of metadata results")

        result = data["results"][0]
        provider = result["provider"]
        consent_expiry_timestamp = int(
            datetime.fromisoformat(result["consent_expires_at"]).timestamp()
        )

        logger.info("Successfully fetched metadata for %r", provider["provider_id"])
        return ConnectionMetadata(
            credentials_id=result["credentials_id"],
            consent_expires_at=consent_expiry_timestamp,
            provider_display_name=provider["display_name"],
            provider_id=provider["provider_id"],
            provider_logo_uri=provider["logo_uri"],
            scopes=result["scopes"],
        )

    def get_all_account_metadata(self) -> list[AccountMetadata]:
        logger.info("Fetching metadata for all accounts")
        try:
            response = requests.get(
                "https://api.truelayer.com/data/v1/accounts",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "X-PSU-IP": self.ip_addr,
                },
            )

            if response.status_code == 400:
                logger.warning(
                    "Failed to get account metadata - access token has expired"
                )
                raise AuthExpiredException(
                    "Failed to get account metadata - access token has expired"
                )

            response.raise_for_status()
        except requests.RequestException as e:
            raise TrueLayerError("Failed to get metadata for all accounts") from e

        data = response.json()

        logger.info(
            "Successfully fetched metadata for %s accounts", len(data["results"])
        )
        return [
            AccountMetadata(
                account_id=account["account_id"],
                account_type=account["account_type"],
                display_name=account["display_name"],
                currency=account["currency"],
                account_number=account["account_number"].get("number"),
                sort_code=account["account_number"].get("sort_code"),
                provider_id=account["provider"]["provider_id"],
            )
            for account in data["results"]
        ]
