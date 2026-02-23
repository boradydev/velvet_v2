from fastapi import APIRouter, status

from src.presentation.fastapi.common.schemas import NullDataResponse
from src.presentation.fastapi.employees import controller
from src.presentation.fastapi.employees.descriptions.registry import docs_registry


employees_public_router = APIRouter(
    prefix="/employees",
    tags=["Авторизация и аутентификация пользователя"],
)

employees_public_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    description=docs_registry.get(filename="descriptions/register.md"),
    response_model=NullDataResponse,
    responses={},
)(controller.register_employee)


employees_public_router.post(
    "/resend",
    status_code=status.HTTP_200_OK,
    description=docs_registry.get(filename="descriptions/resend.md"),
    response_model=NullDataResponse,
    responses={},
)(controller.resend_confirmation_code)
