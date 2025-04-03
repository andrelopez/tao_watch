from typing import AsyncGenerator
from redis.asyncio import Redis
from fastapi import Depends
from app.services.bittensor_client import BittensorClient
from app.services.tao_dividends import TaoDividendsService
from app.services.redis_cache import RedisCache
from app.core.config import settings


async def get_redis() -> AsyncGenerator[Redis, None]:
    """Get Redis client."""
    redis = Redis.from_url(str(settings.REDIS_URI))
    try:
        yield redis
    finally:
        await redis.close()


async def get_redis_cache(redis: Redis = Depends(get_redis)) -> RedisCache:
    """Get Redis cache service."""
    return RedisCache(redis)


async def get_bittensor_client() -> AsyncGenerator[BittensorClient, None]:
    """Get Bittensor client."""
    client = BittensorClient()
    try:
        await client.connect()
        yield client
    finally:
        await client.close()


async def get_tao_dividends_service(
    client: BittensorClient = Depends(get_bittensor_client),
    cache: RedisCache = Depends(get_redis_cache)
) -> TaoDividendsService:
    """Get Tao dividends service."""
    return TaoDividendsService(client, cache) 