import secrets
from contextlib import suppress
from datetime import UTC, datetime, timedelta
from string import ascii_letters, digits

from fastapi import HTTPException, status
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.cache import cache_storage
from src.models import Link as LinkModel
from src.settings import app_settings

from .schemas import LinkAdd as LinkAddSchema


async def add_short_link(
    session: AsyncSession,
    data: LinkAddSchema,
) -> LinkModel:
    while True:
        short_code = ''.join(
            secrets.choice(ascii_letters + digits) for _ in range(app_settings.link_length)
        )
        stmt = select(LinkModel).where(LinkModel.short_code == short_code)
        result = await session.execute(stmt)
        result = result.scalar_one_or_none()

        if result is None:
            break

    stmt = (
        insert(LinkModel)
        .values(
            url=str(data.url),
            short_code=short_code,
            expires_at=datetime.now(UTC) + timedelta(days=app_settings.link_lifetime_days),
        )
        .returning(LinkModel)
    )
    result = await session.execute(stmt)
    result = result.scalar_one()
    await session.commit()

    return result


async def remove_short_link(
    session: AsyncSession,
    short_code: str,
):
    stmt = select(LinkModel).where(LinkModel.short_code == short_code)
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Link not found',
        )

    stmt = delete(LinkModel).where(LinkModel.short_code == short_code)
    await session.execute(stmt)
    await session.commit()

    with suppress(Exception):
        await cache_storage.delete(short_code)
