from urllib.parse import urlparse

from fastapi import FastAPI
from nonebot.drivers import ASGIMixin
from nonebot.plugin import PluginMetadata
from fastapi.responses import RedirectResponse
from nonebot import logger, get_app, get_driver

from .config import Config

driver = get_driver()
plugin_config = Config.parse_obj(driver.config)

from .provider import get_provider
from .provider import ShortURL as ShortURL

__plugin_meta__ = PluginMetadata(
    name="短链接服务支持",
    description="为其他插件提供短链接转换服务",
    usage="见文档（https://github.com/StarHeartHunt/nonebot-plugin-shorturl#readme）",
    type="library",
    homepage="https://github.com/StarHeartHunt/nonebot-plugin-shorturl",
    config=Config,
    supported_adapters=None,
)

if not (
    server_app := get_app() if isinstance(driver, ASGIMixin) else None
) or not isinstance(server_app, FastAPI):
    logger.warning("ShortURL plugin only supports fastapi driver")


if isinstance(server_app, FastAPI):

    @server_app.get(plugin_config.shorturl_endpoint)
    async def endpoint_handler(token: str):
        provider = get_provider()

        if not (url := await provider.lookup(token)):
            return {"msg": "url not found in cache"}

        if not urlparse(url).hostname:
            url = f"http://{url}"

        return RedirectResponse(url)
