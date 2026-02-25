from fastapi import APIRouter
from src.api.v1.auth import router as auth_router
from src.api.v1.boards import router as boards_router
from src.api.v1.interactions import router as interactions_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(boards_router, prefix="/boards", tags=["boards"])
api_router.include_router(interactions_router, prefix="/interactions", tags=["ws"])
