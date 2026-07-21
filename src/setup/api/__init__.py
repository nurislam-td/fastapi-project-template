from fastapi import APIRouter

from shared.auth.api import router as auth_router

router = APIRouter()
router.include_router(auth_router)
