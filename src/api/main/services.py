from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Link as LinkModel


async def get_original_link(
    session: AsyncSession,
    short_code: str,
) -> str:
    stmt = select(LinkModel).where(LinkModel.short_code == short_code)
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Link not found',
        )

    return result.original_url
