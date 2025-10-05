"""User-related API routes."""

from typing import Annotated

from ab_core.database.session_context import db_session_async
from fastapi import APIRouter
from fastapi import Depends as FDepends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/hello", tags=["Hello World"])


@router.get("/world")
async def helloworld(
    _db_session: Annotated[AsyncSession, FDepends(db_session_async)],
):
    """Hello World."""
    return "Good-bye World."
