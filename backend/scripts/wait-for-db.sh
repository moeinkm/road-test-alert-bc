#!/usr/bin/env bash
set -euo pipefail

# Configurable timeout with default fallback
TIMEOUT=${DB_TIMEOUT:-30}
echo "⏱️  Waiting for database connection (timeout: ${TIMEOUT}s)..."

until /code/.venv/bin/python - <<'PY'
import os, time
import psycopg2
from psycopg2 import OperationalError

url = os.getenv("DATABASE_URL", "")
if not url:
    print("❌ DATABASE_URL environment variable not set")
    raise SystemExit(1)

for attempt in range(int(os.getenv("DB_TIMEOUT", "30"))):
    try:
        conn = psycopg2.connect(url)
        conn.close()
        print("✅ Database connection successful!")
        raise SystemExit(0)
    except OperationalError as e:
        if attempt == 0:
            print(f"🔄 Attempting to connect to database...")
        elif attempt % 5 == 0:
            print(f"⏳ Still waiting... (attempt {attempt + 1}/{os.getenv('DB_TIMEOUT', '30')})")
        time.sleep(1)

print(f"❌ Failed to connect to database after {os.getenv('DB_TIMEOUT', '30')} attempts")
raise SystemExit(1)
PY
do
  echo "Waiting for database..."
  sleep 1
done
