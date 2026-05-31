import time
from collections import OrderedDict
from typing import Any


class LRUCache:
    """Thread-safe LRU cache with TTL support."""

    def __init__(self, max_size: int = 1000, ttl: int = 120):
        """
        Initialize LRU cache.

        Args:
            max_size: Maximum number of items in cache
            ttl: Time-to-live in seconds for cached items
        """
        self.max_size = max_size
        self.ttl = ttl
        self.cache: OrderedDict[str, tuple[float, Any]] = OrderedDict()

    def get(self, key: str) -> Any | None:
        """
        Get item from cache.

        Args:
            key: Cache key

        Returns:
            Cached value if found and not expired, None otherwise
        """
        if key not in self.cache:
            return None

        timestamp, value = self.cache[key]

        # Check if expired
        if time.time() - timestamp > self.ttl:
            del self.cache[key]
            return None

        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set item in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        # Remove if already exists
        if key in self.cache:
            del self.cache[key]

        # Add new item
        self.cache[key] = (time.time(), value)

        # Evict oldest if over max size
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)

    def clear(self) -> None:
        """Clear all items from cache."""
        self.cache.clear()

    def size(self) -> int:
        """Get current cache size."""
        return len(self.cache)

    def cleanup_expired(self) -> int:
        """
        Remove all expired items from cache.

        Returns:
            Number of items removed
        """
        current_time = time.time()
        expired_keys = [key for key, (timestamp, _) in self.cache.items() if current_time - timestamp > self.ttl]

        for key in expired_keys:
            del self.cache[key]

        return len(expired_keys)
