CREATE TABLE credentials (
    rec_id SERIAL PRIMARY KEY,
    credentials_id UUID NOT NULL UNIQUE,
    account_id UUID NOT NULL,
    identifier TEXT NOT NULL,
    secret TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX credentials_account_id_idx ON credentials (account_id);
CREATE INDEX credentials_identifier_idx ON credentials (identifier);
