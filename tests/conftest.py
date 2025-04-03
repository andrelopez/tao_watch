import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from unittest.mock import AsyncMock

from app.main import create_application
from app.core.dependencies import get_bittensor_client, get_redis_cache
from app.services.bittensor_client import BittensorClient
from app.services.redis_cache import RedisCache

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
    return create_application()


@pytest.fixture
async def async_client(app: FastAPI) -> AsyncClient:
    """Create an async HTTP client for testing the FastAPI app."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client 


@pytest.fixture
def mock_bittensor_client():
    """Create a mock BittensorClient."""
    mock_instance = AsyncMock(spec=BittensorClient)
    mock_instance.get_tao_dividends.return_value = 1000000.0
    return mock_instance


@pytest.fixture
def mock_redis_cache():
    """Create a mock Redis cache that always misses."""
    cache = AsyncMock(spec=RedisCache)
    cache.get.return_value = None
    cache.set.return_value = True
    return cache


def override_dependencies(app: FastAPI, mock_client: AsyncMock, mock_cache: AsyncMock) -> None:
    """Override FastAPI dependencies for testing."""
    app.dependency_overrides[get_bittensor_client] = lambda: mock_client
    app.dependency_overrides[get_redis_cache] = lambda: mock_cache


@pytest.fixture(autouse=True)
def setup_test_dependencies(app: FastAPI, mock_bittensor_client: AsyncMock, mock_redis_cache: AsyncMock):
    """Setup test dependencies and cleanup."""
    app.dependency_overrides[get_bittensor_client] = lambda: mock_bittensor_client
    app.dependency_overrides[get_redis_cache] = lambda: mock_redis_cache
    yield
    app.dependency_overrides.clear() 