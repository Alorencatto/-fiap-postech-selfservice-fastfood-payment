from fastapi import APIRouter

from src.external.web.fastapi.api_v2.endpoints import (
    payment
)

router = APIRouter()


@router.get("/")
async def read_root():
    return {"message": "Alive"}


router.include_router(payment.router)
