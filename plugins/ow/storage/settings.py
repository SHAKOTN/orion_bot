import os

ENVIRONMENT = os.environ.get("ENV")

REDIS_CLASS = {
    "development": {
        "CLASS": "plugins.ow.storage.redis.LocMemStorage",
    },

    "production": {
        "CLASS": "plugins.ow.storage.redis.RedisStorage",
        "OPTIONS": {
            "url": os.environ.get("REDIS_URL")
        }
    }
}
