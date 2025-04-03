from typing import Optional, Literal
import asyncio
import traceback
from loguru import logger
from substrateinterface import SubstrateInterface
from bittensor.core.chain_data import decode_account_id
from bittensor.core.settings import SS58_FORMAT
from app.core.config import settings

NetworkType = Literal["finney", "test"]

class BittensorClient:
    """Client for interacting with the Bittensor blockchain."""
    
    VALID_NETWORKS = {"finney", "test"}
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    
    def __init__(self, network: Optional[str] = None):
        """
        Initialize the Bittensor client.
        
        Args:
            network: The network to connect to (e.g., 'finney', 'test').
                    If not provided, uses BITTENSOR_NETWORK from settings.
        """
        self._network = self._validate_network(network or settings.BITTENSOR_NETWORK)
        self._substrate: Optional[SubstrateInterface] = None
        
        # Map network names to WebSocket endpoints from settings
        self._endpoints = {
            "finney": settings.bittensor_finney_endpoint,
            "test": settings.bittensor_test_endpoint
        }
    
    def _validate_network(self, network: str) -> NetworkType:
        """Validate and normalize network name."""
        if network not in self.VALID_NETWORKS:
            raise ValueError(
                f"Invalid network: {network}. "
                f"Valid networks are: {', '.join(sorted(self.VALID_NETWORKS))}"
            )
        return network  # type: ignore
    
    async def connect(self) -> None:
        """Establish connection to the Bittensor network with retries."""
        endpoint = self._endpoints.get(self._network)
        if not endpoint:
            raise ValueError(f"Unknown network: {self._network}")
        
        for attempt in range(self.MAX_RETRIES):
            try:
                # Create a substrate interface
                self._substrate = SubstrateInterface(
                    url=endpoint,
                    ss58_format=SS58_FORMAT
                )
                
                # Test the connection by making a simple query
                self._substrate.query("System", "Events")
                
                logger.info(f"Connected to Bittensor {self._network} network at {endpoint}")
                return
                
            except Exception as e:
                self._substrate = None
                if attempt < self.MAX_RETRIES - 1:
                    delay = self.RETRY_DELAY * (attempt + 1)
                    logger.warning(f"Connection attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Failed to connect to Bittensor network after {self.MAX_RETRIES} attempts: {e}")
                    raise
    
    async def close(self) -> None:
        """Close the connection to the Bittensor network."""
        if self._substrate:
            try:
                self._substrate.close()
                self._substrate = None
                logger.info("Closed connection to Bittensor network")
            except Exception as e:
                logger.error(f"Error closing Bittensor connection: {e}")
                raise
    
    async def get_tao_dividends(self, netuid: int, uid: str) -> float:
        """
        Get the Tao dividends for a given subnet and hotkey.
        
        Args:
            netuid: The subnet ID (will be converted to int if string)
            uid: The hotkey (account ID or public key in SS58 format)
            
        Returns:
            The dividend value
            
        Raises:
            RuntimeError: If the client is not connected
            ValueError: If netuid cannot be converted to integer
        """
        if not self._substrate:
            raise RuntimeError("Not connected to Bittensor network")
            
        try:
            # Ensure netuid is an integer
            netuid_int = int(netuid)
            
            # Query the TaoDividendsPerSubnet storage
            query_result = self._substrate.query_map(
                module="SubtensorModule",
                storage_function="TaoDividendsPerSubnet",
                params=[netuid_int]
            )
            
            # Process results
            for key, value in query_result:
                # The key is already in SS58 format, so we can compare directly
                if str(key) == uid:
                    dividend = float(value.value)  # Ensure we return a float
                    logger.info(f"Retrieved dividend for netuid={netuid_int}, uid={uid}: {dividend}")
                    return dividend
                    
            # If we get here, the UID wasn't found
            logger.warning(f"No dividend found for netuid={netuid_int}, uid={uid}")
            return 0.0
            
        except ValueError as e:
            logger.error(f"Invalid netuid value: {netuid}. Must be convertible to integer.")
            raise ValueError(f"Invalid netuid value: {netuid}. Must be convertible to integer.") from e
        except Exception as e:
            logger.error(f"Failed to get Tao dividends: {e} with traceback: {traceback.format_exc()}")
            raise 