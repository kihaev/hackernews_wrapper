from aiohttp import web
from api import routes
from cache.redis import redis_cache
from config import app_config


def create_app():
    app = web.Application()

    app.add_routes(routes)

    redis_cache.init_app(app)

    return app


if __name__ == "__main__":
    web_app = create_app()
    web.run_app(web_app, host=app_config.HOST, port=int(app_config.PORT))
