#!/bin/bash
cd "$(dirname "$0")"
set -a; source .env; set +a
exec venv/bin/uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
