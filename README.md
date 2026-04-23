# Omni RAG Agent Studio

Omni RAG Agent Studio is a standalone starter repo for building a business-grade RAG AI chatbot with an agentic orchestration layer. It combines a Python/FastAPI backend, a Tailwind-powered JavaScript frontend, a 300+ vertical business taxonomy, document ingestion, hybrid retrieval, memory-aware chat, and structured business actions such as lead capture and escalation.

## Why this repo exists

Across recent Google-indexed industry writeups, Reddit production discussions, and Coding Ninjas curriculum references, the same pattern shows up:

- businesses want grounded answers based on their own knowledge
- they also want agentic behavior, not a static FAQ bot
- production failures usually come from stale data, weak retrieval, poor controls, and missing memory rather than from "not enough model intelligence"

This repo is designed to be a practical starting point for many business types, not a niche one-off demo.

## What ships in v1

- Python FastAPI backend with SQLite persistence
- Hybrid lexical retrieval over uploaded knowledge
- Agentic planner for answer, clarify, lead capture, and escalation flows
- 300+ vertical taxonomy generator for broad business coverage
- Seeded demo knowledge for multiple business scenarios
- Vite + React + Tailwind dashboard for workspace, chat, upload, and vertical browsing
- Research brief documenting the product rationale

## Repo layout

```text
omni-rag-agent-studio/
  apps/
    api/       FastAPI RAG + agentic backend
    web/       React + Tailwind frontend
  research/    source-backed product rationale
```

## Quick start

### Backend

1. `cd apps/api`
2. `python -m venv .venv`
3. `.venv\\Scripts\\activate`
4. `pip install -r requirements.txt`
5. `uvicorn app.main:app --reload --port 4300`

### Frontend

1. `cd apps/web`
2. `npm install`
3. `npm run dev`
4. Open `http://localhost:5173`

The frontend expects the API at `http://localhost:4300` by default.

## Core API

- `GET /health`
- `GET /verticals`
- `GET /stats`
- `POST /seed-demo`
- `GET /documents`
- `POST /documents/import`
- `POST /documents/upload`
- `POST /chat`
- `GET /conversations/{conversation_id}`

## Product shape

This starter is meant for businesses that need:

- customer support grounded in internal docs
- product, policy, or pricing assistants
- internal knowledge copilots
- lead-qualification and handoff flows
- multi-vertical adaptability without rebuilding the stack

## Research

See [research/problem-brief.md](research/problem-brief.md) for the source synthesis from Google results, Reddit production discussions, and Coding Ninjas course material related to RAG, advanced RAG, evaluation, FastAPI orchestration, and AI agents.
