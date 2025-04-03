from pydantic import BaseModel, Field


class TaoDividendsResponse(BaseModel):
    """Schema for Tao dividends response."""
    
    netuid: int = Field(..., description="The subnet ID")
    hotkey: str = Field(..., description="The hotkey (account ID or public key)")
    dividend: float = Field(..., description="The dividend value")
    cached: bool = Field(default=True, description="Whether the response was served from cache")
    stake_tx_triggered: bool = Field(default=True, description="Whether a stake transaction was triggered") 