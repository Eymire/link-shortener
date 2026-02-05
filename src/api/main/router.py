from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from src.cache import cache_storage
from src.dependencies import session_dep

from . import services


router = APIRouter()


@router.get('/{short_code}')
async def redirect_to_original_link(
    session: session_dep,
    short_code: str,
):
    if result := await cache_storage.get(short_code):
        return RedirectResponse(url=result)

    result = await services.get_original_link(
        session,
        short_code,
    )

    await cache_storage.set(short_code, result)

    return RedirectResponse(url=result)
