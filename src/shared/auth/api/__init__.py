from fastapi import APIRouter

from .v1 import router as v1

router = APIRouter(prefix="/auth", tags=["Auth"])
router.include_router(v1)
