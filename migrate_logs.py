"""
Migration script: Add new columns to logs table if they don't exist.
Run this once: python migrate_logs.py
"""
from sqlalchemy import text
from database import engine

def migrate():
    """Add new columns to logs table."""
    with engine.begin() as conn:  # begin() auto-commits
        try:
            # Check if columns exist, if not add them
            conn.execute(text("""
                DO $$ 
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                   WHERE table_name='logs' AND column_name='status_code') THEN
                        ALTER TABLE logs ADD COLUMN status_code INTEGER;
                    END IF;
                    
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                   WHERE table_name='logs' AND column_name='user_id') THEN
                        ALTER TABLE logs ADD COLUMN user_id INTEGER;
                    END IF;
                    
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                   WHERE table_name='logs' AND column_name='ip_address') THEN
                        ALTER TABLE logs ADD COLUMN ip_address VARCHAR;
                    END IF;
                    
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                   WHERE table_name='logs' AND column_name='duration_ms') THEN
                        ALTER TABLE logs ADD COLUMN duration_ms INTEGER;
                    END IF;
                END $$;
            """))
            print("✅ Migration successful! New columns added to logs table.")
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            raise

if __name__ == "__main__":
    migrate()
