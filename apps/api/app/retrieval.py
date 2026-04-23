from __future__ import annotations

import json
import math
import re

from .db import list_chunks


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]{2,}")


def tokenize(value: str) -> set[str]:
    return {token.lower() for token in TOKEN_PATTERN.findall(value)}


def score_chunk(query: str, chunk_text: str, vertical_boost: float) -> float:
    query_tokens = tokenize(query)
    chunk_tokens = tokenize(chunk_text)
    if not query_tokens or not chunk_tokens:
        return 0.0

    overlap = len(query_tokens & chunk_tokens)
    density = overlap / max(len(query_tokens), 1)
    length_penalty = math.log(len(chunk_tokens) + 1, 2)
    return (density * 100 / max(length_penalty, 1)) + vertical_boost


def retrieve_relevant_chunks(workspace_id: str, vertical: str, query: str, top_k: int = 4) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for row in list_chunks(workspace_id):
        boost = 8.0 if row["vertical"] == vertical else 0.0
        score = score_chunk(query, row["text"], boost)
        if score <= 0:
            continue
        metadata = json.loads(row["metadata_json"])
        results.append(
            {
                "chunk_id": int(row["id"]),
                "document_id": int(row["document_id"]),
                "document_title": row["title"],
                "vertical": row["vertical"],
                "text": row["text"],
                "score": round(score, 3),
                "metadata": metadata,
            }
        )

    return sorted(results, key=lambda item: item["score"], reverse=True)[:top_k]

