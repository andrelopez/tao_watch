import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio
async def test_health_check(app):
    """Test that the health check endpoint returns 200 OK."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "healthy"} 