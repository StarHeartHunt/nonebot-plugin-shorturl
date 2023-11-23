from enum import Enum

from pydantic import Field, BaseModel, AnyHttpUrl


class CacheType(str, Enum):
    redis = "redis"
    diskcache = "diskcache"


class Config(BaseModel):
    shorturl_host: AnyHttpUrl
    shorturl_cache_type: CacheType = Field(CacheType.diskcache)
