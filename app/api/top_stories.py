from aiohttp import web
from services.top_stories_service import get_top_stories


async def top_stories_view(request):
    top_stories = await get_top_stories()
    return web.json_response(top_stories)
