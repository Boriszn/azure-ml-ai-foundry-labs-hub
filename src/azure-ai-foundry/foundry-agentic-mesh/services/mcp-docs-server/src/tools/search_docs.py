import os
import json
import requests
from typing import Any, Dict, List


def _pick_first(item: Dict[str, Any], keys: List[str], default: str = "") -> str:
    for k in keys:
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return default


def search_docs_impl(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Query Azure AI Search and return a small normalized result set.

    Expected env vars:
    - AZURE_SEARCH_ENDPOINT: https://<service>.search.windows.net
    - AZURE_SEARCH_INDEX_NAME: index name
    - AZURE_SEARCH_API_KEY: admin/query key
    - AZURE_SEARCH_API_VERSION: REST api-version (default: 2024-07-01)
    """
    endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT", "").rstrip("/")
    index_name = os.environ.get("AZURE_SEARCH_INDEX_NAME", "")
    api_key = os.environ.get("AZURE_SEARCH_API_KEY", "")
    api_version = os.environ.get("AZURE_SEARCH_API_VERSION", "2024-07-01")

    if not endpoint or not index_name or not api_key:
        raise RuntimeError("Missing AZURE_SEARCH_* environment variables.")

    url = f"{endpoint}/indexes/{index_name}/docs/search?api-version={api_version}"
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }

    body = {
        "search": query,
        "top": top_k,
        "queryType": "simple",
        "select": "*",
    }

    resp = requests.post(url, headers=headers, data=json.dumps(body), timeout=30)
    if resp.status_code >= 300:
        raise RuntimeError(f"Azure AI Search query failed: {resp.status_code} {resp.text}")

    data = resp.json()
    values = data.get("value", []) or []

    out: List[Dict[str, Any]] = []
    for hit in values:
        title = _pick_first(
            hit,
            keys=[
                "title",
                "metadata_title",
                "metadata_storage_name",
                "metadata_storage_path",
                "name",
            ],
            default="(untitled)",
        )

        # Many wizard-generated indexes include a 'content' field; others do not.
        snippet = _pick_first(hit, keys=["content", "chunk", "text", "summary"], default="").strip()
        if not snippet:
            # fall back to any string field
            for k, v in hit.items():
                if k.startswith("@"):
                    continue
                if isinstance(v, str) and v.strip():
                    snippet = v.strip()
                    break

        source = _pick_first(
            hit,
            keys=[
                "source",
                "url",
                "metadata_storage_path",
                "metadata_storage_url",
                "id",
                "key",
            ],
            default="(unknown-source)",
        )

        score = hit.get("@search.score")
        out.append(
            {
                "title": title,
                "snippet": (snippet[:500] + "…") if len(snippet) > 500 else snippet,
                "source": source,
                "score": float(score) if isinstance(score, (int, float)) else None,
            }
        )

    return out
