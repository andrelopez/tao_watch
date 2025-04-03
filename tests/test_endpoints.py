import asyncio
import websockets
from loguru import logger

async def test_websocket_connection(url: str) -> bool:
    """Test if we can connect to a WebSocket endpoint."""
    try:
        async with websockets.connect(url) as websocket:
            logger.info(f"Successfully connected to {url}")
            return True
    except Exception as e:
        logger.error(f"Failed to connect to {url}: {e}")
        return False

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