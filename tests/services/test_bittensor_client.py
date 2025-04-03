import pytest
from unittest.mock import MagicMock, patch
from app.services.bittensor_client import BittensorClient

MOCK_NETWORK = "test"
MOCK_NETUID = 1
MOCK_HOTKEY = "5FFApaS75bv5pJHfAp2FVLBj9ZaXuFDjEypsaBNc1wCfe52v"
MOCK_DIVIDEND = 1000000


@pytest.fixture
def mock_subtensor():
    with patch("bittensor.subtensor") as mock:
        mock_instance = MagicMock()
        mock_instance.get_dividends_for_uid = MagicMock(return_value=MOCK_DIVIDEND)
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
async def client(mock_subtensor):
    """Create a BittensorClient instance for testing."""
    client = BittensorClient(network=MOCK_NETWORK)
    await client.connect()
    try:
        yield client
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_connect():
    """Test connecting to Bittensor network."""
    with patch("bittensor.subtensor") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        
        client = BittensorClient(network=MOCK_NETWORK)
        await client.connect()
        
        mock.assert_called_once_with(network=MOCK_NETWORK)
        assert client._subtensor == mock_instance


@pytest.mark.asyncio
async def test_close():
    """Test closing Bittensor connection."""
    with patch("bittensor.subtensor") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        
        client = BittensorClient(network=MOCK_NETWORK)
        await client.connect()
        await client.close()
        
        assert client._subtensor is None


@pytest.mark.asyncio
async def test_get_tao_dividends(client):
    """Test getting Tao dividends."""
    async for c in client:
        dividend = await c.get_tao_dividends(MOCK_NETUID, MOCK_HOTKEY)
        
        assert dividend == MOCK_DIVIDEND
        c._subtensor.get_dividends_for_uid.assert_called_once_with(
            netuid=MOCK_NETUID,
            uid=MOCK_HOTKEY
        )
        break


@pytest.mark.asyncio
async def test_get_tao_dividends_not_connected():
    """Test getting Tao dividends when not connected."""
    client = BittensorClient(network=MOCK_NETWORK)
    
    with pytest.raises(RuntimeError, match="Not connected to Bittensor network"):
        await client.get_tao_dividends(MOCK_NETUID, MOCK_HOTKEY) 