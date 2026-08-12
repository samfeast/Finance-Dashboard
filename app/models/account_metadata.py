from dataclasses import dataclass


@dataclass
class AccountMetadata:
    account_id: str
    account_type: str
    display_name: str
    currency: str
    account_number: str | None
    sort_code: str | None
    provider_id: str
