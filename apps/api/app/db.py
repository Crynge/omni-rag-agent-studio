from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, UTC
from threading import Lock

from .config import DB_PATH

_SCHEMA_LOCK = Lock()
_SCHEMA_READY = False


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def db_cursor():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    finally:
        connection.close()


def initialize_database() -> None:
    global _SCHEMA_READY
    if _SCHEMA_READY:
        return

    with _SCHEMA_LOCK:
        if _SCHEMA_READY:
            return

        with db_cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workspace_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    vertical TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_id INTEGER NOT NULL,
                    workspace_id TEXT NOT NULL,
                    vertical TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    metadata_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(document_id) REFERENCES documents(id)
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workspace_id TEXT NOT NULL,
                    vertical TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    citations_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(conversation_id) REFERENCES conversations(id)
                )
                """
            )
        _SCHEMA_READY = True


def count_rows(table: str) -> int:
    initialize_database()
    with db_cursor() as cursor:
        row = cursor.execute(f"SELECT COUNT(*) AS count FROM {table}").fetchone()
        return int(row["count"])


def create_document(workspace_id: str, title: str, vertical: str, source_type: str, content: str) -> int:
    initialize_database()
    with db_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO documents (workspace_id, title, vertical, source_type, content, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (workspace_id, title, vertical, source_type, content, utc_now()),
        )
        return int(cursor.lastrowid)


def create_chunks(document_id: int, workspace_id: str, vertical: str, chunks: list[tuple[int, str, dict[str, object]]]) -> None:
    initialize_database()
    with db_cursor() as cursor:
        cursor.executemany(
            """
            INSERT INTO chunks (document_id, workspace_id, vertical, chunk_index, text, metadata_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (document_id, workspace_id, vertical, chunk_index, text, json.dumps(metadata), utc_now())
                for chunk_index, text, metadata in chunks
            ],
        )


def list_documents() -> list[sqlite3.Row]:
    initialize_database()
    with db_cursor() as cursor:
        rows = cursor.execute(
            """
            SELECT id, workspace_id, title, vertical, source_type, created_at
            FROM documents
            ORDER BY id DESC
            """
        ).fetchall()
        return list(rows)


def list_chunks(workspace_id: str, vertical: str | None = None) -> list[sqlite3.Row]:
    initialize_database()
    with db_cursor() as cursor:
        if vertical:
            rows = cursor.execute(
                """
                SELECT c.id, c.document_id, c.workspace_id, c.vertical, c.chunk_index, c.text, c.metadata_json, d.title
                FROM chunks c
                JOIN documents d ON d.id = c.document_id
                WHERE c.workspace_id = ? AND c.vertical = ?
                ORDER BY c.id DESC
                """,
                (workspace_id, vertical),
            ).fetchall()
        else:
            rows = cursor.execute(
                """
                SELECT c.id, c.document_id, c.workspace_id, c.vertical, c.chunk_index, c.text, c.metadata_json, d.title
                FROM chunks c
                JOIN documents d ON d.id = c.document_id
                WHERE c.workspace_id = ?
                ORDER BY c.id DESC
                """,
                (workspace_id,),
            ).fetchall()
        return list(rows)


def create_conversation(workspace_id: str, vertical: str) -> int:
    initialize_database()
    with db_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO conversations (workspace_id, vertical, created_at)
            VALUES (?, ?, ?)
            """,
            (workspace_id, vertical, utc_now()),
        )
        return int(cursor.lastrowid)


def create_message(conversation_id: int, role: str, content: str, citations: list[dict[str, object]]) -> None:
    initialize_database()
    with db_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO messages (conversation_id, role, content, citations_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (conversation_id, role, content, json.dumps(citations), utc_now()),
        )


def get_conversation_messages(conversation_id: int) -> list[sqlite3.Row]:
    initialize_database()
    with db_cursor() as cursor:
        rows = cursor.execute(
            """
            SELECT id, role, content, citations_json, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
            """,
            (conversation_id,),
        ).fetchall()
        return list(rows)


def clear_all_data() -> None:
    initialize_database()
    with db_cursor() as cursor:
        cursor.execute("DELETE FROM messages")
        cursor.execute("DELETE FROM conversations")
        cursor.execute("DELETE FROM chunks")
        cursor.execute("DELETE FROM documents")
