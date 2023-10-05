from decouple import config


class AppConfig:
    HACKER_NEWS_API_BASE_URL = config(
        "HACKER_NEWS_API_BASE_URL", default="https://hacker-news.firebaseio.com/v0/"
    )
    REDIS_URL = config("REDIS_URL", default="redis://test_redis:6379")
    HOST = config("HOST", default="0.0.0.0")
    PORT = config("PORT", default="8080")


app_config = AppConfig()
