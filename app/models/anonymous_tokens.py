from dataclasses import dataclass


@dataclass
class AnonymousTokens:
    access_token: str
    access_token_expiry: int
    refresh_token: str
