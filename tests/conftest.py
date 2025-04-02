import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.main import app as fastapi_app

# Set test environment
os.environ["ENVIRONMENT"] = "test"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def app() -> FastAPI:
    """Create a FastAPI app instance for testing."""
    return fastapi_app


@pytest.fixture
async def async_client(app: FastAPI) -> AsyncClient:
    """Create an async HTTP client for testing the FastAPI app."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client 