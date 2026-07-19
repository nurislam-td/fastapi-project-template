from fastapi import APIRouter

from .router import router as api

router = APIRouter(prefix="/v1")
router.include_router(api)
