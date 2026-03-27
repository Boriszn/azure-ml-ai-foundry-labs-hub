import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from tools_runtime import execute_tool_call

ROOT = Path(__file__).resolve().parents[2]
STATE_FILE = ROOT / ".state" / "agents.json"

load_dotenv()


def _load_agent_id() -> str:
    if not STATE_FILE.exists():
        raise RuntimeError("Missing .state/agents.json. Run scripts/20_agents_apply.py first.")
    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    agent_id = state.get("agent1", {}).get("id")
    if not agent_id:
        raise RuntimeError("Agent 1 ID not found in .state/agents.json.")
    return agent_id


def run_single_turn(prompt: str) -> str:
    project_endpoint = os.environ["PROJECT_ENDPOINT"]
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(endpoint=project_endpoint, credential=credential)

    agent_id = _load_agent_id()

    thread = project_client.agents.threads.create()
    project_client.agents.messages.create(thread_id=thread.id, role="user", content=prompt)

    run = project_client.agents.runs.create(thread_id=thread.id, agent_id=agent_id)

    delay = 0.5
    max_delay = 5.0

    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(delay)
        run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)

        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs: List[Dict[str, Any]] = []

            for tc in tool_calls:
                fn = tc.function.name
                args = tc.function.arguments
                output = execute_tool_call(fn, args)
                tool_outputs.append({"tool_call_id": tc.id, "output": output})

            project_client.agents.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs,
            )
            delay = 0.5
        else:
            delay = min(delay * 1.5, max_delay)

    # Return the last assistant message text
    msgs = list(project_client.agents.messages.list(thread_id=thread.id))
    # messages are returned newest-first in some SDKs; take the last assistant by scanning
    for msg in msgs:
        if msg.get("role") == "assistant":
            content = msg.get("content")
            return content if isinstance(content, str) else json.dumps(content)

    return "(no assistant message returned)"
