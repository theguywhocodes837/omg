import json


from flask import Response


from utils import redis_connection
from domain.game import Game
from domain.leaderboard import LeaderBoard


conn = redis_connection()


leaderboard = LeaderBoard()



def users_current_rank(username):
    game_id = conn.get(f"active_game:{username}")
    if not game_id:
        data = {"msg": "could not find any active games"}
    else:
        game = Game.get_by_id(game_id.decode("utf-8"))
        data = {
            **game.info(),
            **{"rank": leaderboard.rank(game)}
        }
    return Response(
        json.dumps(data),
        content_type="application/json"
    )


def get_top_ranked_players(n):
    res = []
    for score in leaderboard.top_scores(n):
        game = Game.get_by_id(score["game_id"])
        res.append({
            **game.info(),
            **score
        })
    return Response(
        json.dumps(res),
        content_type="application/json"
    )
