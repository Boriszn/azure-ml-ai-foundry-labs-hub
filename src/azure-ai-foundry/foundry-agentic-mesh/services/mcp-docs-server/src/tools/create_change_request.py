import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


def create_change_request_impl(
    title: str,
    summary: str,
    risk_level: str,
    steps: List[str],
    rollback_plan: str,
    approvers: Optional[List[str]] = None,
) -> Dict[str, Any]:
    out_dir = Path(os.environ.get("CHANGE_REQUEST_OUTPUT_DIR", "data/change_requests_out"))
    out_dir.mkdir(parents=True, exist_ok=True)

    cr_id = f"CR-{uuid.uuid4().hex[:10].upper()}"
    now = datetime.utcnow().isoformat() + "Z"

    payload = {
        "id": cr_id,
        "status": "draft",
        "created_utc": now,
        "title": title,
        "summary": summary,
        "risk_level": risk_level,
        "steps": steps,
        "rollback_plan": rollback_plan,
        "approvers": approvers or [],
    }

    json_path = out_dir / f"{cr_id}.json"
    md_path = out_dir / f"{cr_id}.md"

    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md = []
    md.append(f"# {cr_id}: {title}")
    md.append("")
    md.append(f"**Status:** draft")
    md.append("")
    md.append("## Summary")
    md.append(summary)
    md.append("")
    md.append("## Risk level")
    md.append(risk_level)
    md.append("")
    md.append("## Steps")
    for s in steps:
        md.append(f"- {s}")
    md.append("")
    md.append("## Rollback plan")
    md.append(rollback_plan)
    md.append("")
    md.append("## Approvers")
    if approvers:
        for a in approvers:
            md.append(f"- {a}")
    else:
        md.append("- TBD")
    md.append("")

    md_path.write_text("\n".join(md), encoding="utf-8")

    return {"id": cr_id, "status": "draft", "location": str(json_path)}
