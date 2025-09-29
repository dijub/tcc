from fastapi import APIRouter

from app.api.cliente import router as cliente_router

api_router = APIRouter()
api_router.include_router(cliente_router)

__all__ = ["api_router"]
