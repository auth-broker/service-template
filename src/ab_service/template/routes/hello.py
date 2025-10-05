"""User-related API routes."""

from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends as FDepends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ab_core.database.session_context import db_session_async

router = APIRouter(prefix="/hello", tags=["Hello World"])


@router.get("/world")
async def helloworld(
    db_session: Annotated[AsyncSession, FDepends(db_session_async)],
):
    """Hello World that touches the DB."""
    # Example 1: a trivial read (works on SQLite)
    res = await db_session.execute(text("SELECT 1 AS ok"))
    ok = res.scalar_one()

    # Example 2: create a tiny table and upsert a heartbeat row (id=1)
    # This runs in a transaction; SQLite will auto-commit on success.
    await db_session.execute(
        text("""
        CREATE TABLE IF NOT EXISTS heartbeat (
            id INTEGER PRIMARY KEY,
            last_seen TEXT NOT NULL
        )
        """)
    )
    await db_session.execute(
        text("""
        INSERT INTO heartbeat (id, last_seen)
        VALUES (1, datetime('now'))
        ON CONFLICT(id) DO UPDATE SET last_seen = excluded.last_seen
        """)
    )

    # Read it back
    row = await db_session.execute(
        text("SELECT id, last_seen FROM heartbeat WHERE id = 1")
    )
    id_, last_seen = row.one()

    return {
        "message": "Good-bye World.",
        "db_ok": ok,
        "heartbeat": {"id": id_, "last_seen": last_seen},
    }
