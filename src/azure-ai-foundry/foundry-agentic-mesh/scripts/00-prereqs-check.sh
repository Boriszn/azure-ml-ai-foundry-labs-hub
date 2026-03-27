#!/usr/bin/env bash
set -euo pipefail

missing=0
for cmd in az python3 docker; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing: $cmd"
    missing=1
  fi
done

if [ "$missing" -eq 1 ]; then
  echo "Install missing prerequisites and retry."
  exit 1
fi

echo "OK: prerequisites detected."
