from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Transaction:
    transaction_id: str
    account_id: str
    timestamp: int
    description: str
    amount: Decimal
    currency: str
    transaction_type: str
    category: str
    classification: list[str]
    merchant: str | None
    running_balance: Decimal
