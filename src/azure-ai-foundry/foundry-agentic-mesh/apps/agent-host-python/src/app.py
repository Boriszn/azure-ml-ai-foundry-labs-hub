import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from foundry_run import run_single_turn

load_dotenv()

app = FastAPI(title="Agent Host (optional)", version="0.1.0")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    reply = run_single_turn(req.message)
    return {"reply": reply}
