from contextlib import contextmanager
import logging
from sqlite3 import Connection
import sqlite3

from app.models.account_metadata import AccountMetadata
from app.models.tokens import Tokens

logger = logging.getLogger(__name__)


class RepositoryError(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Repository:
    def __init__(self, conn: Connection):
        self._conn = conn

    # Allows the use of 'with Repository.transaction():' to begin a single atomic transaction
    @contextmanager
    def transaction(self):
        try:
            yield
            self._conn.commit()
        except:
            self._conn.rollback()
            raise

    def store_tokens(self, data: Tokens) -> None:
        try:
            self._conn.execute(
                """
                INSERT INTO tokens (
                    provider_id, 
                    access_token, 
                    access_token_expiry, 
                    refresh_token, 
                    refresh_token_expired
                )
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(provider_id) DO UPDATE SET
                    access_token = excluded.access_token,
                    access_token_expiry = excluded.access_token_expiry,
                    refresh_token = excluded.refresh_token,
                    refresh_token_expired = excluded.refresh_token_expired
                """,
                (
                    data.provider_id,
                    data.access_token,
                    data.access_token_expiry,
                    data.refresh_token,
                    data.refresh_token_expired,
                ),
            )
        except sqlite3.Error as e:
            raise RepositoryError(
                f"Failed to store tokens for {data.provider_id!r}"
            ) from e

    def store_account_metadata(self, data: AccountMetadata):
        try:
            self._conn.execute(
                """
                INSERT INTO account_metadata (
                    account_id,
                    provider_id,
                    account_type,
                    display_name,
                    currency,
                    account_number,
                    sort_code
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(account_id) DO UPDATE SET
                    provider_id = excluded.provider_id,
                    account_type = excluded.account_type,
                    display_name = excluded.display_name,
                    currency = excluded.currency,
                    account_number = excluded.account_number,
                    sort_code = excluded.sort_code
                """,
                (
                    data.account_id,
                    data.provider_id,
                    data.account_type,
                    data.display_name,
                    data.currency,
                    data.account_number,
                    data.sort_code,
                ),
            )
        except sqlite3.Error as e:
            raise RepositoryError(
                f"Failed to store account metadata for {data.account_id!r}"
            ) from e

    def log_refresh_token_expiry(self, provider_id: str) -> None:
        try:
            self._conn.execute(
                """UPDATE tokens SET refresh_token_expired = 1 WHERE provider_id = ?""",
                (provider_id,),
            )
        except sqlite3.Error as e:
            raise RepositoryError(
                f"Failed to record refresh token expiry for {provider_id!r}"
            ) from e

    def get_all_provider_tokens(self) -> list[Tokens]:
        try:
            cur = self._conn.cursor()
            cur.execute("""SELECT * FROM tokens""")
            data = cur.fetchall()
        except sqlite3.Error as e:
            raise RepositoryError("Failed to get provider tokens") from e

        return [
            Tokens(
                provider_id=row["provider_id"],
                access_token=row["access_token"],
                access_token_expiry=row["access_token_expiry"],
                refresh_token=row["refresh_token"],
                refresh_token_expired=row["refresh_token_expired"] == 1,
            )
            for row in data
        ]

    def get_provider_tokens(self, provider_id: str) -> Tokens | None:
        try:
            cur = self._conn.cursor()
            cur.execute(
                """SELECT * FROM tokens WHERE provider_id = ?""", (provider_id,)
            )
            data = cur.fetchone()
        except sqlite3.Error as e:
            raise RepositoryError(
                f"Failed to get provider tokens for {provider_id!r}"
            ) from e

        if data is None:
            return None

        return Tokens(
            provider_id=data["provider_id"],
            access_token=data["access_token"],
            access_token_expiry=data["access_token_expiry"],
            refresh_token=data["refresh_token"],
            refresh_token_expired=data["refresh_token_expired"] == 1,
        )
