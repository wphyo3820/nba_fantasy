from flask import Flask, render_template, request, redirect, url_for
from rank import get_rankings
from generate import generate_data
import pandas as pd

application = Flask(__name__)


@application.route("/")
def home():
    """
	Homepage for the web application
	Purpose: displays ranking sorted by total score
	"""
    col_names = []

    n_results = request.args.get("n", 100, int)

    if request.args.get("FGP", 1, int) == 1:
        col_names.append("FGP")
    if request.args.get("FTP", 1, int) == 1:
        col_names.append("FTP")
    if request.args.get("3PM", 1, int) == 1:
        col_names.append("3PM")
    if request.args.get("PPG", 1, int) == 1:
        col_names.append("PPG")
    if request.args.get("RPG", 1, int) == 1:
        col_names.append("RPG")
    if request.args.get("APG", 1, int) == 1:
        col_names.append("APG")
    if request.args.get("SPG", 1, int) == 1:
        col_names.append("SPG")
    if request.args.get("BPG", 1, int) == 1:
        col_names.append("BPG")
    if request.args.get("TPG", 1, int) == 1:
        col_names.append("TPG")

    data = pd.read_csv("data.csv")
    ranks = get_rankings(data, col_names, n_results)
    return render_template("home.html", col_names=list(ranks), ranks=ranks)


@application.route("/update")
def update():
    generate_data()
    return redirect(url_for('home'))


#TODO: player cards
@application.route("/playercard", methods=["GET"])
def n_games():
    return render_template("player.html")


if __name__ == "__main__":
    application.run(debug=True)
