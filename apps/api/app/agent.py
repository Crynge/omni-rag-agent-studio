from __future__ import annotations

from .schemas import AgentAction, Citation, ChatResponse
from .verticals import VERTICAL_INDEX


def detect_intent(message: str) -> str:
    lowered = message.lower()
    if any(
        keyword in lowered
        for keyword in [
            "demo",
            "quote",
            "pricing",
            "contact sales",
            "call me",
            "contact me",
            "schedule",
            "book",
            "callback",
            "speak to",
            "talk to sales",
        ]
    ):
        return "lead_capture"
    if any(keyword in lowered for keyword in ["refund", "return", "policy", "compliance", "rules", "terms"]):
        return "policy_lookup"
    if any(keyword in lowered for keyword in ["human", "agent", "person", "support rep", "escalate"]):
        return "escalation"
    if any(keyword in lowered for keyword in ["how", "what", "when", "where", "can you", "help me"]):
        return "knowledge_answer"
    return "clarify"


def build_actions(intent: str, vertical: str) -> list[AgentAction]:
    actions: list[AgentAction] = []
    if intent == "lead_capture":
        actions.append(
            AgentAction(
                type="capture_contact",
                label="Capture contact details",
                payload={"required_fields": "name,email,company"},
            )
        )
        actions.append(
            AgentAction(
                type="book_followup",
                label="Offer a sales follow-up",
                payload={"vertical": vertical},
            )
        )
    elif intent == "escalation":
        actions.append(
            AgentAction(
                type="handoff",
                label="Escalate to a human agent",
                payload={"priority": "high"},
            )
        )
    elif intent == "policy_lookup":
        actions.append(
            AgentAction(
                type="cite_policy",
                label="Show source-backed policy answer",
                payload={"mode": "strict"},
            )
        )
    else:
        actions.append(
            AgentAction(
                type="clarify_if_needed",
                label="Ask a follow-up if context is weak",
                payload={"mode": "adaptive"},
            )
        )
    return actions


def build_answer(
    message: str,
    vertical: str,
    retrieved: list[dict[str, object]],
    memory_summary: str,
) -> tuple[str, list[Citation]]:
    profile = VERTICAL_INDEX.get(vertical)
    profile_name = profile["name"] if profile else vertical
    citations: list[Citation] = []

    if retrieved:
        for item in retrieved:
            citations.append(
                Citation(
                    chunk_id=int(item["chunk_id"]),
                    document_title=str(item["document_title"]),
                    snippet=str(item["text"][:180]) + ("..." if len(str(item["text"])) > 180 else ""),
                    score=float(item["score"]),
                )
            )

        context_lines = "\n".join([f"- {citation.document_title}: {citation.snippet}" for citation in citations[:3]])
        answer = (
            f"For {profile_name}, here's the grounded answer based on the current knowledge base.\n\n"
            f"{context_lines}\n\n"
            f"Based on those sources, the safest response is: {summarize_from_chunks(message, retrieved)}"
        )
    else:
        answer = (
            f"I don't have enough grounded knowledge yet for this {profile_name} question. "
            f"Upload more business documents or ask a narrower question so I can respond with citations instead of guessing."
        )

    if memory_summary:
        answer += f"\n\nConversation memory: {memory_summary}"
    return answer, citations


def summarize_from_chunks(message: str, retrieved: list[dict[str, object]]) -> str:
    combined = " ".join(str(item["text"]) for item in retrieved[:2])
    lowered = message.lower()
    if "price" in lowered or "pricing" in lowered:
        return f"the available material points to pricing, package, or quote details inside the retrieved docs: {combined[:240]}..."
    if "refund" in lowered or "return" in lowered:
        return f"the relevant policy and customer handling guidance appears in the retrieved docs: {combined[:240]}..."
    if "support" in lowered or "issue" in lowered:
        return f"the support workflow and resolution path appear to be: {combined[:240]}..."
    return f"the most relevant grounded context says: {combined[:260]}..."


def build_chat_response(
    conversation_id: int,
    intent: str,
    message: str,
    vertical: str,
    retrieved: list[dict[str, object]],
    memory_summary: str,
) -> ChatResponse:
    answer, citations = build_answer(message, vertical, retrieved, memory_summary)
    actions = build_actions(intent, vertical)
    return ChatResponse(
        conversation_id=conversation_id,
        intent=intent,
        answer=answer,
        citations=citations,
        actions=actions,
        memory_summary=memory_summary,
    )
