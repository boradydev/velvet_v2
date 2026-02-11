from typing import Annotated

from fastapi import Depends

from src.application.employees import interactors
from src.presentation.fastapi.base.dependencies import AppResources, get_resources


def get_register_interactor(
    res: Annotated[AppResources, Depends(get_resources)],
) -> interactors.RegisterInteractor:
    return res.interactors.employees.create_register_interactor()
