#!/usr/bin/env bash
set -euo pipefail

# Loads .env if present (simple parser: KEY="VALUE")
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | sed 's/"//g' | xargs) || true
fi

: "${BLOB_ACCOUNT_NAME:?BLOB_ACCOUNT_NAME is required}"
: "${BLOB_CONTAINER_NAME:?BLOB_CONTAINER_NAME is required}"

SRC_DIR="data/sample_docs"

if [ ! -d "$SRC_DIR" ]; then
  echo "Missing folder: $SRC_DIR"
  exit 1
fi

echo "Ensuring container exists: $BLOB_CONTAINER_NAME"
az storage container create   --name "$BLOB_CONTAINER_NAME"   --account-name "$BLOB_ACCOUNT_NAME"   --auth-mode login   1>/dev/null

echo "Uploading files from $SRC_DIR"
az storage blob upload-batch   --account-name "$BLOB_ACCOUNT_NAME"   --auth-mode login   --destination "$BLOB_CONTAINER_NAME"   --source "$SRC_DIR"   --overwrite true   1>/dev/null

echo "Upload completed."
