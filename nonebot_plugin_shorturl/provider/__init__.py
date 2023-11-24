import abc
import secrets
from typing import Optional
from urllib.parse import urljoin

from pydantic import BaseModel

from ..config import CacheType
from .. import driver, plugin_config


class CacheProvider(abc.ABC):
    @abc.abstractmethod
    async def lookup(self, token: str) -> Optional[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def store(self, url: str) -> str:
        raise NotImplementedError

    async def get_unique_token(self, token: Optional[str] = None) -> str:
        if not token or await self.lookup(token):
            return await self.get_unique_token(secrets.token_urlsafe(8))

        else:
            return token


_cache_provider: Optional[CacheProvider] = None


@driver.on_startup
def init_provider():
    global _cache_provider

    if plugin_config.shorturl_cache_type == CacheType.diskcache:
        from .diskcache import DiskcacheProvider

        _cache_provider = DiskcacheProvider()

    elif plugin_config.shorturl_cache_type == CacheType.redis:
        from .redis import RedisCacheProvider

        _cache_provider = RedisCacheProvider()

    elif plugin_config.shorturl_cache_type == CacheType.memory:
        from .memory import MemoryProvider

        _cache_provider = MemoryProvider()

    return _cache_provider


def get_provider():
    if not _cache_provider:
        raise RuntimeError("Shorturl cache provider not initialized!")

    return _cache_provider


class ShortURL(BaseModel):
    url: str

    async def to_url(self) -> str:
        token = await get_provider().store(self.url)

        return urljoin(
            plugin_config.shorturl_host,
            plugin_config.shorturl_endpoint.format(encoded=token),
        )
