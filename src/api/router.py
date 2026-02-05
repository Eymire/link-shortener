from fastapi import APIRouter

from src.api.links.router import router as links_router
from src.api.main.router import router as main_router


router = APIRouter()

router.include_router(
    main_router,
    prefix='',
    tags=['main'],
)
router.include_router(
    links_router,
    prefix='/links',
    tags=['links'],
)
