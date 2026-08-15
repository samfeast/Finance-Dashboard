from dataclasses import dataclass
from decimal import Decimal


@dataclass
class BalanceSnapshot:
    account_id: str
    snapshot_timestamp: int
    update_timestamp: int | None
    currency: str
    available: Decimal | None
    current: Decimal
    overdraft: Decimal | None
