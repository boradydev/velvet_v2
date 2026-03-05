from fastapi import APIRouter, status

from src.presentation.fastapi.common.schemas import NullDataResponse
from src.presentation.fastapi.employees import controllers
from src.presentation.fastapi.employees.docs.registry import docs_registry


employees_public_router = APIRouter(
    prefix="/employees",
    tags=["Авторизация и аутентификация пользователя"],
)

employees_public_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    description=docs_registry.get(filename="docs/register.md"),
    response_model=NullDataResponse,
    responses={},
)(controllers.register_employee)


employees_public_router.post(
    "/resend",
    status_code=status.HTTP_200_OK,
    description=docs_registry.get(filename="docs/resend.md"),
    response_model=NullDataResponse,
    responses={},
)(controllers.resend_confirmation_code)
