from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def verify_token(token: str = Depends(oauth2_scheme)) -> str:
    """Verify the access token."""
    if token != settings.API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token 