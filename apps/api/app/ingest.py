from __future__ import annotations

import csv
import io
import json
from pathlib import Path


def chunk_text(text: str, chunk_size: int = 480, overlap: int = 80) -> list[str]:
    cleaned = " ".join(text.split())
    if len(cleaned) <= chunk_size:
        return [cleaned]

    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(len(cleaned), start + chunk_size)
        chunks.append(cleaned[start:end])
        if end >= len(cleaned):
            break
        start = max(end - overlap, 0)
    return chunks


def parse_uploaded_content(filename: str, payload: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    raw = payload.decode("utf-8", errors="ignore")

    if suffix in {".txt", ".md"}:
        return raw
    if suffix == ".json":
        parsed = json.loads(raw)
        return json.dumps(parsed, indent=2)
    if suffix == ".csv":
        reader = csv.DictReader(io.StringIO(raw))
        rows = list(reader)
        return json.dumps(rows, indent=2)

    return raw

