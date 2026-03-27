# Demo script (10–15 minutes)

## Scene 1 — “Ask for a policy answer”
Prompt:
- “Is public access allowed for storage accounts? Provide a short answer with sources.”

Expected behavior:
- Agent 1 routes to Agent 3 (Policy/Docs).
- Agent 3 requests `search_docs(...)` via MCP tool (OpenAPI).
- Answer returns with a short “Sources” section listing titles/URLs/IDs returned by the tool.

## Scene 2 — “Draft an action”
Prompt:
- “Draft a change request to switch to private endpoints. Keep it low risk.”

Expected behavior:
- Retrieval occurs first.
- Agent returns a structured draft (title, steps, rollback, approvers).
- MCP server writes the draft to `data/change_requests_out/` and returns the artifact location.

## Talking points
- Model choice is independent (GPT‑4o mini here).
- MCP server exposes tools; tool backends can change without rewriting agent prompts.
- Azure AI Search provides scalable retrieval; the agent stays grounded in indexed content.
