from redis.asyncio import ConnectionPool, Redis

from src.settings import app_settings, redis_settings


class CacheStorage:
    def __init__(self) -> None:
        self.pool = ConnectionPool(
            host=redis_settings.host,
            port=redis_settings.port,
            db=redis_settings.db,
            password=redis_settings.password,
            max_connections=redis_settings.max_connections,
            decode_responses=True,
            socket_keepalive=True,
            health_check_interval=30,
        )
        self.redis = Redis(connection_pool=self.pool)

    async def set(self, key: str, value: str):
        await self.redis.set(
            key,
            value,
            ex=app_settings.link_cached_lifetime_minutes * 60,
        )

    async def get(self, key: str) -> str | None:
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def close(self) -> None:
        await self.redis.close()
        await self.pool.disconnect()


cache_storage = CacheStorage()
