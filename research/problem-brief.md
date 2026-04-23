# Problem Brief

## What the research converged on

The strongest cross-source signal is that businesses do not just want a chatbot. They want a system that:

- answers from trusted business knowledge
- remembers the current thread of work
- can decide when to answer, ask for clarification, capture a lead, or escalate
- works across many business types without a full rebuild

## Source highlights

### Google-indexed sources

- [Techment: 10 RAG Architectures in 2026](https://www.techment.com/blogs/rag-architectures-enterprise-use-cases-2026/) argues that hybrid, graph, self-RAG, and agentic RAG patterns are increasingly enterprise infrastructure rather than novelty features.
- [Progress Agentic RAG use cases](https://www.progress.com/agentic-rag/use-cases) shows wide applicability across enterprise search, site search, support, and multiple content formats.
- [Search.co on enterprise RAG use cases](https://search.co/blog/rag-use-cases-enterprise-data-analysis) emphasizes repeatable business question-answering grounded in enterprise data rather than generic chat.
- [Lookio on RAG for business use cases](https://lookio.app/blog/rag-business-use-cases.html) highlights internal knowledge and support workflows where RAG removes reliance on a few experts.

### Reddit production discussions

- [AI Agents and RAG: How Production AI Actually Works](https://www.reddit.com/r/Rag/comments/1r2oj3m/ai_agents_and_rag_how_production_ai_actually_works/) stresses that retrieval failure and stale context are often the real production failure points.
- [Chatbots Without RAG Are Just Guessing](https://www.reddit.com/r/Rag/comments/1rf895s/chatbots_without_rag_are_just_guessing_heres_what/) highlights memory + RAG as the shift from generic Q&A to a usable business assistant.
- [Do companies actually use internal RAG / doc-chat in production?](https://www.reddit.com/r/Rag/comments/1qz1zad/do_companies_actually_use_internal_rag_docchat/) surfaces instrumentation, security, structured extraction, and approval/compliance as gating factors.
- [RAG looks simple until you try to build it in production](https://www.reddit.com/r/AI_Agents/comments/1s66awz/rag_looks_simple_until_you_try_to_build_it_in/) reinforces that data quality and retrieval structure matter more than flashy model selection.

### Coding Ninjas signal

- [Coding Ninjas GenAI + Multi-Agent Systems PDF](https://www.codingninjas.com/careercamp/wp-content/uploads/2025/07/final.pdf) explicitly combines:
  - building simple RAG pipelines
  - advanced RAG techniques
  - RAG evaluation and fallback strategies
  - AI agents and multi-agent systems
  - FastAPI orchestration
  - smart customer support chatbot systems

That combination maps closely to what businesses actually need: grounded retrieval, guardrails, orchestration, and a production-ready service layer.

## Design response in this repo

Instead of building one narrow chatbot for one industry, this starter provides:

- a broad 300+ vertical taxonomy for multi-business adaptability
- a local knowledge ingestion pipeline
- a hybrid retrieval layer
- an agentic decision layer with action types
- a frontend workspace that works as a support, sales, or internal knowledge assistant shell

## Important honesty note

This repo is based on a broad cross-source synthesis and is designed to support many business verticals. It does not claim a literal manually verified analysis of 300+ individual industries one by one. Instead, it encodes 300+ vertical labels and builds a flexible product that can be adapted to many sectors from one architecture.

