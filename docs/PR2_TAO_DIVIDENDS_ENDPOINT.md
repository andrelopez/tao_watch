# PR #2: Implement Tao Dividends Endpoint with Authentication

## Overview

This PR implements the first API endpoint for the Tao Watch service: `/api/v1/tao_dividends`. The endpoint provides a secure way to query Tao dividends data with proper authentication, input validation, and a structured response format. This implementation includes a static response for now, setting up the foundation for future integration with the Bittensor blockchain.

## Implementation Details

### 1. Authentication System
- Implemented Bearer token authentication using FastAPI's `OAuth2PasswordBearer`
- Added `API_TOKEN` configuration in settings
- Token validation middleware with proper error handling
- WWW-Authenticate header for unauthorized requests

### 2. Tao Dividends Endpoint
```python
@router.get("/tao_dividends", response_model=TaoDividendsResponse)
async def get_tao_dividends(
    netuid: int = Query(..., description="The subnet ID", ge=0),
    hotkey: str = Query(..., description="The hotkey (account ID or public key)", min_length=48, max_length=64),
    token: str = Depends(verify_token)
) -> TaoDividendsResponse:
```

#### Features:
- Protected endpoint requiring valid authentication
- Input validation for subnet ID and hotkey
- Structured response using Pydantic models
- Ready for future integration with Bittensor client
- Prepared for Redis caching implementation

### 3. Response Schema
```python
class TaoDividendsResponse(BaseModel):
    netuid: int
    hotkey: str
    dividend: int
    cached: bool
    stake_tx_triggered: bool
```

### 4. Test Coverage
- Comprehensive test suite with helper functions
- Tests for authentication
- Tests for input validation
- Tests for successful responses
- DRY principles applied to test code

## Files Changed
1. `app/core/security.py` - New file for authentication logic
2. `app/core/config.py` - Added API token configuration
3. `app/api/v1/schemas/tao.py` - New file for response schemas
4. `app/api/v1/endpoints/tao.py` - New file for tao endpoints
5. `app/main.py` - Updated to include new router
6. `tests/api/test_tao.py` - New test file

## Testing Instructions

1. Start the service:
```bash
docker compose up -d
```

2. Test the endpoint:
```bash
curl -X GET "http://localhost:8000/api/v1/tao_dividends?netuid=1&hotkey=5FFApaS75bv5pJHfAp2FVLBj9ZaXuFDjEypsaBNc1wCfe52v" \
  -H "Authorization: Bearer your-api-token-here-change-in-production"
```

3. Run tests:
```bash
docker compose exec api pytest tests/api/test_tao.py -v
```

## API Documentation
- Swagger UI available at: `http://localhost:8000/docs`
- ReDoc available at: `http://localhost:8000/redoc`

## Security Considerations
- API token required for protected endpoints
- Input validation prevents invalid data
- Error responses follow HTTP standards
- Authentication headers properly implemented

## Next Steps
1. Integrate Bittensor client for live dividend data
2. Implement Redis caching for responses
3. Add background task for stake operations
4. Add rate limiting
5. Implement proper logging for the endpoint

## Breaking Changes
None - This is a new feature addition.

## Dependencies Added
None - Using existing project dependencies.

## Notes for Reviewers
- The static response is temporary and will be replaced with actual Bittensor integration
- Test coverage is focused on HTTP layer; blockchain integration tests will be added later
- Authentication is simple token-based for now, can be enhanced based on requirements

## Checklist
- [x] Added new endpoint with authentication
- [x] Implemented input validation
- [x] Created response schema
- [x] Added comprehensive tests
- [x] Updated API documentation
- [x] Followed project coding standards
- [x] No breaking changes
- [x] All tests passing 