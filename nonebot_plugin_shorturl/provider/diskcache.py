from typing import Optional
from typing_extensions import override

import diskcache
from nonebot import get_driver
from pydantic import BaseModel

from . import CacheProvider
from .consts import CACHE_KEY_FORMAT


class DiskcacheConfig(BaseModel):
    shorturl_diskcache_folder: str


class DiskcacheProvider(CacheProvider):
    def __init__(self):
        super().__init__()
        self.diskcache_config = DiskcacheConfig.parse_obj(get_driver().config)
        self.cache = diskcache.Cache(self.diskcache_config.shorturl_diskcache_folder)

    @override
    async def lookup(self, token: str):
        url: Optional[str] = self.cache.get(CACHE_KEY_FORMAT.format(token=token))  # type: ignore

        return url

    @override
    async def store(self, url: str):
        token = await self.get_unique_token()
        self.cache.set(CACHE_KEY_FORMAT.format(token=token), url)

        return token
