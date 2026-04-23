from __future__ import annotations

import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .agent import build_chat_response, detect_intent
from .db import (
    count_rows,
    create_chunks,
    create_conversation,
    create_document,
    create_message,
    get_conversation_messages,
    initialize_database,
    list_documents,
)
from .ingest import chunk_text, parse_uploaded_content
from .retrieval import retrieve_relevant_chunks
from .schemas import ChatRequest, DocumentImportRequest, DocumentRecord, StatsResponse
from .seed import seed_demo_workspace
from .verticals import ALL_VERTICAL_COUNT, ALL_VERTICAL_PROFILES, VERTICAL_INDEX


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    if count_rows("documents") == 0:
        seed_demo_workspace()
    yield


app = FastAPI(title="Omni RAG Agent Studio API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/verticals")
def list_vertical_profiles(limit: int = 24) -> dict[str, object]:
    return {
        "count": ALL_VERTICAL_COUNT,
        "items": ALL_VERTICAL_PROFILES[:limit],
    }


@app.get("/stats", response_model=StatsResponse)
def stats() -> StatsResponse:
    return StatsResponse(
        workspace_count=1,
        document_count=count_rows("documents"),
        chunk_count=count_rows("chunks"),
        conversation_count=count_rows("conversations"),
        vertical_count=ALL_VERTICAL_COUNT,
    )


@app.post("/seed-demo")
def seed_demo() -> dict[str, object]:
    result = seed_demo_workspace()
    return {"ok": True, "seeded": result}


@app.get("/documents")
def documents() -> dict[str, list[DocumentRecord]]:
    return {
        "documents": [
            DocumentRecord(**dict(row))
            for row in list_documents()
        ]
    }


@app.post("/documents/import")
def import_document(payload: DocumentImportRequest) -> dict[str, object]:
    if payload.vertical not in VERTICAL_INDEX:
        raise HTTPException(status_code=400, detail="Unknown vertical slug.")

    document_id = create_document(
        workspace_id=payload.workspace_id,
        title=payload.title,
        vertical=payload.vertical,
        source_type=payload.source_type,
        content=payload.content,
    )
    chunks = [
        (index, chunk, {"title": payload.title, "vertical": payload.vertical})
        for index, chunk in enumerate(chunk_text(payload.content))
    ]
    create_chunks(document_id, payload.workspace_id, payload.vertical, chunks)
    return {"document_id": document_id, "chunk_count": len(chunks)}


@app.post("/documents/upload")
async def upload_document(
    workspace_id: str = Form(...),
    vertical: str = Form(...),
    title: str = Form(...),
    file: UploadFile = File(...),
) -> dict[str, object]:
    if vertical not in VERTICAL_INDEX:
        raise HTTPException(status_code=400, detail="Unknown vertical slug.")

    raw = await file.read()
    content = parse_uploaded_content(file.filename or "upload.txt", raw)
    if len(content.strip()) < 10:
        raise HTTPException(status_code=400, detail="Uploaded file does not contain enough usable text.")

    document_id = create_document(
        workspace_id=workspace_id,
        title=title,
        vertical=vertical,
        source_type="upload",
        content=content,
    )
    chunks = [
        (index, chunk, {"title": title, "vertical": vertical, "filename": file.filename or "upload"})
        for index, chunk in enumerate(chunk_text(content))
    ]
    create_chunks(document_id, workspace_id, vertical, chunks)
    return {"document_id": document_id, "chunk_count": len(chunks)}


@app.post("/chat")
def chat(payload: ChatRequest):
    if payload.vertical not in VERTICAL_INDEX:
        raise HTTPException(status_code=400, detail="Unknown vertical slug.")

    conversation_id = payload.conversation_id or create_conversation(payload.workspace_id, payload.vertical)
    create_message(conversation_id, "user", payload.message, [])

    history_rows = get_conversation_messages(conversation_id)
    memory_summary = " | ".join([f"{row['role']}: {row['content'][:60]}" for row in history_rows[-4:]])
    retrieved = retrieve_relevant_chunks(payload.workspace_id, payload.vertical, payload.message, payload.top_k)
    intent = detect_intent(payload.message)
    response = build_chat_response(conversation_id, intent, payload.message, payload.vertical, retrieved, memory_summary)

    create_message(
        conversation_id,
        "assistant",
        response.answer,
        [citation.model_dump() for citation in response.citations],
    )

    return response


@app.get("/conversations/{conversation_id}")
def conversation_detail(conversation_id: int) -> dict[str, object]:
    rows = get_conversation_messages(conversation_id)
    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "id": row["id"],
                "role": row["role"],
                "content": row["content"],
                "citations": json.loads(row["citations_json"]),
                "created_at": row["created_at"],
            }
            for row in rows
        ]
    }
