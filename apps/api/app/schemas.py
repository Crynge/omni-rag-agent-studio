from __future__ import annotations

from pydantic import BaseModel, Field


class VerticalProfile(BaseModel):
    slug: str
    name: str
    sector: str
    short_description: str
    common_use_cases: list[str]
    tone_guidance: str


class DocumentImportRequest(BaseModel):
    workspace_id: str = "demo-workspace"
    title: str
    vertical: str
    content: str = Field(min_length=10)
    source_type: str = "manual"


class DocumentRecord(BaseModel):
    id: int
    workspace_id: str
    title: str
    vertical: str
    source_type: str
    created_at: str


class Citation(BaseModel):
    chunk_id: int
    document_title: str
    snippet: str
    score: float


class AgentAction(BaseModel):
    type: str
    label: str
    payload: dict[str, str | int | float | bool | None]


class ChatRequest(BaseModel):
    workspace_id: str = "demo-workspace"
    vertical: str
    message: str = Field(min_length=2)
    conversation_id: int | None = None
    top_k: int = 4


class ChatResponse(BaseModel):
    conversation_id: int
    intent: str
    answer: str
    citations: list[Citation]
    actions: list[AgentAction]
    memory_summary: str


class StatsResponse(BaseModel):
    workspace_count: int
    document_count: int
    chunk_count: int
    conversation_count: int
    vertical_count: int


