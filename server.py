"""roadtrip-memory — a memory for the places worth stopping again.

Built on your-first-memory: one table, two tools, and the places you
loved on the road survive the end of the conversation. See docs/adr/
for every choice made here — each one records a real decision with the
road not taken.
"""
import os
from mcp.server.fastmcp import FastMCP

import psycopg

# .strip(): a value pasted into a dashboard can carry a stray newline or
# space, which libpq would treat as part of the URL (ADR-0005).
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

mcp = FastMCP(
    "your-first-memory",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8000)),
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS favorites (
    id          SERIAL PRIMARY KEY,
    place       TEXT NOT NULL,
    reason      TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()  -- TIMESTAMPTZ, never ambiguous about its timezone (ADR-0004)
);
"""


def db():
    """One connection per tool call (ADR-0002): Neon's free tier suspends
    when idle, and a fresh connection wakes it transparently. A held pool
    would die during the nap and greet you with a stale-connection error."""
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. Not an error in the code — a feature "
            "waiting for setup: create a free database at neon.tech, copy the "
            "connection string, and set it as an environment variable "
            "(COURSE-STEPS.md, step 2)."
        )
    conn = psycopg.connect(DATABASE_URL)
    with conn.cursor() as cur:
        cur.execute(SCHEMA)
    conn.commit()
    return conn


@mcp.tool()
def save_favorite(place: str, reason: str) -> str:
    """Save a road-trip favorite: the place, and why it was worth it."""
    with db() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO favorites (place, reason) VALUES (%s, %s) RETURNING id, created_at",
            (place, reason),
        )
        fid, ts = cur.fetchone()
        conn.commit()
    return f"Saved as favorite #{fid} at {ts.isoformat()}."


@mcp.tool()
def list_favorites() -> str:
    """Every favorite in the memory, oldest first."""
    with db() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, place, reason, created_at FROM favorites ORDER BY id")
        rows = cur.fetchall()
    if not rows:
        return "No favorites yet. Save a place worth stopping again."
    lines = []
    for fid, place, reason, ts in rows:
        lines.append(f"#{fid} ({ts:%Y-%m-%d %H:%M}): {place} — {reason}")
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
