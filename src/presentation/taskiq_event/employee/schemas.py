from pydantic import EmailStr
from uuid6 import UUID

from src.presentation.taskiq_event.base.schemas import BaseSchemaOrigin


class RegistrationTaskSchema(BaseSchemaOrigin):
    employee_id: UUID
    email: EmailStr
