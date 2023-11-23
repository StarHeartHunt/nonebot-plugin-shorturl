from typing import Optional

import base62
from fastapi import FastAPI
from nonebot import get_app, get_driver
from fastapi.responses import RedirectResponse

from .config import Config, CacheType
from .provider import CacheProvider, DiskcacheProvider, RedisCacheProvider

if not isinstance((server_app := get_app()), FastAPI):
    raise ValueError("ShortURL supports FastAPI driver only")

driver = get_driver()
plugin_config = Config.parse_obj(driver.config)

_cache_provider: Optional[CacheProvider] = None


@driver.on_startup
def init_provider() -> CacheProvider:
    global _cache_provider

    if plugin_config.shorturl_cache_type == CacheType.diskcache:
        _cache_provider = DiskcacheProvider()
    elif plugin_config.shorturl_cache_type == CacheType.redis:
        _cache_provider = RedisCacheProvider()

    if not _cache_provider:
        raise RuntimeError("Failed to initialize shorturl cache provider")

    return _cache_provider


def get_provider():
    return _cache_provider or init_provider()


@server_app.get("/shorturl/{encoded}")
async def custom_api(encoded: str):
    decoded: int = base62.decode(encoded)
    provider = get_provider()

    if not (url := await provider.lookup(decoded)):
        return

    return RedirectResponse(url)


class ShortURL:
    def __init__(self, url: str) -> None:
        self.url: str = url

    async def to_url(self) -> str:
        index = await get_provider().store(self.url)
        return f"{plugin_config.shorturl_host}/shorturl/{base62.encode(index)}"
