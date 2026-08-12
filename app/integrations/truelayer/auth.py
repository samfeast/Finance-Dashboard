import logging
import os
import time

from dotenv import load_dotenv
import requests

from app.config import AUTH_REDIRECT_URI, ENV_PATH
from app.integrations.truelayer.exceptions import AuthExpiredException, TrueLayerError
from app.models.anonymous_tokens import AnonymousTokens

load_dotenv(ENV_PATH)

logger = logging.getLogger(__name__)


def exchange_auth_code(auth_code: str) -> AnonymousTokens:
    logger.info("Exchanging auth code for access token")
    try:
        response = requests.post(
            "https://auth.truelayer.com/connect/token",
            json={
                "grant_type": "authorization_code",
                "client_id": os.getenv("CLIENT_ID"),
                "client_secret": os.getenv("CLIENT_SECRET"),
                "code": auth_code,
                "redirect_uri": AUTH_REDIRECT_URI,
            },
        )

        if response.status_code == 400:
            logger.warning("Auth code exchange returned 400 - user must reauthenticate")
            raise AuthExpiredException(
                "Unable to acquire access token, user must reauthenticate"
            )

        response.raise_for_status()

        data = response.json()

        logger.info("Successfully obtained access token via auth code exchange")
        return AnonymousTokens(
            access_token=data["access_token"],
            access_token_expiry=int(data["expires_in"] + time.time()),
            refresh_token=data["refresh_token"],
        )
    except requests.RequestException as e:
        raise TrueLayerError("Failed to exchange auth code") from e
