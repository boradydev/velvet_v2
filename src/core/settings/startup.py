import os
from dataclasses import dataclass

import dotenv


dotenv.load_dotenv()


@dataclass(frozen=True, slots=True)
class StartupSettings:
    ENTRY_POINT: str = os.environ["ENTRY_POINT"]
    APP_HOST: str = os.environ["APP_HOST"]
    APP_PORT: int = int(os.environ["APP_PORT"])
