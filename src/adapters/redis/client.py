from redis import asyncio as redis

from src.core.config import settings


class RedisAsyncClient:
    def __init__(self, host: str, port: int, db: int = 0) -> None:
        self._host: str = host
        self._port: int = port
        self._db: int = db
        self._client: redis.Redis | None = None

    async def connect(self) -> None:
        self._client = await redis.Redis(
            host=self._host,
            port=self._port,
            db=self._db,
            decode_responses=True,
        )
        await self._client.ping()

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()
            self._client = None

    @property
    def client(self) -> redis.Redis:
        if self._client is None:
            msg = "Redis client is not connected."
            raise RuntimeError(msg)
        return self._client

    @property
    def is_closed(self) -> bool:
        return self._client is None


redis_client = RedisAsyncClient(
    host=settings.redis.host,
    port=settings.redis.port,
    db=settings.redis.database,
)
