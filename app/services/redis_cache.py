from typing import Optional, Any
import json
from redis.asyncio import Redis
from loguru import logger
from app.core.config import settings

class RedisCache:
    """Service for handling Redis caching operations."""
    
    def __init__(self, redis_client: Redis):
        """Initialize the Redis cache service."""
        self._redis = redis_client
        self._expiration_seconds = settings.CACHE_EXPIRATION_SECONDS
    
    @staticmethod
    def _build_key(prefix: str, *args: Any) -> str:
        """Build a cache key from prefix and arguments."""
        return f"{prefix}:{':'.join(str(arg) for arg in args)}"
    
    async def get(self, prefix: str, *args: Any) -> Optional[str]:
        """
        Get a value from cache.
        
        Args:
            prefix: The key prefix (e.g., 'tao_dividends')
            *args: Key components to build the full key
            
        Returns:
            The cached value or None if not found
        """
        key = self._build_key(prefix, *args)
        try:
            value = await self._redis.get(key)
            if value:
                logger.debug(f"Cache hit for key: {key}")
                return value.decode('utf-8')
            logger.debug(f"Cache miss for key: {key}")
            return None
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return None
    
    async def set(self, value: Any, prefix: str, *args: Any) -> bool:
        """
        Set a value in cache.
        
        Args:
            value: The value to cache
            prefix: The key prefix (e.g., 'tao_dividends')
            *args: Key components to build the full key
            
        Returns:
            True if successful, False otherwise
        """
        key = self._build_key(prefix, *args)
        try:
            # Convert value to JSON string for storage
            json_value = json.dumps(value)
            await self._redis.set(
                key,
                json_value,
                ex=self._expiration_seconds
            )
            logger.debug(f"Cached value for key: {key}")
            return True
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False
            
    async def delete(self, prefix: str, *args: Any) -> bool:
        """
        Delete a value from cache.
        
        Args:
            prefix: The key prefix (e.g., 'tao_dividends')
            *args: Key components to build the full key
            
        Returns:
            True if successful, False otherwise
        """
        key = self._build_key(prefix, *args)
        try:
            await self._redis.delete(key)
            logger.debug(f"Deleted cache for key: {key}")
            return True
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")
            return False 