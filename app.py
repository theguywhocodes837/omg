from flask import Flask


from controller import users_current_rank, get_top_ranked_players


app = Flask(__name__)

from seed import seed


# seed the relevant data.
# This is used only for the demo purpose

seed()


@app.route("/<username>/rank")
def rank_view(username):
    return users_current_rank(username)


@app.route("/leaderboard")
@app.route("/leaderboard/<int:n>")
def leaderboard(n=5):
    return get_top_ranked_players(n)
