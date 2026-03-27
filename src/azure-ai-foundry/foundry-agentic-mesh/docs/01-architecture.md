# Architecture (short)

This demo uses Azure AI Foundry as the agent UI and control plane, Azure AI Search as the retrieval backend, and an HTTP tool service (MCP Docs Server) as the tool interface.

Flow:
1. A prompt is entered in the Foundry Agent Playground.
2. Agent 1 (Orchestrator) delegates policy/docs work to Agent 3 (Connected Agent).
3. Agent 3 calls the MCP Docs Server tool endpoints.
4. MCP Docs Server queries Azure AI Search and returns snippets + sources.
5. Agent response is composed using retrieved sources and returned to the chat UI.
