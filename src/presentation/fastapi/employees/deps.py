from typing import Annotated

from fastapi import Depends

from src.application.employees import interactors
from src.infrastructure.common.resources import LifespanState
from src.presentation.fastapi.common.common_deps import get_lifespan_state


def get_register_interactor(
    lifespan: Annotated[LifespanState, Depends(get_lifespan_state)],
) -> interactors.RegisterInteractor:
    return lifespan.interactors.employees.create_register_interactor()
