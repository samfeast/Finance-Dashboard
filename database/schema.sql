DROP TABLE IF EXISTS tokens;
DROP TABLE IF EXISTS balance_snapshots;
DROP TABLE IF EXISTS transaction_classification;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS account_metadata;
CREATE TABLE tokens (
    provider_id TEXT PRIMARY KEY,
    access_token TEXT NOT NULL,
    access_token_expiry INTEGER NOT NULL,
    refresh_token TEXT NOT NULL,
    refresh_token_expired INTEGER NOT NULL,
    last_updated INTEGER NOT NULL
);
CREATE TABLE balance_snapshots (
    account_id TEXT NOT NULL,
    snapshot_timestamp INTEGER NOT NULL,
    update_timestamp INTEGER,
    available_balance_1000x INTEGER,
    current_balance_1000x INTEGER NOT NULL,
    overdraft_1000x INTEGER,
    PRIMARY KEY (account_id, snapshot_timestamp),
    FOREIGN KEY (account_id) REFERENCES account_metadata(account_id)
);
CREATE TABLE transaction_classification (
    transaction_id TEXT NOT NULL,
    classification TEXT NOT NULL,
    PRIMARY KEY (transaction_id, classification),
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);
CREATE TABLE transactions (
    transaction_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    transaction_timestamp INTEGER NOT NULL,
    transaction_description TEXT NOT NULL,
    amount_1000x INTEGER NOT NULL,
    currency TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    category TEXT NOT NULL,
    merchant TEXT,
    running_balance_1000x INTEGER NOT NULL,
    FOREIGN KEY (account_id) REFERENCES account_metadata(account_id)
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