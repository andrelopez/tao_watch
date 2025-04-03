import pytest
from typing import Any, Dict, Optional
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.services.redis_cache import RedisCache

client = TestClient(app)

# Test data constants
VALID_HOTKEY = "5FFApaS75bv5pJHfAp2FVLBj9ZaXuFDjEypsaBNc1wCfe52v"
VALID_NETUID = 1
MOCK_DIVIDEND = 1000000.0
TAO_DIVIDENDS_ENDPOINT = "/api/v1/tao_dividends"

@pytest.fixture
def mock_bittensor_client():
    """Mock the BittensorClient for testing."""
    with patch("app.core.dependencies.BittensorClient") as mock:
        mock_instance = AsyncMock()
        mock_instance.get_tao_dividends.return_value = MOCK_DIVIDEND
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_redis_cache():
    """Create a mock Redis cache that always misses."""
    cache = AsyncMock(spec=RedisCache)
    cache.get.return_value = None
    cache.set.return_value = True
    return cache

def test_get_tao_dividends_unauthorized():
    """Test tao dividends endpoint without authentication."""
    response = make_tao_dividends_request()
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers


def test_get_tao_dividends_success(mock_bittensor_client, mock_redis_cache):
    """Test tao dividends endpoint with valid authentication."""
    # Ensure cache miss
    mock_redis_cache.get.return_value = None
    
    response = make_tao_dividends_request(token=settings.API_TOKEN)
    assert response.status_code == 200
    
    data = response.json()
    assert_valid_tao_response(data)
    mock_bittensor_client.get_tao_dividends.assert_called_once_with(
        VALID_NETUID,
        VALID_HOTKEY
    )


def test_get_tao_dividends_invalid_netuid(mock_bittensor_client):
    """Test tao dividends endpoint with invalid netuid."""
    response = make_tao_dividends_request(
        netuid="invalid",
        token=settings.API_TOKEN
    )
    assert response.status_code == 422
    mock_bittensor_client.get_tao_dividends.assert_not_called()


def test_get_tao_dividends_invalid_hotkey(mock_bittensor_client):
    """Test tao dividends endpoint with invalid hotkey."""
    response = make_tao_dividends_request(
        hotkey="invalid",
        token=settings.API_TOKEN
    )
    assert response.status_code == 422
    mock_bittensor_client.get_tao_dividends.assert_not_called()


def assert_valid_tao_response(data: Dict[str, Any]) -> None:
    """
    Helper function to assert the structure and content of a tao dividends response.
    
    Args:
        data: The response data to validate
    """
    assert data["netuid"] == VALID_NETUID
    assert data["hotkey"] == VALID_HOTKEY
    assert isinstance(data["dividend"], float)
    assert data["dividend"] == float(MOCK_DIVIDEND)
    assert isinstance(data["cached"], bool)
    assert isinstance(data["stake_tx_triggered"], bool)

def make_tao_dividends_request(
    netuid: int = VALID_NETUID,
    hotkey: str = VALID_HOTKEY,
    token: Optional[str] = None
) -> Any:
    """
    Helper function to make a request to the tao_dividends endpoint.
    
    Args:
        netuid: The subnet ID
        hotkey: The hotkey (account ID or public key)
        token: Optional authorization token
        
    Returns:
        Response from the API
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return client.get(
        TAO_DIVIDENDS_ENDPOINT,
        params={"netuid": netuid, "hotkey": hotkey},
        headers=headers
    )