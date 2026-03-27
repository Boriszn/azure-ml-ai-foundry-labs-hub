#!/usr/bin/env python3
"""Delete demo agents recorded in .state/agents.json."""

import json
import os
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = ROOT / ".state" / "agents.json"

PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]


def main() -> None:
    if not STATE_FILE.exists():
        print("No state file found.")
        return

    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)

    for key in ("agent1", "agent3"):
        agent_id = state.get(key, {}).get("id")
        if not agent_id:
            continue
        try:
            project_client.agents.delete_agent(agent_id)
            print(f"Deleted {key}: {agent_id}")
        except Exception as e:
            print(f"Could not delete {key} ({agent_id}): {e}")

    try:
        STATE_FILE.unlink()
    except Exception:
        pass


if __name__ == "__main__":
    main()
