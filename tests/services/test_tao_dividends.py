import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.tao_dividends import TaoDividendsService
from app.services.bittensor_client import BittensorClient

MOCK_NETUID = 1
MOCK_HOTKEY = "5FFApaS75bv5pJHfAp2FVLBj9ZaXuFDjEypsaBNc1wCfe52v"
MOCK_DIVIDEND = 1000000


@pytest.fixture
def mock_client():
    client = MagicMock(spec=BittensorClient)
    client.get_tao_dividends = AsyncMock(return_value=MOCK_DIVIDEND)
    return client


@pytest.fixture
def service(mock_client):
    return TaoDividendsService(bittensor_client=mock_client)


@pytest.mark.asyncio
async def test_get_dividends_success(service, mock_client):
    """Test getting dividends successfully."""
    response = await service.get_dividends(MOCK_NETUID, MOCK_HOTKEY)
    
    assert response.netuid == MOCK_NETUID
    assert response.hotkey == MOCK_HOTKEY
    assert response.dividend == MOCK_DIVIDEND
    assert response.cached is False
    assert response.stake_tx_triggered is False
    
    mock_client.get_tao_dividends.assert_called_once_with(MOCK_NETUID, MOCK_HOTKEY)


@pytest.mark.asyncio
async def test_get_dividends_client_error(service, mock_client):
    """Test handling client errors."""
    mock_client.get_tao_dividends.side_effect = Exception("Network error")
    
    with pytest.raises(Exception, match="Network error"):
        await service.get_dividends(MOCK_NETUID, MOCK_HOTKEY) 