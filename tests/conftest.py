import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient


load_dotenv(".env.test")
from src.presentation.fastapi.app import fastapi_app  # noqa: E402


@pytest.fixture
async def client():
    """Фикстура для асинхронных HTTP-запросов."""
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app()), base_url="http://test"
    ) as ac:
        yield ac
