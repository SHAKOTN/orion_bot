import abc

from typing import List

import redis
from bot.utils import import_string
from plugins.notes.storage.settings import ENVIRONMENT, REDIS_CLASS


class NotesStorage(abc.ABC):

    def set_note(self, note_key: str, note: str):
        note_key = self._make_note_redis_key(note_key)
        self.set(note_key, note)

    def get_note(self, note_key: str):
        note_key = self._make_note_redis_key(note_key)
        return self.get(note_key)

    def _make_note_redis_key(self, key):
        return "note_key:{}".format(key)

    @abc.abstractmethod
    def get(self, key: str) -> dict:
        pass

    @abc.abstractmethod
    def set(self, key: str, data) -> dict:
        pass

    @abc.abstractmethod
    def keys(self):
        pass

    @abc.abstractmethod
    def clear(self):
        pass

    @abc.abstractmethod
    def delete(self, key):
        pass


class LocMemNotesStorage(NotesStorage):

    def __init__(self):
        self._hashmaps = {}

    def get(self, key: str):
        return self._hashmaps.get(key, "")

    def set(self, key: str, data: str):
        self._hashmaps[key] = data

    def keys(self):
        return self._hashmaps.keys()

    def clear(self):
        self._hashmaps = {}

    def delete(self, key):
        self._hashmaps.pop(key, None)

    @property
    def redis(self) -> dict:
        return self._hashmaps


class RedisNotesStorage(NotesStorage):
    def __init__(self, url):
        self._redis = redis.from_url(
            url,
            decode_responses=True
        )
        super().__init__()

    def get(self, key: str):
        return str(self.redis.get(key))

    def set(self, key: str, data: str):
        self.redis.set(key, data)

    def keys(self) -> List[str]:
        return self.redis.keys()

    def clear(self):
        pass

    def delete(self, key):
        self.redis.delete(key)

    @property
    def redis(self):
        return self._redis


def init_storage():
    redis_class = REDIS_CLASS[ENVIRONMENT]["CLASS"]
    params = REDIS_CLASS[ENVIRONMENT].get('OPTIONS', {})

    storage_cls = import_string(redis_class)
    return storage_cls(**params)

redis_storage = init_storage()
