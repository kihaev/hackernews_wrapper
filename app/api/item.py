from aiohttp import web
from services.item_service import get_item


async def item_view(request):
    item_id = request.match_info["item_id"]
    item = await get_item(item_id)
    return web.json_response(item)
