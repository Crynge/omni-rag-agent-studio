from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_vertical_catalog_has_300_plus_entries():
    response = client.get("/verticals")
    assert response.status_code == 200
    assert response.json()["count"] >= 300


def test_seed_demo_and_stats():
    seed_response = client.post("/seed-demo")
    assert seed_response.status_code == 200
    stats = client.get("/stats")
    assert stats.status_code == 200
    payload = stats.json()
    assert payload["document_count"] >= 5
    assert payload["chunk_count"] >= 5


def test_import_and_chat_flow():
    import_response = client.post(
        "/documents/import",
        json={
            "workspace_id": "demo-workspace",
            "title": "SaaS Pricing Notes",
            "vertical": "b2b-saas",
            "content": "Starter plan begins at $49 per seat and enterprise pricing requires a sales consultation with implementation scoping.",
            "source_type": "manual"
        },
    )
    assert import_response.status_code == 200

    chat_response = client.post(
        "/chat",
        json={
            "workspace_id": "demo-workspace",
            "vertical": "b2b-saas",
            "message": "Can you explain pricing and arrange a demo?"
        },
    )
    assert chat_response.status_code == 200
    payload = chat_response.json()
    assert payload["intent"] == "lead_capture"
    assert len(payload["actions"]) >= 1
    assert len(payload["citations"]) >= 1


def test_conversation_endpoint_returns_messages():
    chat_response = client.post(
        "/chat",
        json={
            "workspace_id": "demo-workspace",
            "vertical": "apparel-stores",
            "message": "What is the return policy?"
        },
    )
    conversation_id = chat_response.json()["conversation_id"]
    detail_response = client.get(f"/conversations/{conversation_id}")
    assert detail_response.status_code == 200
    assert len(detail_response.json()["messages"]) >= 2


def test_upload_document_flow():
    upload_response = client.post(
        "/documents/upload",
        data={
            "workspace_id": "demo-workspace",
            "vertical": "apparel-stores",
            "title": "Hotel Concierge Notes",
        },
        files={
            "file": ("concierge.txt", b"Check-in begins at 3 PM. Concierge can arrange airport transfers.", "text/plain")
        },
    )
    assert upload_response.status_code == 200
    assert upload_response.json()["chunk_count"] >= 1
