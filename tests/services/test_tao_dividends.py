import json
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.tao_dividends import TaoDividendsService
from app.api.v1.schemas.tao import TaoDividendsResponse

VALID_NETUID = 1
VALID_HOTKEY = "5FFApaS75bv5pJHfAp2FVLBj9ZaXuFDjEypsaBNc1wCfe52v"
MOCK_DIVIDEND = 1000.0

@pytest.fixture
def mock_bittensor_client():
    """Create a mock BittensorClient."""
    client = AsyncMock()
    client.get_tao_dividends = AsyncMock(return_value=MOCK_DIVIDEND)
    return client

@pytest.fixture
def mock_redis_cache():
    """Create a mock RedisCache."""
    cache = AsyncMock()
    cache.get = AsyncMock(return_value=None)
    cache.set = AsyncMock(return_value=True)
    return cache

@pytest.fixture
def service(mock_bittensor_client, mock_redis_cache):
    """Create a TaoDividendsService instance with mocks."""
    return TaoDividendsService(mock_bittensor_client, mock_redis_cache)

@pytest.mark.asyncio
async def test_get_dividends_cache_miss(service, mock_bittensor_client, mock_redis_cache):
    """Test getting dividends when not in cache."""
    # Execute
    response = await service.get_dividends(VALID_NETUID, VALID_HOTKEY)
    
    # Assert
    assert isinstance(response, TaoDividendsResponse)
    assert response.netuid == VALID_NETUID
    assert response.hotkey == VALID_HOTKEY
    assert response.dividend == MOCK_DIVIDEND
    assert response.cached is False
    
    # Verify cache interactions
    mock_redis_cache.get.assert_called_once_with(
        TaoDividendsService.CACHE_PREFIX,
        VALID_NETUID,
        VALID_HOTKEY
    )
    mock_redis_cache.set.assert_called_once()
    mock_bittensor_client.get_tao_dividends.assert_called_once_with(
        VALID_NETUID,
        VALID_HOTKEY
    )

@pytest.mark.asyncio
async def test_get_dividends_cache_hit(service, mock_bittensor_client, mock_redis_cache):
    """Test getting dividends when in cache."""
    # Setup cached response
    cached_data = {
        "netuid": VALID_NETUID,
        "hotkey": VALID_HOTKEY,
        "dividend": MOCK_DIVIDEND,
        "cached": True,
        "stake_tx_triggered": False
    }
    mock_redis_cache.get.return_value = json.dumps(cached_data)
    
    # Execute
    response = await service.get_dividends(VALID_NETUID, VALID_HOTKEY)
    
    # Assert
    assert isinstance(response, TaoDividendsResponse)
    assert response.netuid == VALID_NETUID
    assert response.hotkey == VALID_HOTKEY
    assert response.dividend == MOCK_DIVIDEND
    assert response.cached is True
    
    # Verify cache interactions
    mock_redis_cache.get.assert_called_once_with(
        TaoDividendsService.CACHE_PREFIX,
        VALID_NETUID,
        VALID_HOTKEY
    )
    mock_redis_cache.set.assert_not_called()
    mock_bittensor_client.get_tao_dividends.assert_not_called()

@pytest.mark.asyncio
async def test_get_dividends_cache_error(service, mock_bittensor_client, mock_redis_cache):
    """Test getting dividends when cache errors."""
    # Setup cache error
    mock_redis_cache.get.side_effect = Exception("Redis error")
    
    # Execute
    response = await service.get_dividends(VALID_NETUID, VALID_HOTKEY)
    
    # Assert
    assert isinstance(response, TaoDividendsResponse)
    assert response.netuid == VALID_NETUID
    assert response.hotkey == VALID_HOTKEY
    assert response.dividend == MOCK_DIVIDEND
    assert response.cached is False
    
    # Verify fallback to blockchain
    mock_bittensor_client.get_tao_dividends.assert_called_once_with(
        VALID_NETUID,
        VALID_HOTKEY
    )

@pytest.mark.asyncio
async def test_get_dividends_client_error(service, mock_bittensor_client, mock_redis_cache):
    """Test error handling when client fails."""
    # Setup client error
    mock_bittensor_client.get_tao_dividends.side_effect = Exception("Network error")
    
    # Execute and assert
    with pytest.raises(Exception):
        await service.get_dividends(VALID_NETUID, VALID_HOTKEY)
    
    # Verify interactions
    mock_redis_cache.get.assert_called_once()
    mock_bittensor_client.get_tao_dividends.assert_called_once() 