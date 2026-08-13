from dataclasses import dataclass
from decimal import Decimal


@dataclass
class BalanceSnapshot:
    account_id: str
    snapshot_timestamp: int
    update_timestamp: int
    currency: str
    available: Decimal
    current: Decimal
    overdraft: Decimal
