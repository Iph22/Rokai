# app/vector_memory.py
# ── Local SQLite fallback — no Supabase required ───────────
# Drop-in replacement. Same function signatures, zero cloud deps.
# Upgrade to Supabase/Chroma later when ready.

import sqlite3
import time

DB_PATH = "rokai_memory.db"

def _conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def _ensure_table():
    con = _conn()
    con.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            metadata TEXT DEFAULT '{}',
            created_at REAL NOT NULL
        )
    """)
    con.commit()
    con.close()

_ensure_table()


def store_memory(content: str, metadata: dict = None):
    import json
    try:
        con = _conn()
        con.execute(
            "INSERT INTO memories (content, metadata, created_at) VALUES (?, ?, ?)",
            (content, json.dumps(metadata or {}), time.time())
        )
        con.commit()
        con.close()
    except Exception as e:
        print(f"Memory store error: {e}")


def search_memories(query: str, limit: int = 5) -> list:
    """Simple keyword search — good enough for llama3 context injection."""
    try:
        con = _conn()
        words = query.lower().split()
        # Score each memory by how many query words it contains
        rows = con.execute(
            "SELECT content, metadata FROM memories ORDER BY created_at DESC LIMIT 100"
        ).fetchall()
        con.close()
        scored = []
        for content, meta in rows:
            score = sum(1 for w in words if w in content.lower())
            if score > 0:
                scored.append((score, {"content": content, "metadata": meta}))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:limit]]
    except Exception as e:
        print(f"Memory search error: {e}")
        return []


def get_recent_memories(limit: int = 10) -> list:
    try:
        con = _conn()
        rows = con.execute(
            "SELECT content, metadata FROM memories ORDER BY created_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
        con.close()
        return [{"content": r[0], "metadata": r[1]} for r in rows]
    except Exception as e:
        print(f"Memory fetch error: {e}")
        return []