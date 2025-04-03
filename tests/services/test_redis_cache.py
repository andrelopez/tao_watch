import json
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.redis_cache import RedisCache

@pytest.fixture
def mock_redis():
    """Create a mock Redis client."""
    redis = AsyncMock()
    redis.get = AsyncMock()
    redis.set = AsyncMock()
    redis.delete = AsyncMock()
    return redis

@pytest.fixture
def cache(mock_redis):
    """Create a RedisCache instance with mock Redis client."""
    return RedisCache(mock_redis)

@pytest.mark.asyncio
async def test_get_cache_hit(cache, mock_redis):
    """Test getting a value that exists in cache."""
    # Setup
    mock_redis.get.return_value = b'{"test": "value"}'
    
    # Execute
    result = await cache.get("test", "key1", "key2")
    
    # Assert
    assert result == '{"test": "value"}'
    mock_redis.get.assert_called_once_with("test:key1:key2")

@pytest.mark.asyncio
async def test_get_cache_miss(cache, mock_redis):
    """Test getting a value that doesn't exist in cache."""
    # Setup
    mock_redis.get.return_value = None
    
    # Execute
    result = await cache.get("test", "key1")
    
    # Assert
    assert result is None
    mock_redis.get.assert_called_once_with("test:key1")

@pytest.mark.asyncio
async def test_get_cache_error(cache, mock_redis):
    """Test getting a value when Redis errors."""
    # Setup
    mock_redis.get.side_effect = Exception("Redis error")
    
    # Execute
    result = await cache.get("test", "key1")
    
    # Assert
    assert result is None
    mock_redis.get.assert_called_once_with("test:key1")

@pytest.mark.asyncio
async def test_set_cache_success(cache, mock_redis):
    """Test setting a value in cache."""
    # Setup
    value = {"test": "value"}
    mock_redis.set.return_value = True
    
    # Execute
    result = await cache.set(value, "test", "key1")
    
    # Assert
    assert result is True
    mock_redis.set.assert_called_once_with(
        "test:key1",
        json.dumps(value),
        ex=120  # Default expiration from settings
    )

@pytest.mark.asyncio
async def test_set_cache_error(cache, mock_redis):
    """Test setting a value when Redis errors."""
    # Setup
    mock_redis.set.side_effect = Exception("Redis error")
    
    # Execute
    result = await cache.set({"test": "value"}, "test", "key1")
    
    # Assert
    assert result is False
    mock_redis.set.assert_called_once()

@pytest.mark.asyncio
async def test_delete_cache_success(cache, mock_redis):
    """Test deleting a value from cache."""
    # Setup
    mock_redis.delete.return_value = 1
    
    # Execute
    result = await cache.delete("test", "key1")
    
    # Assert
    assert result is True
    mock_redis.delete.assert_called_once_with("test:key1")

@pytest.mark.asyncio
async def test_delete_cache_error(cache, mock_redis):
    """Test deleting a value when Redis errors."""
    # Setup
    mock_redis.delete.side_effect = Exception("Redis error")
    
    # Execute
    result = await cache.delete("test", "key1")
    
    # Assert
    assert result is False
    mock_redis.delete.assert_called_once_with("test:key1") 