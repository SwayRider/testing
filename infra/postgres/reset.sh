#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
docker compose down -v
echo "Persistent test Postgres volume removed. Run 'docker compose up -d' to start fresh."
