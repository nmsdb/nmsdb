from typing import Annotated, Dict, Optional
from redis.asyncio import Redis, from_url
from fastapi import Depends

from nmsdb.config import settings


class RedisService:
    def __init__(self, redis_uri: str, redis_password: str):
        self.redis: Redis = from_url(
            redis_uri,
            # password=redis_password,
            encoding="utf-8",
            decode_responses=True,
        )

    async def get(self, key: str) -> Optional[str]:
        """Get a value from Redis or return None if not found"""
        return await self.redis.get(key)

    async def get_multi(self, keys: list[str]) -> Dict[str, Optional[str]]:
        """Get multiple values at once, returns a dict of {key: translation}"""
        if not keys:
            return {}

        pipe = self.redis.pipeline()
        for key in keys:
            pipe.get(key)

        results = await pipe.execute()
        return dict(zip(keys, results))

    async def set(self, key: str, value: str, timeout: Optional[int] = None) -> bool:
        """
        Set a value in Redis with optional expiration time

        Args:
            key: Redis key
            value: Value to store
            timeout: Expiration time in seconds (None means no expiration)
        """
        return await self.redis.set(key, value, ex=timeout)

    async def push_list(self, key: str, *args) -> bool:
        """
        Push values to a Redis list.

        Args:
            key: Redis key
            args: Values to push
        """
        return await self.redis.rpush(key, *args)

    async def get_list(
        self, key: str, lower_range: int = 0, upper_range: int = -1
    ) -> list[str]:
        """
        Get a range of values from a Redis list.

        Args:
            key: Redis key
            lower_range: Start index (inclusive)
            upper_range: End index (exclusive)
        """
        return await self.redis.lrange(key, lower_range, upper_range)

    async def delete(self, *args) -> bool:
        """
        Delete a key from Redis.

        Args:
            key: Redis key
        """
        return await self.redis.delete(*args)


def get_redis_service() -> RedisService:
    return RedisService(
        redis_uri=settings.REDIS_URI, redis_password=settings.REDIS_PASSWORD
    )


RedisServiceDep = Annotated[RedisService, Depends(get_redis_service)]
