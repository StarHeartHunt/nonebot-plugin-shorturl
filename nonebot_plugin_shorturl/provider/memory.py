from typing import Dict
from typing_extensions import override

from . import CacheProvider
from .consts import CACHE_KEY_FORMAT


class MemoryProvider(CacheProvider):
    def __init__(self) -> None:
        super().__init__()
        self.cache: Dict[str, str] = {}

    @override
    async def lookup(self, token: str):
        url = self.cache.get(CACHE_KEY_FORMAT.format(token=token))

        return url

    @override
    async def store(self, url: str):
        token = await self.get_unique_token()
        self.cache[CACHE_KEY_FORMAT.format(token=token)] = url

        return token
