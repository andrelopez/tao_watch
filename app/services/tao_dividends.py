from loguru import logger
from app.services.bittensor_client import BittensorClient
from app.api.v1.schemas.tao import TaoDividendsResponse


class TaoDividendsService:
    """Service for handling Tao dividends operations."""
    
    def __init__(self, bittensor_client: BittensorClient):
        """
        Initialize the TaoDividends service.
        
        Args:
            bittensor_client: The Bittensor client instance
        """
        self._client = bittensor_client
    
    async def get_dividends(self, netuid: int, hotkey: str) -> TaoDividendsResponse:
        """
        Get Tao dividends for a given subnet and hotkey.
        
        Args:
            netuid: The subnet ID
            hotkey: The hotkey (account ID or public key)
            
        Returns:
            TaoDividendsResponse with the dividend data
            
        Raises:
            Exception: If the query fails
        """
        try:
            dividend = await self._client.get_tao_dividends(netuid, hotkey)
            
            return TaoDividendsResponse(
                netuid=netuid,
                hotkey=hotkey,
                dividend=dividend,
                cached=False,  # Not using cache yet
                stake_tx_triggered=False  # Not triggering stake yet
            )
            
        except Exception as e:
            logger.error(f"Failed to get Tao dividends: {e}")
            raise 