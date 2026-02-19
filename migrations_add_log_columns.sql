-- Run this only if you already have a "logs" table and need to add new columns.
-- PostgreSQL example:

ALTER TABLE logs ADD COLUMN IF NOT EXISTS status_code INTEGER;
ALTER TABLE logs ADD COLUMN IF NOT EXISTS user_id INTEGER;
ALTER TABLE logs ADD COLUMN IF NOT EXISTS ip_address VARCHAR;
ALTER TABLE logs ADD COLUMN IF NOT EXISTS duration_ms INTEGER;
