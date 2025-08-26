#!/usr/bin/env bash
set -euo pipefail

APP_PORT=${APP_PORT:-8000}
TIMEOUT=${SMOKE_TIMEOUT:-10}

echo "🚬 Running smoke test on http://localhost:${APP_PORT}/api/v1/health"

# Check if the service is responding
if curl -fS --max-time $TIMEOUT "http://localhost:${APP_PORT}/api/v1/health" 2>/dev/null | grep -q '"status":"ok"'; then
    echo "✅ Health check passed - service is running correctly"
    exit 0
else
    echo "❌ Health check failed - service is not responding correctly"
    echo "💡 Check if the service is running: docker compose ps"
    echo "💡 Check logs: docker compose logs api"
    exit 1
fi
