DROP TABLE IF EXISTS tokens;
DROP TABLE IF EXISTS account_metadata;
DROP TABLE IF EXISTS balance_snapshots;
CREATE TABLE tokens (
    provider_id TEXT PRIMARY KEY,
    access_token TEXT NOT NULL,
    access_token_expiry INTEGER NOT NULL,
    refresh_token TEXT NOT NULL,
    refresh_token_expired INTEGER NOT NULL 
);
CREATE TABLE account_metadata (
    account_id TEXT PRIMARY KEY,
    provider_id TEXT NOT NULL,
    account_type TEXT NOT NULL,
    display_name TEXT NOT NULL,
    currency TEXT NOT NULL,
    account_number TEXT,
    sort_code TEXT
);
CREATE TABLE balance_snapshots (
    account_id TEXT NOT NULL,
    snapshot_timestamp INTEGER NOT NULL,
    available_balance INTEGER NOT NULL,
    current_balance_minor INTEGER NOT NULL,
    overdraft_minor INTEGER NOT NULL,
    scale INTEGER NOT NULL,
    PRIMARY KEY (account_id, snapshot_timestamp),
    FOREIGN KEY (account_id) REFERENCES account_metadata(account_id)
);
