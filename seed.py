from domain.game import Game

from utils import redis_connection


conn = redis_connection()


def seed():
    conn.flushall()
    users = [f"user{i}" for i in range(1, 20)]
    for user in users:
        game = Game()
        game.start(user)
        for step in range(1, 100):
            game.walk()
