# docs-fastmcp (Option B)

A minimal MCP docs search server implemented with FastMCP.

## Setup

```bash
cd mcp-docs-fastmcp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env
```

## Run (stdio)

```bash
python server.py --transport stdio
```

## Run (SSE / HTTP)

```bash
python server.py --transport sse --host 0.0.0.0 --port 8081
```

Tool exposed:

- `search_docs(query: str, top_k: int=5)` -> `{ "results": [...] }`
