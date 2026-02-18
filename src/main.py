import dotenv
import uvicorn

from src.core.settings.startup import StartupSettings


if __name__ == "__main__":
    dotenv.load_dotenv()
    settings = StartupSettings()
    uvicorn.run(
        factory=True,
        app=settings.ENTRY_POINT,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=False,
        workers=None,
    )
