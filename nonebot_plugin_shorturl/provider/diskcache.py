from typing_extensions import override

import diskcache
from nonebot import get_driver
from pydantic import BaseModel

from . import CacheProvider
from .consts import CACHE_KEY_FORMAT, COUNT_KEY_FORMAT


class DiskcacheConfig(BaseModel):
    shorturl_diskcache_folder: str


class DiskcacheProvider(CacheProvider):
    def __init__(self) -> None:
        super().__init__()
        self.diskcache_config = DiskcacheConfig.parse_obj(get_driver().config)
        self.cache = diskcache.Cache(self.diskcache_config.shorturl_diskcache_folder)

    @override
    async def lookup(self, index: str) -> str:
        url: str = self.cache.get(CACHE_KEY_FORMAT.format(index=index))  # type: ignore

        return url

    @override
    async def store(self, url: str) -> int:
        count = self.cache.get(COUNT_KEY_FORMAT, default=0) + 1  # type: ignore
        self.cache.set(COUNT_KEY_FORMAT, count)
        self.cache.set(CACHE_KEY_FORMAT.format(index=count), str(url))

        return count
