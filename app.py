from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": game.board})


@app.post("/api/score-word")
def score_word():
    """Check if the word is legal and return JSON: {result}."""\

    word = request.json["word"].upper()

    game_id = request.json["gameId"]
    game = games[game_id]

    is_word = game.is_word_in_word_list(word)
    is_findable = game.check_word_on_board(word)
    is_not_duplicate = game.is_word_not_a_dup(word)

    if not is_word:
        return jsonify({"result": "not-word"})
    elif not is_findable:
        return jsonify({"result": "not-on-board"})
    elif not is_not_duplicate:
        return jsonify({"result": "duplicate"})
    else:
        word_score = game.play_and_score_word(word)
        return jsonify({"result": "ok", "score": word_score})

    # the request will have JSON with game_id and the word (can get with request.json)
    # check if the word is legal (in the word list AND findable on the board)
    # return JSON
    # if not a word ---> {result: "not-word"}
    # if not on board -> {result: "not-on-board"}
    # if valid word ---> {result: "ok"}
