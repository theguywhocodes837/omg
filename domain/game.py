import random
import uuid


from utils import redis_connection

from .leaderboard import LeaderBoard


FRUIT_AVAILABLE = True
FRUIT_UN_AVILABLE = False
# There is a 10 % chance that a fruit will be
# avilable on the given step.
AVAILABLE_WEIGHT = 0.1
UN_AVAILABLE_WEIGHT = 0.9
FRUIT_CHOICES = [FRUIT_AVAILABLE, FRUIT_UN_AVILABLE]
FRUIT_WEIGHTS = [AVAILABLE_WEIGHT, UN_AVAILABLE_WEIGHT]
POINTS_PER_COLLECTION = 10


conn = redis_connection()


class Game:
    def __init__(self):
        self.game_id = str(uuid.uuid4())
        self._leaderboard = LeaderBoard()

    def start(self, username):
        if self.username:
            raise ValueError(
                "This method can be called only once"
            )
        if conn.exists(f"active_game:{username}"):
            raise ValueError(
                "User can only play one game at a time"
            )
        self.username = username
        self.steps = 0
        self.points = 0
        self.active = True
        conn.set(f"active_game:{username}", self.game_id)
        self._leaderboard.update(self, 0)

    @property
    def game_key(self):
        return f"game:{self.game_id}"

    def _get_hash_value(self, key):
        return conn.hget(self.game_key, key)

    def _set_hash_value(self, key, value):
        conn.hset(self.game_key, key, value)

    @property
    def username(self):
        _username = self._get_hash_value("username")
        if _username:
            return _username.decode("utf-8")

    @username.setter
    def username(self, value):
        self._set_hash_value("username", value)

    @property
    def active(self):
        is_active = self._get_hash_value("active")
        return bool(is_active)

    @active.setter
    def active(self, value):
        value = 1 if value else 0
        self._set_hash_value("active", value)

    @property
    def steps(self):
        _steps = self._get_hash_value("steps")
        if not _steps:
            _steps = 0
        else:
            _steps = int(_steps.decode("utf-8"))
        return _steps

    @steps.setter
    def steps(self, value):
        """This will cause issues when we have multiple instances of same
        game open. Here, I am assuming that a game object is handled by a
        single thread.
        """
        self._set_hash_value("steps", value)

    @property
    def points(self):
        _points = self._get_hash_value("points")
        if not _points:
            _points = 0
        else:
            _points = int(_points.decode("utf-8"))
        return _points

    @points.setter
    def points(self, value):
        self._set_hash_value("points", value)

    def collect_fruit(self):
        self.points += POINTS_PER_COLLECTION
        self._leaderboard.update(self, POINTS_PER_COLLECTION)

    def fruit_on_path(self):
        is_fruit_available = random.choices(
            FRUIT_CHOICES, FRUIT_WEIGHTS
        )[0]
        return is_fruit_available

    def walk(self):
        if not self.active:
            raise ValueError(
                "You can use this command on only live games. "
            )
        self.steps += 1
        if self.fruit_on_path():
            self.collect_fruit()

    def stop(self):
        self.active = False
        self._leaderboard.remove(self)
        conn.delete(f"active_game:{self.username}")

    def info(self):
        return {
            "game_id": self.game_id,
            "username": self.username,
            "steps": self.steps,
            "points": self.points,
            "active": self.active
        }

    @classmethod
    def get_by_id(cls, game_id):
        if not conn.exists(f"game:{game_id}"):
            raise ValueError(
                f"no game found for {game_id}"
            )
        game = cls()
        game.game_id = game_id
        return game
