from dataclasses import dataclass

from uuid6 import UUID


@dataclass
class BaseEntity:
    id: UUID

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.id == other.id
