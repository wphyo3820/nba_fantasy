from flask import Flask, render_template, request
from rank import get_league_stats, get_rankings


app = Flask(__name__)

@app.route("/")
def home():
	col_names = []

	last_n = request.args.get("last_n_games", 0, int)
	if request.args.get("FG_PCT", 1, int) == 1:
		col_names.append("FG_PCT")
	if request.args.get("FT_PCT", 1, int) == 1:
		col_names.append("FT_PCT")
	if request.args.get("FG3M", 1, int) == 1:
		col_names.append("FG3M")
	if request.args.get("PTS", 1, int) == 1:
		col_names.append("PTS")
	if request.args.get("REB", 1, int) == 1:
		col_names.append("REB")
	if request.args.get("AST", 1, int) == 1:
		col_names.append("AST")
	if request.args.get("STL", 1, int) == 1:
		col_names.append("STL")
	if request.args.get("BLK", 1, int) == 1:
		col_names.append("BLK")
	if request.args.get("TOV", 1, int) == 1:
		col_names.append("TOV")
	league_stats = get_league_stats(last_n=last_n)
	ranks = get_rankings(league_stats, col_names)
	return render_template("home.html", col_names = list(ranks), ranks = ranks)

#TODO: player cards
# @app.route("/playercard", methods=["GET"])
# def n_games():
# 	return render_template("player.html")


if __name__ == "__main__":
	app.run()