import json
import os
from typing import Any, Dict, List

import requests


MCP_BASEURL = os.environ.get("MCP_DOCS_SERVER_BASEURL", "http://localhost:8080").rstrip("/")


def _post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{MCP_BASEURL}{path}"
    resp = requests.post(url, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()


def execute_tool_call(function_name: str, arguments_json: str) -> str:
    """Executes a tool call and returns a string output (JSON string recommended)."""
    args = json.loads(arguments_json or "{}")

    if function_name == "search_docs":
        data = _post("/tools/search_docs", {"query": args.get("query", ""), "top_k": args.get("top_k", 5)})
        return json.dumps(data)

    if function_name == "create_change_request":
        data = _post("/tools/create_change_request", args)
        return json.dumps(data)

    raise ValueError(f"Unsupported function: {function_name}")
