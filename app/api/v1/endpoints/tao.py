from fastapi import APIRouter, Depends, Query
from app.core.security import verify_token
from app.api.v1.schemas.tao import TaoDividendsResponse
from app.services.tao_dividends import TaoDividendsService
from app.core.dependencies import get_tao_dividends_service

router = APIRouter()


@router.get("/tao_dividends", response_model=TaoDividendsResponse)
async def get_tao_dividends(
    netuid: int = Query(..., description="The subnet ID", ge=0),
    hotkey: str = Query(..., description="The hotkey (account ID or public key)", min_length=48, max_length=64),
    token: str = Depends(verify_token),
    service: TaoDividendsService = Depends(get_tao_dividends_service)
) -> TaoDividendsResponse:
    """
    Get Tao dividends for a given subnet and hotkey.
    
    This endpoint:
    - Queries the Bittensor blockchain for dividend data
    - Will support caching in future updates
    - Will trigger background stake operations in future updates
    """
    return await service.get_dividends(netuid=netuid, hotkey=hotkey) 