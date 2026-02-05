from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from src.dependencies import session_dep

from . import services


router = APIRouter()


@router.get('/{short_code}')
async def redirect_to_original_link(
    session: session_dep,
    short_code: str,
):
    result = await services.get_original_link(
        session,
        short_code,
    )

    return RedirectResponse(url=result)
