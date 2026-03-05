from pydantic import EmailStr

from src.presentation.taskiq_event.base.schemas import BaseSchemaOrigin


class RegistrationTaskSchema(BaseSchemaOrigin):
    email: EmailStr
    confirmation_code: str
