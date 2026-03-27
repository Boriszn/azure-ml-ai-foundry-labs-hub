#!/usr/bin/env bash
set -euo pipefail

# Reference deployment script for the MCP Docs Server using Azure Container Apps.
# This script assumes:
# - Azure CLI is logged in
# - Resource group exists
# - Container Apps environment exists
# - Container image is available in a registry

echo "This script is a placeholder."
echo "Preferred options:"
echo "1) Use azd (infra/azd)"
echo "2) Use: az containerapp up --name <name> --resource-group <rg> --source services/mcp-docs-server --ingress external --target-port 8080"
