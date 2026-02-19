# Migration: Add new columns to logs table

## Problem
The `logs` table exists but is missing new columns: `status_code`, `user_id`, `ip_address`, `duration_ms`.

## Solution

### Option 1: Run Python migration script (Recommended)
```bash
cd /home/manoj/Videos/backend
python3 migrate_logs.py
```

### Option 2: Run SQL directly via psql
```bash
psql -h 127.0.0.1 -U drivergo -d drivergo_db
```

Then run:
```sql
ALTER TABLE logs ADD COLUMN IF NOT EXISTS status_code INTEGER;
ALTER TABLE logs ADD COLUMN IF NOT EXISTS user_id INTEGER;
ALTER TABLE logs ADD COLUMN IF NOT EXISTS ip_address VARCHAR;
ALTER TABLE logs ADD COLUMN IF NOT EXISTS duration_ms INTEGER;
```

### Option 3: Copy-paste SQL commands
If you have access to PostgreSQL, run these commands:
```sql
ALTER TABLE logs ADD COLUMN IF NOT EXISTS status_code INTEGER;
ALTER TABLE logs ADD COLUMN IF NOT EXISTS user_id INTEGER;
ALTER TABLE logs ADD COLUMN IF NOT EXISTS ip_address VARCHAR;
ALTER TABLE logs ADD COLUMN IF NOT EXISTS duration_ms INTEGER;
```

After running migration, restart your backend server.
