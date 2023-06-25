CREATE TABLE accounts (
    rec_id SERIAL PRIMARY KEY,
    account_id UUID NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX accounts_username ON accounts (username);
CREATE INDEX accounts_status ON accounts (status);
