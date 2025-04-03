import asyncio
import websockets
from loguru import logger
from app.core.config import settings
import pytest

@pytest.mark.asyncio
@pytest.mark.parametrize("url", [
    settings.bittensor_finney_endpoint,
    settings.bittensor_test_endpoint
])
async def test_websocket_connection(url: str) -> None:
    """Test if we can connect to a WebSocket endpoint."""
    try:
        async with websockets.connect(url) as websocket:
            logger.info(f"Successfully connected to {url}")
            # Send a ping and wait for pong to verify connection
            pong_waiter = await websocket.ping()
            await pong_waiter
            logger.info(f"Received pong from {url}")
    except (websockets.exceptions.WebSocketException, ConnectionRefusedError) as e:
        logger.error(f"Failed to connect to {url}: {e}")
        pytest.skip(f"Skipping test for {url} - endpoint not available: {e}")
    except Exception as e:
        logger.error(f"Unexpected error connecting to {url}: {e}")
        pytest.fail(f"Unexpected error connecting to {url}: {e}")

async def main():
    """Test both Bittensor network endpoints."""
    finney_endpoint = "wss://entrypoint-finney.opentensor.ai:443"
    test_endpoint = "wss://test.finney.opentensor.ai:9944"  # Note: Changed to wss://
    
    logger.info("Testing Finney network endpoint...")
    await test_websocket_connection(finney_endpoint)
    
    logger.info("Testing Test network endpoint...")
    await test_websocket_connection(test_endpoint)

if __name__ == "__main__":
    asyncio.run(main()) 