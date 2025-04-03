import pytest
from typing import Any, Dict, Optional
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

# Test data constants
VALID_HOTKEY = "5FFApaS75bv5pJHfAp2FVLBj9ZaXuFDjEypsaBNc1wCfe52v"
VALID_NETUID = 1
TAO_DIVIDENDS_ENDPOINT = f"{settings.API_V1_STR}/tao_dividends"

def test_get_tao_dividends_unauthorized():
    """Test tao dividends endpoint without authentication."""
    response = make_tao_dividends_request()
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers


def test_get_tao_dividends_success():
    """Test tao dividends endpoint with valid authentication."""
    response = make_tao_dividends_request(token=settings.API_TOKEN)
    assert response.status_code == 200
    
    data = response.json()
    assert_valid_tao_response(data)


def test_get_tao_dividends_invalid_netuid():
    """Test tao dividends endpoint with invalid netuid."""
    response = make_tao_dividends_request(
        netuid=-1,
        token=settings.API_TOKEN
    )
    assert response.status_code == 422


def test_get_tao_dividends_invalid_hotkey():
    """Test tao dividends endpoint with invalid hotkey."""
    response = make_tao_dividends_request(
        hotkey="invalid",
        token=settings.API_TOKEN
    )
    assert response.status_code == 422


def assert_valid_tao_response(data: Dict[str, Any]) -> None:
    """
    Helper function to assert the structure and content of a tao dividends response.
    
    Args:
        data: The response data to validate
    """
    assert data["netuid"] == VALID_NETUID
    assert data["hotkey"] == VALID_HOTKEY
    assert isinstance(data["dividend"], int)
    assert data["cached"] is True
    assert data["stake_tx_triggered"] is True 

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