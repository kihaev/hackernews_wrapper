import asyncio
import json

import aiohttp
from cache.redis import redis_cache
from config import app_config


async def get_top_stories():
    cached_top_stories = await redis_cache.get("top_stories")
    if cached_top_stories is not None:
        return json.loads(cached_top_stories)

    async with aiohttp.ClientSession() as session:
        async with session.get(
            app_config.HACKER_NEWS_API_BASE_URL + "topstories.json"
        ) as response:
            top_story_ids = await response.json()

        top_stories = []
        tasks = [
            asyncio.ensure_future(fetch_story_data(session, story_id))
            for story_id in top_story_ids[:10]
        ]

        completed_tasks = await asyncio.gather(*tasks)

        top_stories.extend(completed_tasks)

    await redis_cache.set("top_stories", top_stories, 3600)

    return top_stories


async def fetch_story_data(session, story_id):
    async with session.get(
        app_config.HACKER_NEWS_API_BASE_URL + f"item/{story_id}.json"
    ) as response:
        story = await response.json()
        return {
            "id": story.get("id"),
            "title": story.get("title"),
            "url": story.get("url"),
            "time": story.get("time"),
        }
