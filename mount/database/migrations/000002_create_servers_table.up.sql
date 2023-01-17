CREATE TABLE servers (
    server_id SERIAL NOT NULL PRIMARY KEY,
    server_name VARCHAR(255) NOT NULL UNIQUE,
    hourly_request_limit INTEGER NOT NULL,
    secret_key VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL,
    status VARCHAR(64) NOT NULL,
    updated_at DATETIME NOT NULL DEFAULT NOW(),
    created_at DATETIME NOT NULL DEFAULT NOW()
);
