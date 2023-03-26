CREATE TABLE accounts (
    rec_id SERIAL PRIMARY KEY,
    account_id UUID NOT NULL UNIQUE,
    phone_number TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX accounts_phone_number ON accounts (phone_number);
CREATE INDEX accounts_status ON accounts (status);
