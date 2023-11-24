from typing import Optional
from typing_extensions import override

import redis.asyncio as redis
from nonebot import get_driver
from pydantic import BaseModel, validator

from . import CacheProvider
from .consts import CACHE_KEY_FORMAT


class RedisConfig(BaseModel):
    shorturl_redis_host: str
    shorturl_redis_port: int
    shorturl_redis_db: int = 0
    shorturl_redis_username: Optional[str] = None
    shorturl_redis_password: Optional[str] = None

    @validator("shorturl_redis_db", pre=True)
    def replace_empty(cls, value):
        return value or 0


class RedisCacheProvider(CacheProvider):
    def __init__(self) -> None:
        super().__init__()
        self.redis_config = RedisConfig.parse_obj(get_driver().config)
        self.redis_client = redis.Redis(
            host=self.redis_config.shorturl_redis_host,
            port=self.redis_config.shorturl_redis_port,
            db=self.redis_config.shorturl_redis_db,
            username=self.redis_config.shorturl_redis_username,
            password=self.redis_config.shorturl_redis_password,
            encoding="utf-8",
        )

    @override
    async def lookup(self, token: str):
        cache = (
            await self.redis_client.get(CACHE_KEY_FORMAT.format(token=token))
        ).decode()

        return cache

    @override
    async def store(self, url: str):
        token = await self.get_unique_token()
        await self.redis_client.set(CACHE_KEY_FORMAT.format(token=token), url)

        return token
