<!-- markdownlint-disable MD033 MD036 MD041 -->

<p align="center">
  <a href="https://nonebot.dev/">
    <img src="https://nonebot.dev/logo.png" height="100" alt="nonebot">
  </a>
</p>

<div align="center">

# nonebot-plugin-shorturl

_✨ 为 NoneBot 插件提供短链接服务支持 ✨_

</div>

<p align="center">
  <a href="https://github.com/StarHeartHunt/nonebot-plugin-shorturl/master/LICENSE">
    <img src="https://img.shields.io/github/license/StarHeartHunt/nonebot-plugin-shorturl.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-shorturl">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-shorturl.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</p>

## 使用方式

在 `.env` 文件中添加必填的配置项

## 配置项

### 通用配置项

- `SHORTURL_HOST`（必填）：用于为外部插件构造完整的包含域名的短链接。示例值：`http://localhost:8080`
- `SHORTURL_ENDPOINT`：指定短链接服务的入口点模板。默认值：`/shorturl/{encoded}`，可以自定义为 `/s/{encoded}` 等
- `SHORTURL_CACHE_TYPE`：指定短链接服务的后端缓存类型，可选值：`memory` | `diskcache` | `redis`

### 差分配置项

#### Redis

- `SHORTURL_REDIS_HOST`：Redis 后端的地址
- `SHORTURL_REDIS_PORT`：Redis 后端的端口
- `SHORTURL_REDIS_DB`：Redis DB 配置项
- `SHORTURL_REDIS_USERNAME`：Redis 用户名
- `SHORTURL_REDIS_PASSWORD`：Redis 密码

#### Diskcache

- `SHORTURL_DISKCACHE_FOLDER`：Diskcache 文件持久化目录
