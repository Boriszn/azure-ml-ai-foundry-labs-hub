import os
import re
import base64
import argparse
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

# FastMCP import path can differ by version.
# If this import fails, try: `from mcp.server import FastMCP`
from mcp.server.fastmcp import FastMCP  # type: ignore

load_dotenv()

mcp = FastMCP("docs-fastmcp")

# -------------------------
# Helpers
# -------------------------

_BASE64_RE = re.compile(r"^[A-Za-z0-9+/]+={0,2}$")


def _try_b64_decode(s: str) -> Optional[str]:
    """
    Decode base64 strings (common in Azure Search metadata fields).
    Returns decoded string if it looks valid & printable, else None.
    """
    if not s or len(s) < 12:
        return None
    if len(s) % 4 != 0:
        return None
    if not _BASE64_RE.match(s):
        return None

    try:
        raw = base64.b64decode(s, validate=True)
        decoded = raw.decode("utf-8", errors="strict").strip()
    except Exception:
        return None

    # Heuristic: keep only printable-ish strings
    if not decoded or any(ord(ch) < 9 for ch in decoded):
        return None
    return decoded


def _decode_if_b64(s: Optional[str]) -> Optional[str]:
    if not s:
        return s
    decoded = _try_b64_decode(s)
    return decoded if decoded else s


def _pick_first(d: Dict[str, Any], keys: List[str]) -> Optional[str]:
    for k in keys:
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


def _build_snippet(doc: Dict[str, Any], max_len: int = 280) -> str:
    # Try common chunk/content fields
    text = _pick_first(doc, ["chunk", "content", "text", "page_content"]) or ""
    text = re.sub(r"\s+", " ", text).strip()
    return (text[:max_len] + "…") if len(text) > max_len else text


def _search_azure_ai_search(query: str, top_k: int) -> List[Dict[str, Any]]:
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT", "").rstrip("/")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "")
    api_key = os.getenv("AZURE_SEARCH_API_KEY", "")
    api_version = os.getenv("AZURE_SEARCH_API_VERSION", "2024-07-01")
    select_fields = os.getenv("AZURE_SEARCH_SELECT_FIELDS", "").strip()

    if not endpoint or not index_name or not api_key:
        raise RuntimeError(
            "Missing env vars. Need AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_INDEX_NAME, AZURE_SEARCH_API_KEY."
        )

    url = f"{endpoint}/indexes/{index_name}/docs/search?api-version={api_version}"
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }

    payload: Dict[str, Any] = {
        "search": query if query else "*",
        "top": int(top_k),
        "queryType": "simple",
    }

    if select_fields:
        payload["select"] = select_fields

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("value", [])


# -------------------------
# MCP Tool
# -------------------------

@mcp.tool()
def search_docs(query: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Search indexed documents and return normalized results.

    - decodes base64 title/source/metadata paths when applicable
    - returns clean source_url field
    """
    hits = _search_azure_ai_search(query=query, top_k=top_k)
    results: List[Dict[str, Any]] = []

    for h in hits:
        raw_title = _pick_first(h, ["title", "metadata_storage_name", "document_name"])
        raw_source = _pick_first(
            h,
            [
                "source",
                "source_url",
                "url",
                "metadata_storage_path",
                "metadata_storage_url",
            ],
        )

        title = _decode_if_b64(raw_title) or raw_title or "Untitled"
        source = _decode_if_b64(raw_source) or raw_source

        source_url = source
        if isinstance(title, str) and title.startswith(("http://", "https://")) and not (
            source_url and str(source_url).startswith(("http://", "https://"))
        ):
            source_url = title

        snippet = _build_snippet(h)

        results.append(
            {
                "title": title,
                "source_url": source_url,
                "snippet": snippet,
                "id": _pick_first(h, ["id", "key", "metadata_storage_path"]),
                "score": h.get("@search.score"),
            }
        )

    return {"results": results}


# -------------------------
# Entrypoint
# -------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--transport", default="stdio", choices=["stdio", "sse"])
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8081)
    args = ap.parse_args()

    if args.transport == "stdio":
        mcp.run()
    else:
        mcp.run(transport="sse", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
