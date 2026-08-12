from dataclasses import dataclass


@dataclass
class Tokens:
    provider_id: str
    access_token: str
    access_token_expiry: int
    refresh_token: str
    refresh_token_expired: bool
