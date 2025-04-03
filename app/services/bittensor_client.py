from typing import Optional
from loguru import logger
import bittensor

class BittensorClient:
    """Client for interacting with the Bittensor blockchain."""
    
    def __init__(self, network: str = "finney"):
        """
        Initialize the Bittensor client.
        
        Args:
            network: The network to connect to (e.g., 'finney', 'test')
        """
        self._network = network
        self._subtensor: Optional[bittensor.subtensor] = None
    
    async def connect(self) -> None:
        """Establish connection to the Bittensor network."""
        try:
            # Create a subtensor instance for the specified network
            self._subtensor = bittensor.subtensor(network=self._network)
            logger.info(f"Connected to Bittensor {self._network} network")
        except Exception as e:
            logger.error(f"Failed to connect to Bittensor network: {e}")
            raise
    
    async def close(self) -> None:
        """Close the connection to the Bittensor network."""
        if self._subtensor:
            # No need to close in v9.2.0 as it's handled internally
            self._subtensor = None
            logger.info("Closed connection to Bittensor network")
    
    async def get_tao_dividends(self, netuid: int, uid: str) -> float:
        """
        Get the Tao dividends for a given subnet and hotkey.
        
        Args:
            netuid: The subnet ID
            uid: The hotkey (account ID or public key)
            
        Returns:
            The dividend value
            
        Raises:
            RuntimeError: If the client is not connected
        """
        if not self._subtensor:
            raise RuntimeError("Not connected to Bittensor network")
            
        try:
            # Query the chain state for dividends
            dividend = self._subtensor.get_dividends(
                netuid=netuid,
                address=uid
            )
            logger.info(f"Retrieved dividend for netuid={netuid}, uid={uid}: {dividend}")
            return dividend
            
        except Exception as e:
            logger.error(f"Failed to get Tao dividends: {e}")
            raise 