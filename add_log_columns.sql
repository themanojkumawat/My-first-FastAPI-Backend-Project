-- Quick migration: Add new columns to logs table
-- Run: psql -h 127.0.0.1 -U drivergo -d drivergo_db -f add_log_columns.sql

ALTER TABLE logs ADD COLUMN IF NOT EXISTS status_code INTEGER;
ALTER TABLE logs ADD COLUMN IF NOT EXISTS user_id INTEGER;
ALTER TABLE logs ADD COLUMN IF NOT EXISTS ip_address VARCHAR;
ALTER TABLE logs ADD COLUMN IF NOT EXISTS duration_ms INTEGER;
