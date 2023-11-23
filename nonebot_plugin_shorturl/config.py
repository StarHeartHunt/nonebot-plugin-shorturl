from enum import Enum

from pydantic import Field, BaseModel, AnyHttpUrl


class CacheType(str, Enum):
    redis = "redis"
    memory = "memory"
    diskcache = "diskcache"


class Config(BaseModel):
    shorturl_host: AnyHttpUrl
    shorturl_endpoint: str = Field("/shorturl/{encoded}")
    shorturl_cache_type: CacheType = Field(CacheType.memory)
