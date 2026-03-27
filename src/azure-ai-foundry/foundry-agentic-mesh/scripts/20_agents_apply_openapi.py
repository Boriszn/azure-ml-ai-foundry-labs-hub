#!/usr/bin/env python3
"""Create or replace demo agents (OpenAPI tool variant).

This script creates:
- Agent 3: Policy/Docs specialist
- Agent 1: Orchestrator with:
  - Connected Agent Tool (delegation to Agent 3)
  - OpenAPI Tool pointing to the MCP Docs Server (HTTP)

This variant is recommended for using Azure AI Foundry Agent Playground as the UI,
because tool execution happens server-side through the OpenAPI tool.
"""

import json
import os
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ConnectedAgentTool, OpenApiTool, OpenApiAnonymousAuthDetails

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / ".state"
STATE_FILE = STATE_DIR / "agents.json"

AGENT1_NAME = "meetup_orchestrator"
AGENT3_NAME = "meetup_policy_docs"

AGENT1_PROMPT = (ROOT / "agents" / "agent1-orchestrator" / "system.md").read_text(encoding="utf-8")
AGENT3_PROMPT = (ROOT / "agents" / "agent3-policy-docs" / "system.md").read_text(encoding="utf-8")

PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]
MODEL_DEPLOYMENT_NAME = os.environ["MODEL_DEPLOYMENT_NAME"]
MCP_BASEURL = os.environ.get("MCP_DOCS_SERVER_BASEURL", "http://localhost:8080").rstrip("/")

OPENAPI_SPEC_PATH = ROOT / "services" / "mcp-docs-server" / "openapi.json"


def _load_state() -> dict | None:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return None


def _save_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def main() -> None:
    spec = json.loads(OPENAPI_SPEC_PATH.read_text(encoding="utf-8"))

    # Patch server URL to match deployment
    spec["servers"] = [{"url": MCP_BASEURL}]

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

    openapi_tool = OpenApiTool(
        name="mcp_docs_tools",
        description="Tools for document search and change request drafting.",
        spec=spec,
        auth=OpenApiAnonymousAuthDetails(),
    )

    agent1 = project_client.agents.create_agent(
        model=MODEL_DEPLOYMENT_NAME,
        name=AGENT1_NAME,
        instructions=AGENT1_PROMPT,
        tools=[*connected_policy.definitions, *openapi_tool.definitions],
    )

    _save_state(
        {
            "agent1": {"id": agent1.id, "name": agent1.name},
            "agent3": {"id": agent3.id, "name": agent3.name},
            "project_endpoint": PROJECT_ENDPOINT,
            "model_deployment_name": MODEL_DEPLOYMENT_NAME,
            "variant": "openapi",
            "mcp_baseurl": MCP_BASEURL,
        }
    )

    print("Created agents:")
    print(f"- Agent 1 (Orchestrator): {agent1.name}  id={agent1.id}")
    print(f"- Agent 3 (Policy/Docs):  {agent3.name}  id={agent3.id}")
    print(f"MCP base URL: {MCP_BASEURL}")
    print(f"State file: {STATE_FILE}")


if __name__ == "__main__":
    main()
