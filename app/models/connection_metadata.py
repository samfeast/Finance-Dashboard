from dataclasses import dataclass


@dataclass
class ConnectionMetadata:
    credentials_id: str
    consent_expires_at: int
    provider_display_name: str
    provider_id: str
    provider_logo_uri: str
    scopes: list[str]
