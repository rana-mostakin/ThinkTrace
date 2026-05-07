# Author: rana-mostakin
"""
ThinkTrace v1 — Database Layer
SQLite with full schema: users, sessions, knowledge_graph, schedule
"""

import sqlite3
import hashlib
import secrets
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any

DB_PATH = os.environ.get("THINKTRACE_DB", "thinktrace.db")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Create all tables if they don't exist."""
    conn = get_conn()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        email       TEXT    NOT NULL UNIQUE,
        password_hash TEXT  NOT NULL,
        salt        TEXT    NOT NULL,
        grade       TEXT    NOT NULL DEFAULT '',
        study_goal  TEXT    NOT NULL DEFAULT '',
        language    TEXT    NOT NULL DEFAULT 'English',
        created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS sessions (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        subject         TEXT    NOT NULL,
        topics_json     TEXT    NOT NULL DEFAULT '[]',
        messages_json   TEXT    NOT NULL DEFAULT '[]',
        gaps_json       TEXT    NOT NULL DEFAULT '[]',
        depth_reached   INTEGER NOT NULL DEFAULT 1,
        style           TEXT    NOT NULL DEFAULT 'unclear',
        created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS knowledge_graph (
        user_id     INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
        graph_json  TEXT    NOT NULL DEFAULT '{}',
        updated_at  TEXT    NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS schedule (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        concept         TEXT    NOT NULL,
        subject         TEXT    NOT NULL,
        next_review     TEXT    NOT NULL,
        strength        REAL    NOT NULL DEFAULT 0.5,
        interval_days   INTEGER NOT NULL DEFAULT 1,
        session_count   INTEGER NOT NULL DEFAULT 0
    );
    """)

    conn.commit()
    conn.close()


# ── AUTH ──────────────────────────────────────────────────────────────────────

def _hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode()).hexdigest()


def create_user(name: str, email: str, password: str,
                grade: str, study_goal: str, language: str) -> Optional[int]:
    """Create a new user. Returns user_id or None if email taken."""
    salt = secrets.token_hex(16)
    pw_hash = _hash_password(password, salt)
    try:
        conn = get_conn()
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (name, email, password_hash, salt, grade, study_goal, language) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, email.lower().strip(), pw_hash, salt, grade, study_goal, language)
        )
        user_id = c.lastrowid
        conn.commit()
        conn.close()

        # Initialize empty knowledge graph
        _init_knowledge_graph(user_id)
        return user_id
    except sqlite3.IntegrityError:
        return None


def authenticate(email: str, password: str) -> Optional[Dict]:
    """Authenticate user. Returns user dict or None."""
    conn = get_conn()
    c = conn.cursor()
    row = c.execute(
        "SELECT * FROM users WHERE email = ?",
        (email.lower().strip(),)
    ).fetchone()
    conn.close()

    if not row:
        return None
    expected = _hash_password(password, row["salt"])
    if expected != row["password_hash"]:
        return None
    return dict(row)


def get_user(user_id: int) -> Optional[Dict]:
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_user(user_id: int, **kwargs):
    allowed = {"name", "grade", "study_goal", "language"}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return
    sets = ", ".join(f"{k} = ?" for k in fields)
    vals = list(fields.values()) + [user_id]
    conn = get_conn()
    conn.execute(f"UPDATE users SET {sets} WHERE id = ?", vals)
    conn.commit()
    conn.close()


# ── SESSIONS ──────────────────────────────────────────────────────────────────

def create_session(user_id: int, subject: str, topics: List[str]) -> int:
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO sessions (user_id, subject, topics_json) VALUES (?, ?, ?)",
        (user_id, subject, json.dumps(topics))
    )
    sid = c.lastrowid
    conn.commit()
    conn.close()
    return sid


def update_session(session_id: int, **kwargs):
    """Update session fields. messages/gaps/topics can be passed as lists."""
    updates = {}
    for k, v in kwargs.items():
        if k in ("messages", "gaps", "topics"):
            updates[f"{k}_json"] = json.dumps(v)
        elif k in ("depth_reached", "style"):
            updates[k] = v
    if not updates:
        return
    sets = ", ".join(f"{k} = ?" for k in updates)
    vals = list(updates.values()) + [session_id]
    conn = get_conn()
    conn.execute(f"UPDATE sessions SET {sets} WHERE id = ?", vals)
    conn.commit()
    conn.close()


def get_session(session_id: int) -> Optional[Dict]:
    conn = get_conn()
    row = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d["topics"] = json.loads(d["topics_json"])
    d["messages"] = json.loads(d["messages_json"])
    d["gaps"] = json.loads(d["gaps_json"])
    return d


def get_user_sessions(user_id: int, limit: int = 20) -> List[Dict]:
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM sessions WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit)
    ).fetchall()
    conn.close()
    result = []
    for row in rows:
        d = dict(row)
        d["topics"] = json.loads(d["topics_json"])
        d["messages"] = json.loads(d["messages_json"])
        d["gaps"] = json.loads(d["gaps_json"])
        result.append(d)
    return result


def get_user_stats(user_id: int) -> Dict:
    conn = get_conn()
    sessions = conn.execute(
        "SELECT * FROM sessions WHERE user_id = ?", (user_id,)
    ).fetchall()
    conn.close()

    total_sessions = len(sessions)
    total_gaps = 0
    repaired_gaps = 0
    cross_links = 0
    subjects_seen = set()

    for row in sessions:
        gaps = json.loads(row["gaps_json"])
        total_gaps += len(gaps)
        subjects_seen.add(row["subject"])

    # cross_links approximated
    cross_links = max(0, len(subjects_seen) - 1) * 2

    # Schedule gives us repaired count
    conn = get_conn()
    repaired = conn.execute(
        "SELECT COUNT(*) FROM schedule WHERE user_id = ? AND strength > 0.7",
        (user_id,)
    ).fetchone()[0]
    conn.close()

    return {
        "sessions": total_sessions,
        "gaps_found": total_gaps,
        "gaps_repaired": repaired,
        "cross_links": cross_links,
    }


# ── KNOWLEDGE GRAPH ───────────────────────────────────────────────────────────

def _init_knowledge_graph(user_id: int):
    conn = get_conn()
    conn.execute(
        "INSERT OR IGNORE INTO knowledge_graph (user_id, graph_json) VALUES (?, ?)",
        (user_id, json.dumps({"nodes": [], "edges": []}))
    )
    conn.commit()
    conn.close()


def get_knowledge_graph(user_id: int) -> Dict:
    _init_knowledge_graph(user_id)
    conn = get_conn()
    row = conn.execute(
        "SELECT graph_json FROM knowledge_graph WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()
    if not row:
        return {"nodes": [], "edges": []}
    return json.loads(row["graph_json"])


def update_knowledge_graph(user_id: int, graph: Dict):
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO knowledge_graph (user_id, graph_json, updated_at) "
        "VALUES (?, ?, datetime('now'))",
        (user_id, json.dumps(graph))
    )
    conn.commit()
    conn.close()


def upsert_graph_node(user_id: int, concept: str, subject: str,
                      strength_delta: float = 0.05, is_gap: bool = False):
    """Add or update a concept node in the knowledge graph."""
    graph = get_knowledge_graph(user_id)
    nodes = {n["id"]: n for n in graph.get("nodes", [])}

    if concept not in nodes:
        nodes[concept] = {
            "id": concept,
            "subject": subject,
            "strength": 0.3 if is_gap else 0.5,
            "session_count": 1,
            "is_gap": is_gap,
        }
    else:
        node = nodes[concept]
        node["session_count"] = node.get("session_count", 0) + 1
        if is_gap:
            node["strength"] = max(0.1, node.get("strength", 0.5) - 0.1)
            node["is_gap"] = True
        else:
            node["strength"] = min(1.0, node.get("strength", 0.5) + strength_delta)
            node["is_gap"] = node.get("strength", 0.5) < 0.3

    graph["nodes"] = list(nodes.values())
    update_knowledge_graph(user_id, graph)


def upsert_graph_edge(user_id: int, source: str, target: str, broken: bool = False):
    """Add or update a causal edge."""
    graph = get_knowledge_graph(user_id)
    edges = graph.get("edges", [])

    # Check if edge exists
    for edge in edges:
        if edge["source"] == source and edge["target"] == target:
            edge["broken"] = broken
            graph["edges"] = edges
            update_knowledge_graph(user_id, graph)
            return

    edges.append({"source": source, "target": target, "broken": broken})
    graph["edges"] = edges
    update_knowledge_graph(user_id, graph)


# ── SPACED REPETITION SCHEDULE ────────────────────────────────────────────────

def upsert_schedule(user_id: int, concept: str, subject: str,
                    strength: float = 0.5, is_gap: bool = True):
    """Add or update a scheduled review item."""
    interval = 1 if is_gap else 3
    next_review = (datetime.now() + timedelta(days=interval)).strftime("%Y-%m-%d")

    conn = get_conn()
    existing = conn.execute(
        "SELECT id, interval_days, strength, session_count FROM schedule "
        "WHERE user_id = ? AND concept = ?",
        (user_id, concept)
    ).fetchone()

    if existing:
        # SM-2 simplified: if strength improved, increase interval
        old_interval = existing["interval_days"]
        if strength > existing["strength"]:
            new_interval = min(old_interval * 2, 60)
        else:
            new_interval = max(1, old_interval // 2)
        new_next = (datetime.now() + timedelta(days=new_interval)).strftime("%Y-%m-%d")
        conn.execute(
            "UPDATE schedule SET strength=?, interval_days=?, next_review=?, session_count=session_count+1 "
            "WHERE id=?",
            (strength, new_interval, new_next, existing["id"])
        )
    else:
        conn.execute(
            "INSERT INTO schedule (user_id, concept, subject, next_review, strength, interval_days) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, concept, subject, next_review, strength, interval)
        )

    conn.commit()
    conn.close()


def get_due_reviews(user_id: int, limit: int = 10) -> List[Dict]:
    """Get concepts due for review (today or overdue)."""
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM schedule WHERE user_id = ? AND next_review <= ? "
        "ORDER BY next_review ASC LIMIT ?",
        (user_id, today, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_schedule(user_id: int) -> List[Dict]:
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM schedule WHERE user_id = ? ORDER BY next_review ASC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
