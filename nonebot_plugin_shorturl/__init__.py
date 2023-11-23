from typing import Optional

import base62
from fastapi import FastAPI
from nonebot.plugin import PluginMetadata
from fastapi.responses import RedirectResponse
from nonebot import get_app, get_driver

from .provider import CacheProvider
from .config import Config, CacheType

if not isinstance((server_app := get_app()), FastAPI):
    raise ValueError("ShortURL supports FastAPI driver only")

driver = get_driver()
plugin_config = Config.parse_obj(driver.config)

_cache_provider: Optional[CacheProvider] = None


@driver.on_startup
def init_provider():
    global _cache_provider

    if plugin_config.shorturl_cache_type == CacheType.diskcache:
        from .provider.diskcache import DiskcacheProvider

        _cache_provider = DiskcacheProvider()
    elif plugin_config.shorturl_cache_type == CacheType.redis:
        from .provider.redis import RedisCacheProvider

        _cache_provider = RedisCacheProvider()
    elif plugin_config.shorturl_cache_type == CacheType.memory:
        from .provider.memory import MemoryProvider

        _cache_provider = MemoryProvider()

    return _cache_provider


def get_provider():
    if not _cache_provider:
        raise RuntimeError("Shorturl cache provider not initialized!")

    return _cache_provider


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


__plugin_meta__ = PluginMetadata(
    name="短链接服务支持",
    description="为其他插件提供短链接转换服务",
    usage="见文档（https://github.com/StarHeartHunt/nonebot-plugin-shorturl#readme）",
    type="library",
    homepage="https://github.com/StarHeartHunt/nonebot-plugin-shorturl",
    config=Config,
    supported_adapters=None,
)
