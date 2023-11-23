from typing import Dict
from typing_extensions import override

from . import CacheProvider
from .consts import CACHE_KEY_FORMAT


class MemoryProvider(CacheProvider):
    def __init__(self) -> None:
        super().__init__()
        self.count = 0
        self.cache: Dict[str, str] = {}

    @override
    async def lookup(self, index: str) -> str:
        if not (url := self.cache.get(CACHE_KEY_FORMAT.format(index=index))):
            raise KeyError(f"Index {index} not found in cache")

        return url

    @override
    async def store(self, url: str) -> int:
        self.count += 1
        self.cache[CACHE_KEY_FORMAT.format(index=self.count)] = url

        return self.count
