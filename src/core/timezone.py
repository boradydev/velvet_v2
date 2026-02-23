from datetime import UTC, datetime, timedelta
from typing import NewType


Timestamp = NewType("Timestamp", datetime)
Timedelta = NewType("Timedelta", timedelta)


def get_timestamp() -> Timestamp:
    """Единая точка получения текущего времени UTC."""
    return Timestamp(datetime.now(UTC))
