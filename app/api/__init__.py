from aiohttp import web

from .item import item_view
from .top_stories import top_stories_view

routes = [
    web.get("/topstories", top_stories_view),
    web.get("/items/{item_id}", item_view),
]
