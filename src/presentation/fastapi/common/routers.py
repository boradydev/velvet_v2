from fastapi import APIRouter

from src.presentation.fastapi.employees.routers import employees_public_router


public = APIRouter(
    prefix="/public",
)

public.include_router(employees_public_router)

protected = APIRouter(
    prefix="/protected",
)
