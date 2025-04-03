from fastapi import APIRouter, Depends, Query
from app.core.security import verify_token
from app.api.v1.schemas.tao import TaoDividendsResponse

router = APIRouter()


@router.get("/tao_dividends", response_model=TaoDividendsResponse)
async def get_tao_dividends(
    netuid: int = Query(..., description="The subnet ID", ge=0),
    hotkey: str = Query(..., description="The hotkey (account ID or public key)", min_length=48, max_length=64),
    token: str = Depends(verify_token)
) -> TaoDividendsResponse:
    """
    Get Tao dividends for a given subnet and hotkey.
    
    This endpoint returns static data for now. In the future, it will:
    - Query the Bittensor blockchain
    - Cache results in Redis
    - Trigger background stake operations
    """
    # Static response for now
    return TaoDividendsResponse(
        netuid=netuid,
        hotkey=hotkey,
        dividend=123456789,
        cached=True,
        stake_tx_triggered=True
    ) 