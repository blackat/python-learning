#!/usr/bin/env bash
# clean.sh — clear Python cache and run pytest

set -e

echo "🧹 Clearing Python cache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
rm -rf .pytest_cache 2>/dev/null || true

echo "✅ Cache cleared"
echo ""
echo "🧪 Running tests..."
pytest