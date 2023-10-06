import json

import redis.asyncio as redis
from config import app_config


class RedisCache:
    def __init__(self, app):
        self.app = app
        self.redis_pool = None

    def init_app(self, app):
        self.app = app
        app.on_startup.append(self.on_startup)
        app.on_cleanup.append(self.on_cleanup)

    async def on_startup(self, _):
        pool = redis.ConnectionPool.from_url(
            app_config.REDIS_URL, decode_responses=True
        )
        self.redis_pool = await redis.Redis.from_pool(pool)

    async def on_cleanup(self, _):
        if self.redis_pool is not None:
            await self.redis_pool.close(close_connection_pool=True)

    async def get(self, key):
        res = await self.redis_pool.get(key)
        return res

    async def set(self, key, value, seconds):
        await self.redis_pool.set(key, json.dumps(value), seconds)


redis_cache = RedisCache(None)
