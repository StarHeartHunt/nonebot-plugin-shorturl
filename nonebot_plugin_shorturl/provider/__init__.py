import abc


class CacheProvider(abc.ABC):
    @abc.abstractmethod
    async def lookup(self, index: int) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def store(self, url: str) -> int:
        raise NotImplementedError


from .memory import MemoryProvider as MemoryProvider
from .redis import RedisCacheProvider as RedisCacheProvider
from .diskcache import DiskcacheProvider as DiskcacheProvider
