# routes/health_route.py

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthStatus(BaseModel):
    status: str
    version: str

@router.get(
    "/healthCheck",
    response_model=HealthStatus,
    tags=["Health"],
    summary="Health check endpoint",
    description="Returns the current health status and app version.",
    responses={
        200: {"description": "Service health status"},
        500: {"description": "Internal server error"},
    },
)
def health_check():
    return HealthStatus(status="healthy", version="1.0.0")
