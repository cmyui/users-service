CREATE TABLE login_attempts (
    rec_id SERIAL PRIMARY KEY,
    login_attempt_id UUID NOT NULL UNIQUE,
    username TEXT NOT NULL,
    user_agent TEXT NOT NULL,
    ip_address TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX login_attempts_username_idx ON login_attempts (username);
