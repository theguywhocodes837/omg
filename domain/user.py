from utils import redis_connection


conn = redis_connection()


class User:
    def __init__(self, username, name):
        self._username = username
        self.name = name

    def _hash_value(self, key):
        return conn.hget(f"user:{self.username}", key)

    def _set_hash_value(self, key, value):
        conn.hset(f"user:{self.username}", key, value)

    def __repr__(self):
        return self.username

    @property
    def username(self):
        return self._username

    @property
    def name(self):
        return self._hash_value("name")

    @name.setter
    def name(self, value):
        self._set_hash_value("name", value)

    @property
    def avatar(self):
        return self._hash_value("avatar")

    @avatar.setter
    def avatar(self, value):
        self._set_hash_value("avatar", value)

    @property
    def tagline(self):
        return self._hash_value("tagline")

    @tagline.setter
    def tagline(self, value):
        self._set_hash_value("tagline", value)
