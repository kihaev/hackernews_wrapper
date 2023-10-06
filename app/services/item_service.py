import json

import aiohttp
from cache.redis import redis_cache
from config import app_config


async def get_item(item_id):
    async with aiohttp.ClientSession() as session:
        return await fetch_item(item_id, session)


async def fetch_item(item_id, session):
    cached_item = await redis_cache.get(item_id)
    if cached_item is not None:
        item = json.loads(cached_item)
    else:
        async with session.get(
            app_config.HACKER_NEWS_API_BASE_URL + f"item/{item_id}.json"
        ) as response:
            res = await response.json()

            item = prepare_item_data(res)

            await redis_cache.set(item_id, item, 3600)

    if "kids" in item and item["kids"] is not None:
        kids = []
        for kid_id in item["kids"]:
            kid = await fetch_item(kid_id, session)
            kids.append(kid)
        item["kids"] = kids

    return item


def prepare_item_data(item):
    field_mapping = {
        "story": {"id": "id", "url": "url", "kids": "kids"},
        "comment": {"by": "by", "text": "text", "time": "time", "kids": "kids"},
    }

    item_type = item.get("type", "")
    result = {
        new_key: item.get(old_key)
        for new_key, old_key in field_mapping.get(item_type, {}).items()
    } or item

    return result
