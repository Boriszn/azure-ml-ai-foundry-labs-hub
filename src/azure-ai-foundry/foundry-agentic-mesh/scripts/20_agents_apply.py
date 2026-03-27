#!/usr/bin/env python3
"""Create or replace demo agents (FunctionTool variant).

This script creates:
- Agent 3: Policy/Docs specialist
- Agent 1: Orchestrator with:
  - Connected Agent Tool (delegation to Agent 3)
  - FunctionTool definitions (local function-calling style)

This variant is intended for the optional Python Agent Host mode.
"""

import json
import os
from pathlib import Path
from typing import Any, List, Optional

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ConnectedAgentTool, FunctionTool

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / ".state"
STATE_FILE = STATE_DIR / "agents.json"

AGENT1_NAME = "meetup_orchestrator"
AGENT3_NAME = "meetup_policy_docs"

AGENT1_PROMPT = (ROOT / "agents" / "agent1-orchestrator" / "system.md").read_text(encoding="utf-8")
AGENT3_PROMPT = (ROOT / "agents" / "agent3-policy-docs" / "system.md").read_text(encoding="utf-8")

PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]
MODEL_DEPLOYMENT_NAME = os.environ["MODEL_DEPLOYMENT_NAME"]


# -----------------------------
# FunctionTool schemas (docstring-driven)
# The agent service never executes these functions.
# Execution happens in the optional Python host runtime.
# -----------------------------
def search_docs(query: str, top_k: int = 5) -> str:
    """Search internal documents and return relevant snippets.

    Args:
        query: Search query.
        top_k: Maximum number of results.

    Returns:
        JSON string:
        {
          "results": [
            {"title": "...", "snippet": "...", "source": "..."}
          ]
        }
    """
    raise NotImplementedError


def create_change_request(
    title: str,
    summary: str,
    risk_level: str,
    steps: List[str],
    rollback_plan: str,
    approvers: Optional[List[str]] = None,
) -> str:
    """Create a change request draft artifact.

    Args:
        title: Short title.
        summary: Summary of change.
        risk_level: One of: low, medium, high.
        steps: Ordered steps.
        rollback_plan: Rollback plan.
        approvers: Optional list of approvers.

    Returns:
        JSON string:
        {
          "id": "...",
          "status": "draft",
          "location": "..."
        }
    """
    raise NotImplementedError


def _load_state() -> dict | None:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return None


def _save_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def main() -> None:
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)

    # Replace existing agents tracked in .state to avoid duplicates in the portal.
    state = _load_state()
    if state:
        for key in ("agent1", "agent3"):
            agent_id = state.get(key, {}).get("id")
            if agent_id:
                try:
                    project_client.agents.delete_agent(agent_id)
                except Exception:
                    pass

    agent3 = project_client.agents.create_agent(
        model=MODEL_DEPLOYMENT_NAME,
        name=AGENT3_NAME,
        instructions=AGENT3_PROMPT,
    )

    connected_policy = ConnectedAgentTool(
        id=agent3.id,
        name="policy_docs",
        description=(
            "Use for policy/docs questions. Input should include retrieved doc snippets and sources. "
            "Output must be grounded only in provided sources."
        ),
    )

    functions = FunctionTool(functions={search_docs, create_change_request})

    agent1 = project_client.agents.create_agent(
        model=MODEL_DEPLOYMENT_NAME,
        name=AGENT1_NAME,
        instructions=AGENT1_PROMPT,
        tools=[*connected_policy.definitions, *functions.definitions],
    )

    _save_state(
        {
            "agent1": {"id": agent1.id, "name": agent1.name},
            "agent3": {"id": agent3.id, "name": agent3.name},
            "project_endpoint": PROJECT_ENDPOINT,
            "model_deployment_name": MODEL_DEPLOYMENT_NAME,
            "variant": "functiontool",
        }
    )

    print("Created agents:")
    print(f"- Agent 1 (Orchestrator): {agent1.name}  id={agent1.id}")
    print(f"- Agent 3 (Policy/Docs):  {agent3.name}  id={agent3.id}")
    print(f"State file: {STATE_FILE}")


if __name__ == "__main__":
    main()
