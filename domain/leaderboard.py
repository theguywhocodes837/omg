from utils import redis_connection


conn = redis_connection()


class LeaderBoard:
    def __init__(self, name="game_leaderboard"):
        self.name = name

    def update(self, game, points):
        conn.zincrby(self.name, points, game.game_id)

    def remove(self, game):
        conn.zrem(self.name, game.game_id)

    def rank(self, game):
        game_rank = conn.zrevrank(self.name, game.game_id)
        if isinstance(game_rank, int):
            return game_rank + 1
        return game_rank

    def top_scores(self, n=5):
        res = []
        game_rank = 1
        entries = conn.zrevrange(self.name, 0, n - 1, "withscores")
        for game_id, score in entries:
            res.append({
                "game_id": game_id.decode("utf-8"),
                "score": score,
                "rank": game_rank
            })
            game_rank += 1
        return res
