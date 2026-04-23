from __future__ import annotations

from .db import clear_all_data, count_rows, create_document, create_chunks
from .ingest import chunk_text


DEMO_DOCUMENTS = [
    {
        "title": "General Business Support Playbook",
        "vertical": "b2b-saas",
        "source_type": "seed",
        "content": """
        Support agents should answer using the company knowledge base first, cite policy where possible, and escalate billing or legal issues to a human.
        When a visitor requests pricing or demos, the chatbot should collect name, email, company, and use case before offering follow-up.
        If the user asks for a refund or cancellation, the assistant should explain the standard policy and provide a human handoff when exceptions may apply.
        """
    },
    {
        "title": "Retail Return and Shipping Policy",
        "vertical": "apparel-stores",
        "source_type": "seed",
        "content": """
        Standard returns are allowed within 30 days if the item is unused and in original packaging.
        Exchanges are supported for size and color variants when stock is available.
        Orders above $100 qualify for free shipping in domestic regions, while international delivery times vary by customs clearance.
        """
    },
    {
        "title": "Healthcare Scheduling and Compliance Notes",
        "vertical": "hospitals",
        "source_type": "seed",
        "content": """
        The assistant must not provide medical diagnosis or treatment advice.
        It can help patients understand appointment scheduling, insurance document requirements, clinic hours, and what records to bring.
        Any urgent symptom discussion must be escalated immediately to a licensed professional or emergency guidance workflow.
        """
    },
    {
        "title": "Real Estate Lead Qualification Guide",
        "vertical": "residential-brokerages",
        "source_type": "seed",
        "content": """
        For homebuyer inquiries, capture the target area, budget range, financing status, and buying timeline before scheduling an agent callback.
        For seller leads, capture the property type, location, expected listing timeline, and whether a valuation is requested.
        """
    },
    {
        "title": "Universal RAG Assistant Guardrails",
        "vertical": "b2b-saas",
        "source_type": "seed",
        "content": """
        The assistant should never fabricate policy, contract, pricing, regulatory, or legal details.
        When retrieval confidence is weak, it should ask a clarifying question or say that more documents are required.
        It should include citations for important operational or policy answers, and trigger escalation for human review when the issue is sensitive.
        """
    },
]


def seed_demo_workspace(workspace_id: str = "demo-workspace") -> dict[str, int]:
    clear_all_data()
    for document in DEMO_DOCUMENTS:
        document_id = create_document(
            workspace_id=workspace_id,
            title=document["title"],
            vertical=document["vertical"],
            source_type=document["source_type"],
            content=document["content"].strip(),
        )
        chunks = [
            (index, chunk, {"title": document["title"], "vertical": document["vertical"]})
            for index, chunk in enumerate(chunk_text(document["content"].strip()))
        ]
        create_chunks(document_id, workspace_id, document["vertical"], chunks)

    return {
        "documents": count_rows("documents"),
        "chunks": count_rows("chunks"),
    }

