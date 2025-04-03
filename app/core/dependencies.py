from typing import AsyncGenerator
from fastapi import Depends
from app.services.bittensor_client import BittensorClient
from app.services.tao_dividends import TaoDividendsService
from app.core.config import settings


async def get_bittensor_client() -> AsyncGenerator[BittensorClient, None]:
    """
    FastAPI dependency that provides a BittensorClient instance.
    Handles connection lifecycle.
    """
    client = BittensorClient(network=settings.BITTENSOR_NETWORK)
    await client.connect()
    try:
        yield client
    finally:
        await client.close()


async def get_tao_dividends_service(
    client: BittensorClient = Depends(get_bittensor_client)
) -> TaoDividendsService:
    """
    FastAPI dependency that provides a TaoDividendsService instance.
    """
    return TaoDividendsService(bittensor_client=client) 