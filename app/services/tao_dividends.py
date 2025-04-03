import json
from loguru import logger
from app.services.bittensor_client import BittensorClient
from app.services.redis_cache import RedisCache
from app.api.v1.schemas.tao import TaoDividendsResponse


class TaoDividendsService:
    """Service for handling Tao dividends operations."""
    
    CACHE_PREFIX = "tao_dividends"
    
    def __init__(self, bittensor_client: BittensorClient, cache: RedisCache):
        """
        Initialize the TaoDividends service.
        
        Args:
            bittensor_client: The Bittensor client instance
            cache: The Redis cache service
        """
        self._client = bittensor_client
        self._cache = cache
    
    async def get_dividends(self, netuid: int, hotkey: str) -> TaoDividendsResponse:
        """
        Get Tao dividends for a given subnet and hotkey.
        
        Args:
            netuid: The subnet ID
            hotkey: The hotkey (account ID or public key)
            
        Returns:
            TaoDividendsResponse with the dividend data
            
        Raises:
            Exception: If the blockchain query fails
        """
        try:
            # Try to get from cache first
            try:
                logger.info(f"Getting dividends from cache for netuid={netuid}, hotkey={hotkey}")
                cached_value = await self._cache.get(self.CACHE_PREFIX, netuid, hotkey)
                if cached_value:
                    logger.info("Cache hit")
                    # Parse cached JSON and return response
                    data = json.loads(cached_value)
                    return TaoDividendsResponse(
                        netuid=data["netuid"],
                        hotkey=data["hotkey"],
                        dividend=data["dividend"],
                        cached=True,
                        stake_tx_triggered=data["stake_tx_triggered"]
                    )
            except Exception as cache_error:
                logger.error(f"Cache error: {cache_error}")
                # Continue with blockchain query on cache error
            
            # Get from blockchain
            dividend = await self._client.get_tao_dividends(netuid, hotkey)
            
            # Create response
            response = TaoDividendsResponse(
                netuid=netuid,
                hotkey=hotkey,
                dividend=dividend,
                cached=False,
                stake_tx_triggered=False
            )
            
            # Try to cache the response
            try:
                await self._cache.set(
                    response.model_dump(),
                    self.CACHE_PREFIX,
                    netuid,
                    hotkey
                )
            except Exception as cache_error:
                logger.error(f"Failed to cache response: {cache_error}")
                # Continue without caching
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to get Tao dividends: {e}")
            raise 