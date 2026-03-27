import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from .tools.search_docs import search_docs_impl
from .tools.create_change_request import create_change_request_impl

load_dotenv()

app = FastAPI(title="MCP Docs Server", version="0.1.0")


class SearchDocsRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(5, ge=1, le=20)


class SearchDocsResult(BaseModel):
    title: str
    snippet: str
    source: str
    score: float | None = None


class SearchDocsResponse(BaseModel):
    results: list[SearchDocsResult]


class CreateChangeRequestRequest(BaseModel):
    title: str = Field(..., min_length=3)
    summary: str = Field(..., min_length=5)
    risk_level: str = Field(..., pattern="^(low|medium|high)$")
    steps: list[str] = Field(..., min_length=1)
    rollback_plan: str = Field(..., min_length=5)
    approvers: list[str] | None = None


class CreateChangeRequestResponse(BaseModel):
    id: str
    status: str
    location: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tools")
def list_tools():
    return {
        "tools": [
            {"name": "search_docs", "method": "POST", "path": "/tools/search_docs"},
            {"name": "create_change_request", "method": "POST", "path": "/tools/create_change_request"},
        ]
    }


@app.post("/tools/search_docs", response_model=SearchDocsResponse, operation_id="search_docs")
def search_docs(req: SearchDocsRequest):
    try:
        results = search_docs_impl(query=req.query, top_k=req.top_k)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/create_change_request", response_model=CreateChangeRequestResponse, operation_id="create_change_request")
def create_change_request(req: CreateChangeRequestRequest):
    try:
        out = create_change_request_impl(
            title=req.title,
            summary=req.summary,
            risk_level=req.risk_level,
            steps=req.steps,
            rollback_plan=req.rollback_plan,
            approvers=req.approvers,
        )
        return out
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
