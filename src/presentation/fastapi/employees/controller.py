from typing import Annotated

from fastapi import Depends

from src.application.employees.dto import CredentialsEmployeeDTO
from src.application.employees.interactors import RegisterInteractor
from src.presentation.fastapi.base.schemas import NullDataResponse
from src.presentation.fastapi.employees import dependencies as deps
from src.presentation.fastapi.employees.schemas import RegisterRequest


async def register(
    data: RegisterRequest,
    interactor: Annotated[RegisterInteractor, Depends(deps.get_register_interactor)],
) -> NullDataResponse:
    await interactor.register(
        CredentialsEmployeeDTO(
            email=data.email,
            password=str(data.password),
        )
    )
    return NullDataResponse()
