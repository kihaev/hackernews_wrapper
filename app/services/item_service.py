import json

import aiohttp
from cache.redis import redis_cache
from config import app_config


async def get_item(item_id):
    async with aiohttp.ClientSession() as session:
        return await fetch_item_with_cached_kids(item_id, session)


async def fetch_item_with_cached_kids(item_id, session):
    cached_item = await redis_cache.get(item_id)
    if cached_item is not None:
        item = cached_item

    else:
        async with session.get(
            app_config.HACKER_NEWS_API_BASE_URL + f"item/{item_id}.json"
        ) as response:
            item = await response.json()

            await redis_cache.setx(item_id, item, 3600)

    if "kids" in item:
        kids = []
        for kid_id in item["kids"]:
            kid = await fetch_item_with_cached_kids(kid_id, session)
            kids.append(kid)
        item["kids"] = kids

    return item
