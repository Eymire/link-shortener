from fastapi import APIRouter, status

from src.dependencies import session_dep

from . import services
from .schemas import LinkAdd as LinkAddSchema
from .schemas import LinkOut as LinkOutSchema


router = APIRouter()


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
)
async def add_short_link(
    session: session_dep,
    data: LinkAddSchema,
) -> LinkOutSchema:
    result = await services.add_short_link(
        session,
        data,
    )

    return result


@router.delete(
    '/{short_code}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_short_link(
    session: session_dep,
    short_code: str,
):
    await services.remove_short_link(
        session,
        short_code,
    )
