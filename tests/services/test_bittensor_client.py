import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.services.bittensor_client import BittensorClient
from app.core.config import settings

MOCK_NETWORK = "test"
MOCK_NETUID = 1
MOCK_HOTKEY = "5DD26kk..."
MOCK_DIVIDEND = 1000000


@pytest.fixture(autouse=True)
def mock_settings():
    """Mock settings for testing."""
    with patch("app.services.bittensor_client.settings") as mock_settings:
        mock_settings.BITTENSOR_NETWORK = MOCK_NETWORK
        mock_settings.bittensor_finney_endpoint = "wss://mock-finney:443"
        mock_settings.bittensor_test_endpoint = "ws://mock-test:9944"
        yield mock_settings


@pytest.fixture
def mock_subtensor():
    with patch("bittensor.subtensor") as mock:
        mock_instance = MagicMock()
        mock_instance.get_dividends_for_uid = MagicMock(return_value=MOCK_DIVIDEND)
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
async def client():
    """Create a BittensorClient instance for testing."""
    with patch("app.services.bittensor_client.SubstrateInterface") as mock_substrate:
        mock_instance = MagicMock()
        mock_substrate.return_value = mock_instance
        
        client = BittensorClient(network=MOCK_NETWORK)
        await client.connect()
        yield client
        await client.close()


@pytest.mark.asyncio
async def test_connect():
    """Test connecting to Bittensor network."""
    with patch("app.services.bittensor_client.SubstrateInterface") as mock_substrate:
        mock_instance = MagicMock()
        mock_substrate.return_value = mock_instance

        client = BittensorClient(network=MOCK_NETWORK)
        await client.connect()
        
        mock_substrate.assert_called_once()
        assert client._substrate is not None


@pytest.mark.asyncio
async def test_close():
    """Test closing Bittensor connection."""
    with patch("app.services.bittensor_client.SubstrateInterface") as mock_substrate:
        mock_instance = MagicMock()
        mock_substrate.return_value = mock_instance

        client = BittensorClient(network=MOCK_NETWORK)
        await client.connect()
        await client.close()
        
        assert client._substrate is None


@pytest.mark.asyncio
async def test_get_tao_dividends(client):
    """Test getting Tao dividends."""
    async for c in client:
        mock_substrate = c._substrate
        mock_substrate.query_map = MagicMock()
        
        # Create a mock query result that matches the expected format
        mock_key = MagicMock()
        mock_value = MagicMock()
        mock_value.value = 1000
        
        # Mock decode_account_id to return our test hotkey
        with patch("app.services.bittensor_client.decode_account_id") as mock_decode:
            mock_decode.return_value = MOCK_HOTKEY
            mock_substrate.query_map.return_value = [(mock_key, mock_value)]
            
            result = await c.get_tao_dividends(MOCK_NETUID, MOCK_HOTKEY)
            assert result == 1000
            
            mock_substrate.query_map.assert_called_once_with(
                module="SubtensorModule",
                storage_function="TaoDividendsPerSubnet",
                params=[MOCK_NETUID]
            )
            mock_decode.assert_called_once_with(mock_key)
        break


@pytest.mark.asyncio
async def test_get_tao_dividends_not_connected():
    """Test getting Tao dividends when not connected."""
    client = BittensorClient(network=MOCK_NETWORK)
    with pytest.raises(RuntimeError, match="Not connected to Bittensor network"):
        await client.get_tao_dividends(MOCK_NETUID, MOCK_HOTKEY)


@pytest.mark.asyncio
async def test_init_with_invalid_network():
    """Test initialization with invalid network."""
    with pytest.raises(ValueError, match="Invalid network: invalid"):
        BittensorClient(network="invalid")


@pytest.mark.asyncio
async def test_init_with_default_network():
    """Test initialization with default network from settings."""
    client = BittensorClient()
    assert client._network == MOCK_NETWORK 


@pytest.mark.asyncio
async def test_get_tao_dividends_with_string_netuid(client):
    """Test getting Tao dividends with string netuid."""
    async for c in client:
        mock_substrate = c._substrate
        mock_substrate.query_map = MagicMock()
        
        # Create a mock query result
        mock_key = MagicMock()
        mock_value = MagicMock()
        mock_value.value = "1000"  # String value from substrate
        
        # Mock decode_account_id to return our test hotkey
        with patch("app.services.bittensor_client.decode_account_id") as mock_decode:
            mock_decode.return_value = MOCK_HOTKEY
            mock_substrate.query_map.return_value = [(mock_key, mock_value)]
            
            # Test with string netuid
            result = await c.get_tao_dividends("1", MOCK_HOTKEY)
            assert result == 1000.0
            
            mock_substrate.query_map.assert_called_once_with(
                module="SubtensorModule",
                storage_function="TaoDividendsPerSubnet",
                params=[1]  # Should be converted to int
            )
            mock_decode.assert_called_once_with(mock_key)
        break


@pytest.mark.asyncio
async def test_get_tao_dividends_with_invalid_netuid(client):
    """Test getting Tao dividends with invalid netuid."""
    async for c in client:
        with pytest.raises(ValueError, match="Invalid netuid value: invalid. Must be convertible to integer."):
            await c.get_tao_dividends("invalid", MOCK_HOTKEY)
        break 