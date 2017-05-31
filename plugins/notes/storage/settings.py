import os

ENVIRONMENT = os.environ.get("ENV")

REDIS_CLASS = {
    "development": {
        "CLASS": "plugins.notes.storage.redis.LocMemNotesStorage",
    },

    "production": {
        "CLASS": "plugins.notes.storage.redis.RedisNotesStorage",
        "OPTIONS": {
            "url": os.environ.get("REDIS_URL")
        }
    }
}
