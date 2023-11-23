from typing import Optional

import base62
from fastapi import FastAPI
from nonebot.drivers import ASGIMixin
from nonebot.plugin import PluginMetadata
from fastapi.responses import RedirectResponse
from nonebot import logger, get_app, get_driver

from .provider import CacheProvider
from .config import Config, CacheType

__plugin_meta__ = PluginMetadata(
    name="短链接服务支持",
    description="为其他插件提供短链接转换服务",
    usage="见文档（https://github.com/StarHeartHunt/nonebot-plugin-shorturl#readme）",
    type="library",
    homepage="https://github.com/StarHeartHunt/nonebot-plugin-shorturl",
    config=Config,
    supported_adapters=None,
)

driver = get_driver()
server_app = get_app() if isinstance(driver, ASGIMixin) else None

if not server_app or not isinstance(server_app, FastAPI):
    logger.warning("ShortURL plugin only support fastapi driver")

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


if isinstance(server_app, FastAPI):

    @server_app.get("/shorturl/{encoded}")
    async def endpoint_handler(encoded: str):
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
