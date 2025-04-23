# routes/home_route.py

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.get(
    "/",
    response_class=PlainTextResponse,
    tags=["Root"],
    summary="Home endpoint",
    description="Home page for gateway or any other temp FE",
    responses={200: {"description": "Service is up"}},
)
def home():
    return "ok"
