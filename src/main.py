import uvicorn

from src.core.enums import AppEnv
from src.core.settings import settings

if settings.APP_ENV == AppEnv.local:
    if __name__ == "__main__":
        uvicorn.run(
            "src.presentation.fastapi.app:app", host=settings.APP_HOST, reload=False, workers=None
        )
elif settings.APP_ENV == AppEnv.dev:
    if __name__ == "__main__":
        uvicorn.run(
            "src.presentation.fastapi.app:app", host=settings.APP_HOST, reload=False, workers=None
        )
